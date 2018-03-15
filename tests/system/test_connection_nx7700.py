from tests.system.common import CondoorTestCase, StopTelnetSrv, StartTelnetSrv
from tests.dmock.dmock import NX7700Handler, NX7700CHandler
from tests.utils import remove_cache_file

import condoor


class TestNX7700Connection(CondoorTestCase):
    @StartTelnetSrv(NX7700Handler, 10024)
    def setUp(self):
        CondoorTestCase.setUp(self)

    @StopTelnetSrv()
    def tearDown(self):
        pass

    def test_NX7700_1_discovery(self):

        remove_cache_file()

        urls = ["telnet://admin:admin@127.0.0.1:10024"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "Nexus7000", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "N77-C7706", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "NX-OS", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "8.1(2a)", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Nexus7700 C7706 (6 Slot) Chassis",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "N77-C7706", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "V01", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "FXS1824Q0SE", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console connection detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_NX7700_2_rediscovery(self):

        urls = ["telnet://admin:admin@127.0.0.1:10024"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "Nexus7000", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "N77-C7706", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "NX-OS", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "8.1(2a)", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Nexus7700 C7706 (6 Slot) Chassis",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "N77-C7706", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "V01", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "FXS1824Q0SE", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console connection detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_NX7700_3_connection_wrong_user(self):
        urls = ["telnet://root:admin@127.0.0.1:10024"]
        self.conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)

        with self.assertRaises(condoor.ConnectionAuthenticationError):
            self.conn.connect(self.logfile_condoor)

        self.conn.disconnect()


class TestNX7700CConnection(CondoorTestCase):
    @StartTelnetSrv(NX7700CHandler, 10026)
    def setUp(self):
        CondoorTestCase.setUp(self)

    @StopTelnetSrv()
    def tearDown(self):
        pass

    def test_NX7700C_1_discovery(self):

        remove_cache_file()

        urls = ["telnet://admin:admin@127.0.0.1:10026"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "Nexus7000", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "N77-C7706", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "NX-OS", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "8.1(2a)", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Nexus7700 C7706 (6 Slot) Chassis",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "N77-C7706", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "V01", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "FXS1824Q0SE", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, True, "Console connection not detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_NX7700C_2_rediscovery(self):

        urls = ["telnet://admin:admin@127.0.0.1:10026"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "Nexus7000", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "N77-C7706", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "NX-OS", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "8.1(2a)", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Nexus7700 C7706 (6 Slot) Chassis",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "N77-C7706", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "V01", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "FXS1824Q0SE", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, True, "Console connection not detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_NX7700C_3_connection_wrong_user(self):
        urls = ["telnet://root:admin@127.0.0.1:10026"]
        self.conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)

        with self.assertRaises(condoor.ConnectionAuthenticationError):
            self.conn.connect(self.logfile_condoor)

        self.conn.disconnect()


if __name__ == '__main__':
    from unittest import main
    main()
