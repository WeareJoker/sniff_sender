from socket import *
from functools import partial

host = 'localhost'
port = 9999


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(2)
    client, addr = s.accept()

    f = open('result.pcap', 'w')

    for pcap_chunk in iter(partial(client.recv, 1024), ''):
        print(pcap_chunk)
        f.write(pcap_chunk)


if __name__ == '__main__':
    main()
