from socket import *
from functools import partial

host = 'localhost'
port = 9999


def send_file(filename):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    with open(filename, 'rb') as f:
        for pcap_chunk in iter(partial(f.read, 1024), ''):
            print(pcap_chunk)
            s.send(pcap_chunk)

if __name__ == '__main__':
    send_file('pcap/output1.pcap')
