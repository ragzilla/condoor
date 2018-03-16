from tests.system.common import CondoorTestCase, StopTelnetSrv, StartTelnetSrv
from tests.dmock.dmock import XR12KHandler
from tests.utils import remove_cache_file

import condoor


class TestXR12KConnection(CondoorTestCase):
    @StartTelnetSrv(XR12KHandler, 10023)
    def setUp(self):
        CondoorTestCase.setUp(self)

    @StopTelnetSrv()
    def tearDown(self):
        pass

    def test_XR12K_1_discovery(self):
        """ASR9k: Test the connection and discovery"""

        remove_cache_file()

        urls = ["telnet://admin:admin@127.0.0.1:10023"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        # TODO: Test if device_info is correct
        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "GSR-PE19", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "XR12K", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "GSR16", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "XR", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "4.2.1", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Cisco 12416 320 Gbps",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "GSR16/320", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "1.0", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "TBM12077586", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "RP/0/7/CPU0:GSR-PE19#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console: {}".format(conn.is_console))

        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()

    def test_XR12K_2_rediscovery(self):
        """ASR9k: Test whether the cached information is used"""
        urls = ["telnet://admin:admin@127.0.0.1:10023"]
        conn = condoor.Connection("host", urls, log_session=self.log_session, log_level=self.log_level)
        self.conn = conn
        conn.connect(self.logfile_condoor)

        self.assertEqual(conn.is_discovered, True, "Not discovered properly")
        self.assertEqual(conn.hostname, "GSR-PE19", "Wrong Hostname: {}".format(conn.hostname))
        self.assertEqual(conn.family, "XR12K", "Wrong Family: {}".format(conn.family))
        self.assertEqual(conn.platform, "GSR16", "Wrong Platform: {}".format(conn.platform))
        self.assertEqual(conn.os_type, "XR", "Wrong OS Type: {}".format(conn.os_type))
        self.assertEqual(conn.os_version, "4.2.1", "Wrong Version: {}".format(conn.os_version))
        self.assertEqual(conn.udi['name'], "Chassis", "Wrong Name: {}".format(conn.udi['name']))
        self.assertEqual(conn.udi['description'], "Cisco 12416 320 Gbps",
                         "Wrong Description: {}".format(conn.udi['description']))
        self.assertEqual(conn.udi['pid'], "GSR16/320", "Wrong PID: {}".format(conn.udi['pid']))
        self.assertEqual(conn.udi['vid'], "1.0", "Wrong VID: {}".format(conn.udi['vid']))
        self.assertEqual(conn.udi['sn'], "TBM12077586", "Wrong S/N: {}".format(conn.udi['sn']))
        self.assertEqual(conn.prompt, "RP/0/7/CPU0:GSR-PE19#", "Wrong Prompt: {}".format(conn.prompt))
        self.assertEqual(conn.is_console, False, "Console: {}".format(conn.is_console))

        with self.assertRaises(condoor.CommandSyntaxError):
            conn.send("wrongcommand")

        conn.disconnect()



if __name__ == '__main__':
    from unittest import main
    main()
