from Iperf import *

import sys
import argparse


parser = argparse.ArgumentParser(description="Testing network utility.")
parser.add_argument("host", help="Host address", type=str)
parser.add_argument("-t", help="Set time for testing", default=10)
parser.add_argument("-u", help="Set UDP type", action="store_true")
args = parser.parse_args()


host = args.host

srv = Ipref(host)
srv.setTime(args.t)

if args.u:
    srv.setType("-u")

srv.makeCommandClient()
srv.makeCommandServer()
srv.startServer()
srv.startClient()
srv.parse()
srv.stop()
