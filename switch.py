import socket
import sys
import time
import threading
import random
import argparse
import zmq
import json

HOST = '10.1.1.4'
PORT = 65431

LOCAL_TIME = 0
valid = True
count = 0

DEFAULT_NUMBER = 10
DEFAULT_MODE = 'clock_on'

comandos = ["!time"]
clocks = [1, 2, 3, 4, 5]
logic_offset = 0



def count_time(value, f):
    global valid
    global LOCAL_TIME
    global logic_offset
    global count
    valid = True
    count = 0
    LOCAL_TIME = 0
    while(True):
        print("Local time: {}".format(LOCAL_TIME), file=f, flush=True)
        print("Local time: {}".format(LOCAL_TIME))
        if count > 5:
            valid = False
            count = 0
        LOCAL_TIME += value + logic_offset
        count += 1
        time.sleep(1)


def update_local_time(data):
    global LOCAL_TIME
    global logic_offset
    data_list = json.loads(data)
    a = data_list[0]
    b = LOCAL_TIME
    x = data_list[1]
    y = data_list[2]


    print ("a={}, b={}, x={}, y={}".format(a,b,x,y))
    logic_offset += ((y - x)//2) - ((b - a)//2)
    print("logic offset: " + str(logic_offset))
    if logic_offset < 1:
        logic_offset = 1
    
    test_time = LOCAL_TIME + ((x-a + y-b) // 2)
    if test_time > LOCAL_TIME:
        LOCAL_TIME += (x-a + y-b) // 2






def main():
    global valid
    global HOST
    global PORT
    parser = argparse.ArgumentParser(description="Time Calculator")
    help_msg = "Switch"
    parser.add_argument("--number", "-n", help=help_msg, default=DEFAULT_NUMBER, type=str)
    parser.add_argument("--mode", "-m", help=help_msg, default=DEFAULT_MODE, type=str)
    args = parser.parse_args()

    execution_type = ""
    if args.mode == 'clock_on':
        execution_type = 'normal'
    elif args.mode == 'clock_off':
        execution_type = 'noclocksync'
    elif args.mode == 'delay':
        execution_type = 'delay'
    f = open('switch{}_{}.txt'.format(args.number, execution_type), 'w')

    value = clocks[random.randint(0, len(clocks)-1)]
    threading.Thread(target=count_time, args=(value, f)).start()
    print("Clock: {}".format(value), file=f, flush=True)

    context = zmq.Context()
    zmq_sock = context.socket(zmq.DEALER)
    identity = args.number.encode("utf-8")
    zmq_sock.setsockopt(zmq.IDENTITY, identity)
    zmq_sock.connect("tcp://{}:{}".format(HOST, PORT))

    while(True):
        if valid == False and args.mode == 'clock_on':
            zmq_sock.send(str(LOCAL_TIME).encode("utf-8"))
            data = zmq_sock.recv()
            print("Recebido valor {}.".format(data.decode("utf-8")), file=f, flush=True)
            update_local_time(data.decode("utf-8"))
            valid = True
            count = 0
                
        



if __name__ == "__main__":
    main()