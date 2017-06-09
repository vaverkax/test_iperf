from unittest import TestCase
from Iperf import Ipref
import json

class TestIpref(TestCase):
    def test_setTime(self):

        ip = Ipref('192.168.10.136')
        self.assertEqual(ip.setTime('15'), '15')

    def test_setType(self):
        type = "-udp"
        ip = Ipref('192.168.10.136')
        self.assertEqual(ip.setType(type), type)


    def test_makeCommandServer(self):
        ip = Ipref('192.168.10.136')
        command =  ['ssh', '-n', '192.168.10.136', 'iperf3', '-s', '-D', '-1']
        self.assertEqual(ip.makeCommandServer(),command)


    def test_startServer(self):
        ip = Ipref('192.168.10.136')
        ip.makeCommandServer()
        self.assertEqual(ip.startServer(), 0)
        ip.stop()

    def test_makeCommandClient(self):
        ip = Ipref('192.168.10.136')
        ip.test = 'udp'
        ip.time = '11'
        command = ['iperf3', '-c','192.168.10.136', '-t','11', '-u']
        self.assertEqual(ip.makeCommandClient(), command)


    def test_startClient(self):
        ip = Ipref('192.168.10.136')
        ip.time = '11'
        ip.makeCommandClient()
        ip.makeCommandServer()
        ip.startServer()
        self.assertEqual(ip.startClient(), 0)
        ip.stop()

    def test_stop(self):
        ip = Ipref('192.168.10.136')
        self.assertEqual(ip.stop(), 0)

    def test_parse(self):
        ip = Ipref('192.168.10.136')
        testjson = '{\n    "status": "0", \n    "result": [\n        {\n            "ip": [\n                "192.168.10.136"\n            ], \n            "bandwidth": [\n                "3.69 Gbits/sec"\n            ], \n            "interval": [\n                "0.00-1.00"\n            ], \n            "transfer": [\n                "441 MBytes"\n            ]\n        }, \n        {\n            "ip": [\n                "192.168.10.136"\n            ], \n            "bandwidth": [\n                "2.90 Gbits/sec"\n            ], \n            "interval": [\n                "1.00-2.00"\n            ], \n            "transfer": [\n                "346 MBytes"\n            ]\n        }\n    ], \n    "error": ""\n}'

        ip.time = '2'
        ip.result = ['Connecting to host 192.168.10.136, port 5201\n[  4] local 192.168.10.137 port 56078 connected to 192.168.10.136 port 5201\n[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd\n[  4]   0.00-1.00   sec   441 MBytes  3.69 Gbits/sec  667    390 KBytes   \n[  4]   1.00-2.00   sec   346 MBytes  2.90 Gbits/sec  544    192 KBytes       \n']
        self.assertEqual(ip.parse(), testjson)