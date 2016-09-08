import time
import pcapy

from send_client import send_file

# list all the network devices

pcap_path = './pcap/'

pc = pcapy.open_live(
    "any",  # Just all packet
    8192,  # max bytes
    True,  # i want promiscuous mode.
    100  # 100 milliseconds
)

# make filename list
filename_list = [pcap_path + "output%d.pcap" % i for i in range(1, 2)]

# make celery job list
job_dict = dict()

for filename in filename_list:
    dumper = pc.dump_open(filename)

    # callback for received packets
    def recv_packets(hdr, data):
        # packet = EthDecoder().decode(data)  # <-- When print packet info
        # print(packet)

        dumper.dump(hdr, data)  # Store packet to pcap file


    packet_limit = 20
    pc.loop(packet_limit, recv_packets)  # capture packets

    # Capture count at limit
    print(filename + " Saved!")
    # Call celery task
    job_dict[filename] = send_file.delay(filename)


# Check Job
job_finish = False

while job_finish is not True:
    for job_pcapname in job_dict:
        if job_dict[job_pcapname].status != 'SUCCESS':
            print("Undo!! %s : %s" % (job_pcapname, job_dict[job_pcapname].status))
            time.sleep(10)
            break
    else:
        job_finish = True
