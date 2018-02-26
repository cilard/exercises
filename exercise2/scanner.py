#############
# Functions #
#############

# FUNCTION 'get_target()': Check the format of host or network address supplied
#   as parameter on the command line.
# RETRUNS: Target host IP or network address
import argparse
import ipaddress

def get_target():

    global target_is_net

    # Host address
    if "/" not in args.target:
        # Correct format used?
        try:
            return ipaddress.ip_address(args.target)
        except ValueError:
            return False
    # Network address in CIDR notation
    else:
        # Correct format used?
        try:
            # Change the target flag to network address
            target_is_net = True
            return ipaddress.ip_network(args.target)
        except ValueError:
            return False


# FUNCTION 'port_print(host_ip, port, flag)': Print port status on the screen.
#
# RETURNS:

def port_print(host_ip, port, flag):

    print('Host: {}{}Ports: {}/open/tcp [{}]'.format(host_ip, '\t\t', port, flag))


# FUNCTION 'scan_ports(host_ip)': Scan well-known TCP ports of a host specified by
#   'host_ip' parameter
# RETRUNS:
import socket

def scan_ports(host_ip):

    global scan_db

    for i in range(1,1024):
        # Reset port state flag to [No change]
        flag = 'No change'
        # Open then close TCP socket using port 'i'
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock_tcp.connect_ex((host_ip, i))
        sock_tcp.close()
        # Port is OPEN
        if result == 0:
            # If host doesn't exist in the DB, create the host
            if host_ip not in scan_db:
                scan_db[host_ip] = []
            # Opened port doesn't exist in the DB
            if i not in scan_db[host_ip]:
                # Set port state flag to [New] open port
                flag = 'New'
                # Add the opened port into DB
                scan_db[host_ip].append(i)
            port_print(host_ip, i, flag)
        # Port is CLOSED
        else:
            # Host exists in the DB
            if host_ip in scan_db:
                # Closed port exist in the DB
                if i in scan_db[host_ip]:
                    # Set the port state flag to open port is now [Closed]'
                    flag = 'Closed'
                    # Remove the closed port from DB
                    scan_db[host_ip].remove(i)
                    port_print(host_ip, i, flag)

# FUNCTION 'do_scan(target)': Perform port scan of a host or network by using
#   'target' var from 'get_target()' function. Limit the range of IP addresses in
#   the network by using the 'range' parameter.
# RETURNS:

def do_scan(target):

    # Set connection timeout
    socket.setdefaulttimeout(0.001)

    print('*Target - {0}: Full scan results:*'.format(str(target)))
    # Scan one host
    if target_is_net is False:
        scan_ports(str(target))
    # Scan multiple hosts in network
    else:
        # RANGE not specified
        if args.range is None:
            for host in target.hosts():
                scan_ports(str(host))
        # RANGE specified
        else:
            # Split CIDR notation into two vars
            network,prefix = str(target).split('/')
            # Range is supported only for /24 subnets
            if int(prefix) == 24:
                try:
                    start,end = args.range.split(':')
                except ValueError:
                    print('RANGE not recognized.')
                    exit(1)
                # Convert network var into list so that I can change the last octet when
                # used with 'range' var
                octets = network.split('.')
                for i in range(int(start),int(end)+1):
                    octets[3] = str(i)
                    scan_ports('.'.join(octets))
            else:
                print('Error: RANGE can be used with /24 subnet only. Exiting.')


# FUNCTION dump_db(filename, db): Dump the DB stored in 'db' dict var into 'filename'
#   stored in /tmp
# RETURNS:

def dump_db(filename, db):

        f = open(filename, 'w')
        f.write(str(db))
        f.close()


# FUNCTION read_db(filename, db): Read file 'filename' and store its contents in 'db'.
#   If the 'filename' doesn't exist or cannot be read, initialize 'db' with dummy record.
# RETRUNS: DB (dict var)
from pathlib import Path
from ast import literal_eval

def read_db(filename):

    # If the file exists
    if Path(filename).is_file():
        f = open(filename, 'r')
        line = f.readline()
        # Convert the line read from the file into dictionary format and return it
        return literal_eval(line)
    else:
        return {'dummy': []}


########
# Main #
########

# Description for '-h' parameter
parser = argparse.ArgumentParser(description='''The scanner utility is used to do port
                                 scan of devices on the network. The 'target' can be
                                 specified as sinle IPv4 IP address or subnet in CIDR
                                 format. If used with /24 subnet target, it is possible
                                 to further limit devices to be scanned by using the
                                 'range' parameter.''')

# Add positional arguments
parser.add_argument('target', help='specify the target to scan')
# Add optional arguments
parser.add_argument('-r', '--range', help='''specify a range to scan (last octet of IP
                                     addr), e.g. 10:20 for x.x.x.20 - x.x.x.30''')
# Get arguments from command line
args = parser.parse_args()

# Create 'database/dict' to store scan results and populate it
db_file = '/tmp/scanner.db'
scan_db  = read_db(db_file)

# Scan target is host by default
target_is_net = False
# Get target in correct format
target = get_target()
if target is not False:
    do_scan(target)
    # Dump DB to file
    dump_db(db_file, scan_db)
else:
    print('Invalid IPv4 host or network address specified:', args.target)
