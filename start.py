import argparse
import sys

from Iperf import *

parser = argparse.ArgumentParser(description="Testing network utility.")
parser.add_argument("host", help="Host address", type=str)
parser.add_argument("-t", help="Set time for testing", default='10')
parser.add_argument("-u", help="Set UDP type", action="store_true")
args = parser.parse_args()
if __name__ == "__main__":
    host = args.host

    srv = Ipref(host)
    srv.set_time(args.t)

    if args.u:
        srv.set_type("-u")

    try:
        srv.make_command_client()
        srv.make_command_server()
        srv.start_server()
        #srv.start_client()
        srv.parse()
        srv.stop()
    except Exception as err:
        sys.stderr.write(err.message)
        sys.exit(1)
    finally:
        sys.exit(0)
