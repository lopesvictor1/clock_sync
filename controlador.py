import socket
import datetime
import time
import ssl
import random
import threading
import zmq
import json

#  -  s2 -     -  T1
#s1         H - T2
#  -  s3 -     -  T3

#H

HOST = '10.1.1.4'  # IP padrão do Host Local
PORT = 65431        # Porta escolhida para conexão

GLOBAL_TIME = 0 #tempo do controlador
valid = False #diz se o tempo do controlador esta atualizado
count = 0



def count_time(f):
    global valid
    global GLOBAL_TIME
    global count
    valid = False
    count = 0
    GLOBAL_TIME = 0
    while(True):
        print("Local Time: {}".format(GLOBAL_TIME), file=f, flush=True)
        if count > 8:
            valid = False
            count = 0
        GLOBAL_TIME += 6
        count += 1
        time.sleep(1)
    


def return_local_time(zmq_sock, f, data, identity):
    global GLOBAL_TIME
    a = int(data)
    x = GLOBAL_TIME
    time.sleep(2)
    y = GLOBAL_TIME
    times = [a, x, y]
    json_times = json.dumps(times)
    print(json_times)
    zmq_sock.send(identity, zmq.SNDMORE)
    zmq_sock.send(json_times.encode("utf-8"))




#funcao principal do sistema
def main():
    print("testando...................")
    f = open('controlador.txt', 'w+')
    threading.Thread(target=count_time, args=(f,)).start()
    TIME_SUM = 0

    context = zmq.Context()
    zmq_sock = context.socket(zmq.ROUTER)
    zmq_sock.bind("tcp://{}:{}".format(HOST, PORT))
    poll = zmq.Poller()
    poll.register(zmq_sock, zmq.POLLIN)
    while True:
        identity = zmq_sock.recv()
        data = zmq_sock.recv()
        print("Recebido dados: " + data.decode("utf-8") + "\n")
        thread = threading.Thread(target=return_local_time, args=(zmq_sock, f, data, identity)).start()
                        

if __name__ == "__main__":
    main()