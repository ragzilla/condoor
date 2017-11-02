import os
import sys
import yaml
import condoor
import threading
from time import sleep
from collections import defaultdict

config = """
devices:
  # hostname
  device1:
    # driver i.e. XR, eXR, NX-OS, IOS
    driver: 'XR'
    prompts:
      # sometimes tacacs has a custom prompts
      tacacs:
        # optional default to driver prompt
        user_prompt: "[Uu]sername: "
        # optional default to driver prompt
        password_prompt: "[Pp]assword: "
      # local prompts for tacacs fallback or no tacacs
      local:
        # optional default to driver prompt
        user_prompt: "[Uu]sername: "
        # optional default to driver prompt
        password_prompt: "[Pp]assword: "
      jumphost:
        # optional default to driver prompt
        user_prompt: '[U|u]sername:\s|login:\s?|BRIDGETON NOC:\s?'
        # optional default to driver prompt
        password_prompt: '[P|p]assword:\s?|Password :\s?'

    credentials:
      jumphost:
        username: klstanie
        password: pass
      console:
        username: lab
        password: lab
      line:
        username: root
        password: root
      admin:
        username: root
        password: root
      enable:
        username: root
        password: root

    jumphost:
      protocol: ssh
      ip: localhost
      port: 22
      # could be useful to handle dynamic prompt (i.e. with linenum)
      # device_prompt: '[#>\$]'

    connections:
      # console_a
      a:
        protocol: telnet
        ip: 10.86.188.23
        port: 2060
      # console_b
    #   b:
    #     protocol: telnet
    #     ip: 10.86.188.23
    #     port: 2038
    #   # vty
      vty:
        protocol: telnet
        ip: 10.86.188.84
        port: 23
      
      alt:
        protocol: ssh
        ip: 10.86.188.84
        port: 24

    logging:
      directory: /tmp

"""

RC_OK = 0
RC_CONNECTION_ERROR = 1
RC_AUTHENTICATION_ERROR = 2
RC_COMMAND_SYNTAX_ERROR = 3

error_messages = [
    "Success",
    "Connection Error",
    "Authentication Error",
    "Command Syntax Error",
]


# this is a temporaty
def make_url(ip=None, protocol=None, port=None, username=None, password=None):
    return "{}://{}:{}@{}:{}".format(protocol, username, password, ip, port)


with open("config.yaml", "w") as f:
    f.write(config)


def loader(config_file):
    with open(config_file, "r") as f:
        config = yaml.load(f)
        # add voltopus validation
        return config['devices']
    return None


def make_devices_from_config(config):
    if isinstance(config, dict):
        devices = {}
        for key, config in config.items():
            devices[key] = Device(key, config)
        return devices
    assert "Error"


class WorkerThread(threading.Thread):
    def __init__(self, name, func, **kwargs):
        threading.Thread.__init__(self, name=name)
        self.rc = RC_OK
        self.func = func
        self.kwargs = kwargs


class ConnectionThread(WorkerThread):
    def run(self):
        print("Connecting to {}...".format(self.name))
        try:
            self.func(**self.kwargs)
            print("Connected to {}.".format(self.name))
        except condoor.ConnectionAuthenticationError:
            self.rc = RC_AUTHENTICATION_ERROR
            print("Connection authentication to {} failed.".format(self._name))
        except condoor.ConnectionError:
            self.rc = RC_CONNECTION_ERROR
            print("Connection to {} failed.".format(self.name))


class DisconnectThread(WorkerThread):
    def run(self):
        print("Disconnecting {}".format(self.name))
        try:

            self.func(**self.kwargs)
            print("Disconnected from {}".format(self.name))
        except condoor.ConnectionError as e:
            print(e)
            self.rc = RC_CONNECTION_ERROR
            print("Disconnection from {} failed.".format(self.name))


