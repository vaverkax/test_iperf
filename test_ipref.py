from unittest import TestCase
from Iperf import Ipref

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
