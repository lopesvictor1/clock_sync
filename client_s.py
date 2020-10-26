import socket
import sys
import time
import threading
import random

HOST = '127.0.0.1'
PORT = 65431

LOCAL_TIME = 0



comandos = ["!time"]
clocks = [1, 3, 5]




def count_time(value):
    valid = False
    count = 0
    LOCAL_TIME = 0
    print("Clock: {}".format(value))
    while(True):
        if count > 20:
            valid = False
            count = 0
        LOCAL_TIME += value   
        count += 1
        print("Local time: {}".format(LOCAL_TIME))
        time.sleep(1)

value = clocks[random.randint(0, 2)]

threading.Thread(target=count_time, args=(value,)).start()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))    
    s.sendall(comandos[0].encode("utf-8"))