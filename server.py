import socket
import datetime
import time
import ssl
import random
import threading

#  -  s2 -     -  T1
#s1         H - T2
#  -  s3 -     -  T3

#H

HOST = '127.0.0.1'  # IP padrão do Host Local
PORT = 65431        # Porta escolhida para conexão

GLOBAL_TIME = 0 #tempo do controlador
valid = False #diz se o tempo do controlador esta atualizado
count = 0

t1_ip = '10.1.1.1'
t2_ip = '10.1.1.2'
t3_ip = '10.1.1.3'
t_port = 65532 #porta aberta no lado dos 't'

TIME_SUM = 0
lock = threading.Lock()

#funcao para formatar o mensagem recebida gdo servidor
def format(msg):
    last = len(msg)-1
    bar = False
    for index, x in enumerate(msg, start = 0):
        if(index == 0 or index == 1 or index == last):
            bar = False
        elif(x == '\\'):
            bar = True
            continue
        elif(x == 'n' and bar == True):
            bar = False
            print("")
        else:
            bar = False
            print(x, end = "")



def update_time_switch(conn, addr):
    while True:
        data = conn.recv(1024)
        if len(data) < 1:
            print("error receiving message from host")
            return
        else:
            if valid == True:
                conn.sendall(str(GLOBAL_TIME).encode("utf-8"))
            else:
                update_controller_time()
                conn.sendall(str(GLOBAL_TIME).encode("utf-8"))



#pede para os servidor de sincronização 'T' os valores para fazer a média do tempo no controlador
def update_controller_time():
    #threads = [threading.Thread(target=send_request, args=(t1_ip, t_port)), threading.Thread(target=send_request, args=(t2_ip, t_port)), threading.Thread(target=send_request, args=(t3_ip, t_port))]
    threads = [threading.Thread(target=send_request, args=(t1_ip, t_port))]
    #busca os horários dos servidores 'T' 
    for t in threads:
        t.daemon = True
        t.start()
    for t in threads:
        t.join()
    
    GLOBAL_TIME = TIME_SUM // 3
    valid = True
    count = 0
    TIME_SUM = 0

       
def send_request(ip, port):
    global TIME_SUM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:                        #cria um socket utilizando os protocolos IPv4 e TCP
        s.connect((ip, port))
        s.sendall("!time")
        data = s.recv(1024)
        with lock:
            TIME_SUM += int(format(str(data)))


def count_time():
    valid = False
    count = 0
    GLOBAL_TIME = 0
    while(True):
        if count > 20:
            valid = False
            count = 0
        GLOBAL_TIME += 1
        count += 1
        time.sleep(1)
    



#funcao principal do sistema
def main():
    threading.Thread(target=count_time).start()
    TIME_SUM = 0
    update_controller_time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:                            
        s.bind((HOST, PORT)) #porta do controlador conectada com os clientes (h1,h2,h3)                                                               
        print("Aguardando Conexão...") 
        while True:                                                                          
            s.listen()                                                                       
            conn, addr = s.accept()
            print('Estabelecida conexão com {}.'.format(addr))
            threading.Thread(target=update_time_switch, args=(conn, addr)).start()
                        

if __name__ == "__main__":
    main()