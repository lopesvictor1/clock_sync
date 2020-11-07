import socket
import sys
import time
import threading
import random
import argparse

HOST = '10.1.1.4'
PORT = 65431
DEFAULT_IP = '1'

LOCAL_TIME = 0
clocks = [6, 7, 8, 9, 10]


def count_time(value):
    LOCAL_TIME = 0
    while(True):    
        GLOBAL_TIME += value
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Time Calculator")
    help_msg = "ESTORO DE FACAO"
    parser.add_argument("--ip", "-i", help=help_msg, default=DEFAULT_IP, type=str)

    #parse args
    args = parser.parse_args()

    host = "10.1.1." + args.ip
    port = 65532
    value = clocks[random.randint(0, len(clocks)-1)]                       
    threading.Thread(target=count_time, args=(value,))


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:     
        s.bind((host, port)) #porta do controlador conectada com os clientes (h1,h2,h3)                                                               
        print("Aguardando Conexão...") 
        while True:                                                                          
            s.listen()                                                                       
            conn, addr = s.accept()
            print('Estabelecida conexão com {}.'.format(addr))
            data = s.recv(2048)
            if data ==  b'!time':
                s.sendall(str(LOCAL_TIME).encode("utf-8"))
            else:
                print("Error receiving message from {}".format(addr))
            




if __name__ == "__main__":
    main()