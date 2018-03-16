from tests.system.common import CondoorTestCase, StopTelnetSrv, StartTelnetSrv
from tests.dmock.dmock import C4500XHandler
from tests.utils import remove_cache_file

import condoor


class TestC4500XConnection(CondoorTestCase):
    @StartTelnetSrv(C4500XHandler, 10024)
    def setUp(self):
        CondoorTestCase.setUp(self)

    @StopTelnetSrv()
    def tearDown(self):
        pass

    def test_C4500X_1_discovery(self):

        remove_cache_file()

        urls = ["telnet://admin:admin@127.0.0.1:10024"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "Switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "C4500-X", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "WS-C4500X-32", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "XE", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "03.08.03.E", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Switch System", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Cisco Systems, Inc. WS-C4500X-32 2 slot switch",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "JAE154100BA", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "Switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console connection not detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_C4500X_1_rediscovery(self):

        urls = ["telnet://admin:admin@127.0.0.1:10024"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "Switch", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "C4500-X", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "WS-C4500X-32", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "XE", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "03.08.03.E", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Switch System", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Cisco Systems, Inc. WS-C4500X-32 2 slot switch",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "JAE154100BA", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "Switch#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console connection not detected")
        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()



if __name__ == '__main__':
    from unittest import main
    main()
