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




def count_time():
    valid = False
    count = 0
    LOCAL_TIME = 0
    while(True):
        if count > 20:
            valid = False
            count = 0
        x = random.randint(0, 2)
        LOCAL_TIME += clocks[x]   
        count += 1
        print("Local time: %d", LOCAL_TIME)
        time.sleep(1)


threading.Thread(target=count_time,).start()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))    
    s.sendall(comandos[0].encode("utf-8"))