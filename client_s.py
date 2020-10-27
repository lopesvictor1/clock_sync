import socket
import sys
import time
import threading
import random

HOST = '127.0.0.1'
PORT = 65431

LOCAL_TIME = 0



comandos = ["!time"]
clocks = [1, 2, 3, 4, 5]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    value = clocks[random.randint(0, len(clocks)-1)]
    s.connect((HOST, PORT))    
    count = 0
    LOCAL_TIME = 0

    s.sendall("!time".encode("utf-8"))
    data = s.recv(2048)
    LOCAL_TIME = int(data.decode("utf-8"))

    print("Clock: {}".format(value))
    while(True):
        if count >= 5:
            count = 0  
            s.sendall("!time".encode("utf-8"))
            data = s.recv(2048)
            LOCAL_TIME = int(data.decode("utf-8"))
        LOCAL_TIME += value   
        count += 1
        print("Local time: {}".format(LOCAL_TIME))
        time.sleep(1)
