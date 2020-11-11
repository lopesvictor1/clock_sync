from mininet.topo import Topo
from mininet.node import Host
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI


import sys
import os
import argparse
import logging
import random
import time
import threading
import pexpect

DEFAULT_DELAY_MS = 0
DEFAULT_MODE = 'clock_on'

class CustomTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        #logging.info("Criando Topologia...\n")
        print("Criando topologia...\n")
        link_parametros = {'delay' : '5ms'}

        #logging.info("Adicionando Switches...\n")
        print("Adicionando Switches...\n")

        self.addHost('client1', ip='10.1.2.1', defaultRoute= None)
        self.addHost('client2', ip='10.1.2.2', defaultRoute= None)
        self.addHost('client3', ip='10.1.2.3', defaultRoute= None)

        #logging.info("Adicionando Temporizadores...\n")
        print("Adicionando Temporizadores...\n")
        
        self.addHost('temp1', ip='10.1.1.1', defaultRoute= None)
        self.addHost('temp2', ip='10.1.1.2', defaultRoute= None)
        self.addHost('temp3', ip='10.1.1.3', defaultRoute= None)

        #logging.info("Adicionando Controlador...\n")
        print("Adicionando Controlador...\n")
        self.addHost('control', cls=Host, ip='10.1.1.4', defaultRoute= None)

        self.addSwitch('s1')
        self.addSwitch('s2')
        self.addSwitch('s3')
        
        print("Criando links...\n")
        self.addLink('client1', 's1', cls=TCLink, **link_parametros)
        self.addLink('client2', 's1', cls=TCLink, **link_parametros)
        self.addLink('client3', 's1', cls=TCLink, **link_parametros)
        
        self.addLink('temp1', 's2', cls=TCLink, **link_parametros)
        self.addLink('temp2', 's2', cls=TCLink, **link_parametros)
        self.addLink('temp3', 's2', cls=TCLink, **link_parametros)

        self.addLink('control', 's3', cls=TCLink, **link_parametros)

        self.addLink('s1', 's3', cls=TCLink, **link_parametros)
        self.addLink('s2', 's3', cls=TCLink, **link_parametros)



def main():
    os.system('sudo mn --clean')
    os.system('sudo rm temporizador1.txt')
    os.system('sudo rm temporizador2.txt')
    os.system('sudo rm temporizador3.txt')
    os.system('sudo rm switch1.txt')
    os.system('sudo rm switch2.txt')
    os.system('sudo rm switch3.txt')
    os.system('sudo rm controlador.txt')



    help_msg = "Orquestrador"
    parser = argparse.ArgumentParser(description='Orquestrator...')
    parser.add_argument("--mode", "-m", default=DEFAULT_MODE, type=str)
    args = parser.parse_args()

    topo = CustomTopo()
    net = Mininet(topo=topo, host=Host, link=TCLink)

    net.start()

    cmd_t1 = 'python3 temporizador.py -i 1 &'
    cmd_t2 = 'python3 temporizador.py -i 2 &'
    cmd_t3 = 'python3 temporizador.py -i 3 &'

    cmd_control = 'python3 controlador.py &'
    if args.mode == 'clock_on':
        cmd_s1 = 'python3 switch.py -n 1 &'
        cmd_s2 = 'python3 switch.py -n 2 &'
        cmd_s3 = 'python3 switch.py -n 3 &'
    else:
        cmd_s1 = 'python3 switch.py -n 1 -m clock_off &'
        cmd_s2 = 'python3 switch.py -n 2 -m clock_off &'
        cmd_s3 = 'python3 switch.py -n 3 -m clock_off &'
        
    
    
    t1 = net.getNodeByName('temp1')
    t2 = net.getNodeByName('temp2')
    t3 = net.getNodeByName('temp3')
    s1 = net.getNodeByName('client1')
    s2 = net.getNodeByName('client2')
    s3 = net.getNodeByName('client3')
    
    control = net.getNodeByName('control')

    t1.cmd(cmd_t1)
    #time.sleep(2)
    t2.cmd(cmd_t2)
    #time.sleep(2)
    t3.cmd(cmd_t3)
    time.sleep(2)

    control.cmd(cmd_control)

    time.sleep(2)
    s1.cmd(cmd_s1)
    s2.cmd(cmd_s2)
    s3.cmd(cmd_s3)

    time.sleep(1)
    
    net.stop()
    
    

if __name__ == "__main__":
    sys.exit(main())

