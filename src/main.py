# main.py

import sys
import getopt
import signal
from utils import check_root, sigint_handler, print_usage
from tor_control import start_torward, stop_torward, request_new_tor_circuit
from constants import VERSION

def main():
    check_root()
    signal.signal(signal.SIGINT, sigint_handler)

    if len(sys.argv) <= 1:
        print_usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'srxhu', ['start', 'switch', 'stop', 'help', 'update'])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for o, a in opts:
        if o in ('-h', '--help'):
            print_usage()
        elif o in ('-s', '--start'):
            start_torward()
        elif o in ('-x', '--stop'):
            stop_torward()
        elif o in ('-r', '--switch'):
            request_new_tor_circuit()
        else:
            print_usage()

if __name__ == '__main__':
    main()
