import os
import sys

############################################################
############ Multicast Tree Simulation Analysis ############
############################################################

EVENT = 0
TIME = 1
FROM_NODE = 2
TO_NODE = 3
PKT_TYPE = 4
PKT_SIZE = 5
FLAGS = 6
FID = 7
SRC_ADDR = 8
DST_ADDR = 9
SEQ_NUM = 10
PKT_ID = 11


class Fid:
    cbr = 0
    tcp1 = 1
    tcp2 = 2


class Event:
    receive = 'r'
    enqueue = '+'
    dequeue = '-'
    drop    = 'd'


def try_number(x):
    try:
        f = float(x)
        if round(f) == f:
            f = int(f)
        return f
    except ValueError:
        return x


# read ns trace file and return the data in a 2D array
def read_ns_trace_file(file_path=
                       "/home/hong/Documents/Projects/Networks_HW1/out.tr"):
    with open(file_path) as f:
        lines = f.read().splitlines()
        trace_list = [[try_number(x) for x in line.split()] for line in lines]
    return trace_list


def compute_avg_bandwidth(trace_list, time):
    total_packet_sizes = [0,0,0,0,0,0,0,0]
    for record in trace_list:
        if (record[EVENT] == Event.receive and
                record[TO_NODE] == record[DST_ADDR]):
            total_packet_sizes[record[DST_ADDR]] += record[PKT_SIZE]
    # return each node's bandwidth in Mbps
    return [total*8/1000/1000 / time for total in total_packet_sizes]


def compute_avg_packet_loss_rate(trace_list):
    packets_sent = [0,0,0,0,0,0,0,0]
    packets_dropped = [0,0,0,0,0,0,0,0]
    for record in trace_list:
        if record[EVENT] == Event.enqueue and \
                record[FROM_NODE] == record[SRC_ADDR]:
            packets_sent[record[FROM_NODE]] += 1
        if record[EVENT] == Event.drop:
            packets_dropped[int(record[SRC_ADDR])] += 1
    return [packets_sent, packets_dropped]


if __name__ == "__main__":
    for root, dirs, files in os.walk("./"+sys.argv[1]):
        for name in files:
            if name.endswith(".tr"):
                file_path = os.path.join(root, name)
                trace_list = read_ns_trace_file(file_path)
                bandwidth_of_nodes = compute_avg_bandwidth(trace_list, 10)
                packets_sent_and_lost = compute_avg_packet_loss_rate(trace_list)
                print(file_path)
                print(bandwidth_of_nodes)
                print(packets_sent_and_lost)
                print()
