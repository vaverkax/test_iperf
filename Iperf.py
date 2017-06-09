import subprocess
import sys
import json
import re

class Ipref:
    def __init__(self, host):
        self.host = host
        self.test = ""
        self.commandClient = ""
        self.commandServer = ""
        self.result = ""
        self.dictout = {"error": "",
                   "result": {},
                   "status": ""
                   }
        self.serverresultconnect = 0


    def setTime(self, time):
        self.time = time
        return self.time

    def setType(self, test):
        self.test = test
        return self.test

    def makeCommandServer(self):
        commandServer = ['ssh', '-n', self.host, 'iperf3', '-s', '-D', '-1']
        self.commandServer = commandServer
        return self.commandServer

    def startServer(self):
        proc = subprocess.Popen(self.commandServer)
        proc.wait()
        res = proc.communicate()
        self.serverresultconnect = proc.returncode
        return proc.returncode

    def makeCommandClient(self):
        commandClient = ['iperf3', '-c', self.host, '-t', self.time]
        if self.test == 'udp':
            commandClient.append('-u')
        self.commandClient = commandClient
        return self.commandClient

    def startClient(self):

        proc = subprocess.Popen(self.commandClient, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        self.result= proc.communicate()
        return proc.returncode


    def stop(self):
        command = ['ssh', '-n', self.host, 'pkill', 'iperf3']
        res = subprocess.call(command)
        return res



    def parse(self):
       if self.serverresultconnect != 0:
           self.dictout["error"] = "server connection error"
           self.dictout["status"] = "-1"
           json_data = json.dumps(self.dictout, indent=4)
           print json_data
           return -1

       arr = str(self.result[0])
       error = re.findall(r'error', arr)
       if error != []:
           errlis = re.split('-',arr)
           self.dictout["error"] = errlis[1]
           self.dictout["status"] = "-1"
           json_data = json.dumps(self.dictout, indent=4)
           print json_data
           return -1

       lis = list(re.split('\n', arr))
       ip =re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',lis[0])


       data = []
       x = 0
       y = int(self.time)
       while x < y:
           tmp_dict = {}
           tmp_dict = {"ip": ip ,"interval": re.findall(r'\d{1,9}.\d{2}-\d{1,9}.\d{2}',lis[x+3]),
                                         "transfer": re.findall(r'\d{3} MBytes',lis[x+3]),
                                         "bandwidth":re.findall(r'\d{1}.\d{2} Gbits/sec', lis[x+3])}

           data.append(tmp_dict)
           x = x + 1

       self.dictout["result"] = ""
       self.dictout["result"] = data
       self.dictout["status"] = "0"
       json_data = json.dumps(self.dictout, indent = 4)
       print json_data


       return json_data



