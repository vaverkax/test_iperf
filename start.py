from Iperf import *

import sys


if len(sys.argv) < 2:
    print "usage: python start.py host"
    sys.exit()

host = sys.argv[1]

srv = Ipref(host)

if len(sys.argv) == 3:
    srv.setTime(sys.argv[2])
else:
    srv.setTime('10')

if len(sys.argv) == 4:
    srv.setType("-u")

srv.makeCommandClient()
srv.makeCommandServer()
srv.startServer()
srv.startClient()
srv.parse()
srv.stop()
