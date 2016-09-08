from socket import *
from celery import Celery
from functools import partial

app = Celery('send_client', backend='amqp', broker='amqp://guest@localhost//')

host = 'localhost'
port = 9999


@app.task
def send_file(filename):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    with open(filename, 'rb') as f:
        for pcap_chunk in iter(partial(f.read, 1024), ''):
            print(pcap_chunk)
            s.send(pcap_chunk)


if __name__ == '__main__':
    result = send_file.delay('pcap/output1.pcap')
    print(result.status)
