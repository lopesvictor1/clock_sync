import socket
import sys
import time
import threading
import random
import argparse

HOST = '10.1.1.4'
PORT = 65431

LOCAL_TIME = 0

DEFAULT_NUMBER = 1
DEFAULT_MODE = 'clock_on'

comandos = ["!time"]
clocks = [1, 2, 3, 4, 5]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    parser = argparse.ArgumentParser(description="Time Calculator")
    help_msg = "Switch"
    parser.add_argument("--number", "-n", help=help_msg, default=DEFAULT_NUMBER, type=str)
    parser.add_argument("--mode", "-m", help=help_msg, default=DEFAULT_MODE, type=str)
    args = parser.parse_args()
    f = open('switch{}.txt'.format(args.number), 'w')
    value = clocks[random.randint(0, len(clocks)-1)]
    print("Clock: {}".format(value), file=f, flush=True)
    count = 0
    LOCAL_TIME = 0
    if args.mode == 'clock_on':
        s.connect((HOST, PORT))    
        s.sendall("!time".encode("utf-8"))
        data = s.recv(2048)
        LOCAL_TIME = int(data.decode("utf-8"))

    while(True):
        if count >= 5 and args.mode == 'clock_on':
            count = 0  
            s.sendall("!time".encode("utf-8"))
            data = s.recv(2048)
            print("Recebido valor {}.".format(data.decode("utf-8")), file=f, flush= True)
            LOCAL_TIME = int(data.decode("utf-8"))
        LOCAL_TIME += value   
        count += 1
        print("Local time: {}".format(LOCAL_TIME), file=f, flush=True)
        time.sleep(1)
