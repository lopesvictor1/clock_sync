# clock_sync

sudo python3 orquestrador.py -m clock_off
clock synchronization algorithm

## Requisitos:
ZMQ:
* pip install pyzmq

Python 3 (&ge; 3.3):
* apt install python3

## How to run:
Execução com sincronização:
* sudo python3 orquestrador.py -m clock_on

Execução sem sincronização:
* sudo python3 orquestrador.py -m clock_off

Execução com delay (em desenvolvimento):
* sudo python3 orquestrador.py -m delay

How it works:
**clock_sync** is a logical clock synchronization algorithm based on NTP. We also consider the following topology for our experiments:

![](topology.png)

O algoritmo funciona da seguinte maneira:
The algorithm works as following:
1. A switch requests the controller, sending its local time (a).
2. The controller receives the request and save its local time at the moment the requisition (x), storing 'a' e 'x' as variables. It then waits 2 seconds (while this value is static, but I can make it passed as a parameter) and saves its local time again (y).
3. The controller answers the switch with a menssage containg 'a', 'x' and 'y'.
4. The switch receives this message and stores the local time value when the message arrives (b).
5. The switch then calculates the clock difference between it and the controller, based on the following equation: ((y - x) // 2) - ((b - a) // 2).
6. In addition, the switch calculates the time offset to "reach" the controller
7. The switch changes its local time based on its clock + logical clock offset calculated in step 5.
8. At a given interval, the switch makes a new request to the controller, recreating steps 1 ~ 7.