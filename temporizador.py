import socket
import sys
import time
import threading
import random
import argparse
import zmq

HOST = '10.1.1.4'
PORT = 65431
DEFAULT_IP = '1'

LOCAL_TIME = 0
clocks = [7, 8, 9, 10]


def count_time(value):
    print("Value " + str(value) + "\n")
    global LOCAL_TIME
    while True:    
        print("Local Time: {}, clock: {}\n".format(LOCAL_TIME, value))
        LOCAL_TIME += value
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Time Calculator")
    help_msg = "Temporizador"
    parser.add_argument("--ip", "-i", help=help_msg, default=DEFAULT_IP, type=str)

    #parse args
    args = parser.parse_args()

    f = open('temporizador{}.txt'.format(args.ip), 'w')
    host = "10.1.1." + args.ip
    port = 65532
    value = clocks[random.randint(0, len(clocks)-1)]                       
    x = threading.Thread( target=count_time, args=(value,) ).start()



    context = zmq.Context()
    zmq_sock = context.socket(zmq.REP)
    zmq_sock.bind("tcp://{}:{}".format(host, port))
    print("Aguardando conexão...")
    while True:
        data = zmq_sock.recv()
        if data == b'!time':
            print("Recebido comando: {}.".format(data.decode("utf-8")), file=f, flush=True)
            time = str(LOCAL_TIME)
            print("Enviando mensagem: {}.".format(time), file=f, flush=True)
            zmq_sock.send(time.encode("utf-8"))
        else:
            print("Error receiving message.")

            




if __name__ == "__main__":
    main()