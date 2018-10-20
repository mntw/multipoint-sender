#!/usr/bin/python2.7
from multiprocessing.dummy import Pool as ThreadPool
from sys import stdin, exit, argv
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET
#from io import IOBase # Python3 object for isinstance(fd, IOBase)
import argparse, time, tqdm

parser = argparse.ArgumentParser(description='Simple multipoint transmission.', prog='smt')

source_group = parser.add_mutually_exclusive_group(required=True)
source_group.add_argument('-sf', '--sfile', help='path to source file', metavar="FILE NAME", type=str, default=0)
source_group.add_argument('-stdi', '--std-input', help='use standard input as input (pipe before s required)', action='store_true' )
source_group.add_argument("-s", '--server', action = 'store_true', help='use input socket as input')

destination_group = parser.add_argument_group(title='possible actions (at least one is required)')
destination_group.add_argument('-df', '--dfile', help='path to destination file', metavar="FILE NAME", type=str, default=None)
destination_group.add_argument('-H', '--hosts', nargs='+', metavar='IP:PORT', type=str, help='destination hosts')

parser.add_argument('-m', '--mss', help='max segment size', metavar="MSS", type=int, default=8972)
parser.add_argument('-p', '--port', help='Port address to receive data from remote host', metavar="PORT", type=int, default=8880)
parser.add_argument('-fs', '--filesize', help='Size of transmitted data', metavar="MB", type=int, default=0)
parser.add_argument('-st', '--statistics', help='Show statistics and progress', action='store_true')


if len(argv) == 1:
    parser.print_help()
    exit(1)
    
args = parser.parse_args()

if not args.dfile and not args.hosts:
     parser.error ('Either --hosts or --dfile is required.')

def host_parser(ahosts):
    if not ahosts: return []
    try:
	return [(ip, int(port)) for ip, port in [i.split(':') for i in ahosts]]
    except Exception as e:
	print e, '\nWrong input hosts format.'
	exit(0)

def create_socket(ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))
    return sock

def destroy_sockets(sockets):
	[i.close() for i in sockets]

def send(sock, data):
    if isinstance(sock, socket):
        sock.send(data)
    elif isinstance(sock, file):
	sock.write(data)

class Source():
    def __init__(self, isSocket = False, port=None, filename = None):
        self.port = port
	self.isSocket = isSocket 
	self.socket = None
	self.filename = filename
	self.fd = None
	self.data = True
        self.received_size = 0
    def accept_connection(self):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	sock.bind(('0.0.0.0', self.port))
	sock.listen(1)
	conn, addr = sock.accept()
	sock.close()
	return conn 
    def file_open(self, name):
        try:
            return open(name, 'rb') if name else stdin
        except Exception as e:
            print(e,'\nCant open file %s' % str(name))
            exit(0)
    def create(self):
        if self.isSocket:
            self.socket = self.accept_connection()
        else:
	    self.fd = self.file_open(self.filename) 
	return self
    def Read(self, size):
        self.data = self.socket.recv(size) if self.isSocket else self.fd.read(size)
        ldata = len(self.data)
        self.received_size += ldata
        return ldata
    def getData(self):
	return self.data
    def close(self):
        self.socket.close() if self.isSocket else self.fd.close()


addrs = host_parser(args.hosts)
source = Source(isSocket=args.server, port=args.port, filename=args.sfile).create()
sockets = [create_socket(ip, port) for ip,port in addrs]

if args.dfile:
    fd_write = open(args.dfile, 'wb')
    sockets.append(fd_write)

pool = ThreadPool(processes = len(sockets))

if (args.filesize and args.statistics):
    pbar = tqdm.tqdm(total = args.filesize * 1e3 * 1024, leave=False, unit='B', unit_scale=1, dynamic_ncols=True, ascii=0)

t1 = time.time() if args.statistics else 0
while source.getData():
    length = source.Read(args.mss)
    results = pool.map(lambda x : send(x, source.getData()), sockets)
    pbar.update(length) if (args.filesize and args.statistics) else None

t2 = time.time() if args.statistics else 0

pool.close()
pool.join()
destroy_sockets(sockets)
source.close()
if args.statistics:
    print '\nAmount of transmitted data: %d MB' % (source.received_size / 1e3 / 1024) 
    print 'Average datarate: %f Mbps' % (source.received_size * 8.0 / 1e3 /  1024 / (t2-t1))
