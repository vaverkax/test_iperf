import subprocess
import json
import re


class Ipref:
    def __init__(self, host):
        self.host = host
        self.test = ""
        self.command_client = ""
        self.command_server = ""
        self.result = ""
        self.dictout = {"error": "",
                        "result": {},
                        "status": ""
                        }
        self.server_result_connect = 0

    def set_time(self, time):
        self.time = time
        return self.time

    def set_type(self, test):
        self.test = test
        return self.test

    def make_command_server(self):
        command_server = ['ssh', '-n', self.host, 'iperf3', '-s', '-D']
        self.command_server = command_server
        return self.command_server

    def start_server(self):
        try:
            subprocess.check_call(self.command_server)
        except subprocess.CalledProcessError as err:
            print err.output
            return err.returncode
        except OSError:
            return -1
        finally:
            self.server_result_connect = 0
            return 0

    def make_command_client(self):
        command_client = ['iperf3', '-c', self.host, '-t', self.time]
        if self.test == 'udp':
            command_client.append('-u')
        self.command_client = command_client
        return self.command_client

    def start_client(self):
        proc = subprocess.Popen(self.command_client, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            self.result = proc.communicate()
            return 0
        else:
            print "Client Connection error"
            return 1

    def stop(self):
        command = ['ssh', '-n', self.host, 'pkill', 'iperf3']
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as err:
            print err.output
            return err.returncode
        except OSError:
            return -1
        finally:
            return 0

    def parse(self):
        if self.server_result_connect != 0:
            self.dictout["error"] = "server connection error"
            self.dictout["status"] = "-1"
            json_data = json.dumps(self.dictout, indent=4)
            print json_data
            return -1

        arr = str(self.result[0])
        error = re.findall(r'error', arr)
        if error:
            errlis = re.split('-', arr)
            self.dictout["error"] = errlis[1]
            self.dictout["status"] = "-1"
            json_data = json.dumps(self.dictout, indent=4)
            print json_data
            return -1

        lis = list(re.split('\n', arr))
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', lis[0])
        patt = re.compile(r'[ \d]\s+(?P<interval>\d+\.\d+-\d+\.\d+)'
                          r'\s+\w+\s+'
                          r'(?P<transfer>\d+ \w+)\s+'
                          r'(?P<bandwidth>\d+\.\d+ \w+/\w+)')

        data = []
        x = 0
        y = int(self.time)
        while x < y:
            search_result = re.search(patt, lis[x + 3])
            tmp_dict = {"ip": ip, "interval": search_result.group('interval'),
                        "transfer": search_result.group('transfer'),
                        "bandwidth": search_result.group('bandwidth')}

            data.append(tmp_dict)
            x = x + 1

        self.dictout["result"] = ""
        self.dictout["result"] = data
        self.dictout["status"] = "0"
        json_data = json.dumps(self.dictout, indent=4)
        print json_data

        return json_data