class Device(object):
    def __init__(self, name, config):
        self._name = name
        self._config = config
        self._connections = dict()
        self._log_fds = dict()
        self._return_codes = dict()
        self._make_connections()
        self._context = None

    def _get_credentials(self, via):
        # to be updated
        return self._config['credentials']['line']

    def _get_suitable_context(self):
        # TODO: check if vty is even defined
        context = 'vty'
        if 'vty' not in self._connections:
            if 'a' in self._connections:
                context = 'a'
            elif 'b' in self._connections:
                context = 'b'
        return context

    def _make_connections(self):
        connection_via = list(self._config['connections'].keys())
        for via in connection_via:
            connection_config = self._config['connections'][via]
            credentials = self._get_credentials(via)
            connection_config.update(
                username=credentials['username'],
                password=credentials['password']
            )
            url = make_url(**connection_config)
            self._connections[via] = condoor.Connection(
                self.hostname, urls=url, log_level=0, log_session=True
            )

    def _open_log_file(self, via, name):
        filename = '{}_{}.log'.format(name, via)
        try:
            log_dir = self._config['logging']['directory']
        except KeyError:
            log_dir = None

        fd = None
        if log_dir:
            full_path = os.path.join(log_dir, filename)
            try:
                fd = open(full_path, "a+")
            except (OSError, IOError) as ex:
                print("Error in opening logfile: {}".format(str(ex)))
            print("{} {} logging to {}".format(via, name, full_path))
        else:
            fd = sys.stdout
        return fd

    def _close_log_file(self, fd):
        if fd != sys.stdout:
            try:
                fd.close()
            except (OSError, IOError) as ex:
                print("Error in closing logfile: {}".format(str(ex)))

    @property
    def hostname(self):
        return self._name

    @property
    def connections(self):
        con = {}
        for name, connection in self._connections.items():
            try:
                con[name] = connection.is_connected
            except condoor.ConnectionError:
                con[name] = False
        return con

    @property
    def rc(self):
        if self._context:
            return self._return_codes[self._context]
        else:
            return self._return_codes

    def connect(self, alias=None, via=None, force_discovery=False):
        if via:
            connection_via = [via]
        else:
            if self._context:
                # connect to context
                connection_via = [self._context]
            else:
                # connect to all
                connection_via = list(self._config['connections'].keys())

        threads = []
        for via in connection_via:
            thread = self._make_connect_thread(via, force_discovery=force_discovery)
            thread.start()
            threads.append(thread)
            # sleep(2)

        for thread in threads:
            thread.join()
            self._return_codes[thread.name] = thread.rc
        print("Done")

    def _make_connect_thread(self, via, **kwargs):
        logs = {
            'logfile': self._open_log_file(via, 'session'),
            'tracefile': self._open_log_file(via, 'condoor')
        }
        self._log_fds[via] = logs
        kwargs.update(logs)
        connection = self._connections[via]
        name = "{}".format(via)
        thread = ConnectionThread(name=name, func=connection.connect, **kwargs)
        thread.daemon = False
        return thread

    def _make_disconnect_thread(self, via):
        connection = self._connections[via]
        name = "{}".format(via)
        thread = DisconnectThread(name=name, func=connection.disconnect)
        thread.daemon = False
        return thread

    def __getattr__(self, name):
        if name in self._config['connections'].keys():
            self._context = name
            return self

        if not self._context:
            context = self._get_suitable_context()
            self._context = context

        connection = self._connections[self._context]

        try:
            attr = connection.__getattribute__(name)
        except KeyError:
            print("no attribute: {}".format(name))
            raise KeyError

        if callable(attr):
            def wrapp_method(*args, **kwargs):
                try:
                    self._return_codes[self._context] = RC_OK
                    connection.send()
                    if connection.is_connected:
                        return attr(*args, **kwargs)
                    else:
                        self._return_codes[self._context] = RC_CONNECTION_ERROR

                except condoor.ConnectionError:
                    self._return_codes[self._context] = RC_CONNECTION_ERROR
                except condoor.CommandSyntaxError:
                    self._return_codes[self._context] = RC_COMMAND_SYNTAX_ERROR

                if self._return_codes[self._context] == RC_CONNECTION_ERROR:
                    try:
                        self.disconnect(via=self._context)
                    except condoor.ConnectionError:
                        print("already disconnected")

                    try:
                        self._return_codes[self._context] = RC_OK
                        self.connect(via=self._context, force_discovery=True)
                        self._context = None
                        return attr(*args, **kwargs)
                    except condoor.ConnectionError:
                        self._return_codes[self._context] = RC_CONNECTION_ERROR

            return wrapp_method
        self._context = None
        return attr

    def disconnect(self, via=None):
        if via:
            connection_via = [via]
        else:
            if self._context:
                # connect to context
                connection_via = [self._context]
            else:
                # connect to all
                connection_via = list(self._config['connections'].keys())
        threads = []
        for via in connection_via:
            connection = self._connections[via]
            try:
                if connection.is_connected:
                    thread = self._make_disconnect_thread(via)
                    threads.append(thread)
                    thread.start()
            except condoor.ConnectionError:
                continue

        for thread in threads:
            thread.join()



"""
import condoor
config = condoor.loader('config.yaml')
devices = condoor.make_devices_from_config(config)
d = devices['device1']
d.a.send('show users')
d.disconnect()

exit()

d.connect()


d.connect(alias='mgmt', via='vty1')
d.connect(alias='console', via='a')
"""
