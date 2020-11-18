#!/usr/bin/python3
# -*- coding: utf-8 -*-

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
    def __init__(self, hasDelay):
        Topo.__init__(self)
        #logging.info("Criando Topologia...\n")
        print("Criando topologia...\n")
        link_parametros = {'delay' : '5ms'}

        #logging.info("Adicionando Switches...\n")
        print("Adicionando Switches...\n")

        self.addHost('client1', ip='10.1.2.1', defaultRoute= None)
        self.addHost('client2', ip='10.1.2.2', defaultRoute= None)
        self.addHost('client3', ip='10.1.2.3', defaultRoute= None)

        #logging.info("Adicionando Controlador...\n")
        print("Adicionando Controlador...\n")
        self.addHost('control', cls=Host, ip='10.1.1.4', defaultRoute= None)

        self.addSwitch('s1')
        self.addSwitch('s3')
        
        print("Criando links...\n")
        self.addLink('client1', 's1', cls=TCLink, **link_parametros)
        self.addLink('client2', 's1', cls=TCLink, **link_parametros)
        if hasDelay == True:
            link_parametros = {'delay' : '500ms'}
        self.addLink('client3', 's1', cls=TCLink, **link_parametros)


        self.addLink('control', 's3', cls=TCLink, **link_parametros)
        self.addLink('s1', 's3', cls=TCLink, **link_parametros)



def main():

    parser = argparse.ArgumentParser(description="Orquestrador")
    help_msg = "Orquestrador"
    parser.add_argument("--mode", "-m", help=help_msg, default=DEFAULT_MODE, type=str)
    args = parser.parse_args()

    os.system('sudo mn --clean')
    os.system('sudo rm controlador.txt')


    #executando com clock_sync
    if args.mode == 'clock_on':
        os.system('sudo rm switch1_normal.txt')
        os.system('sudo rm switch2_normal.txt')
        os.system('sudo rm switch3_normal.txt')
        topo = CustomTopo(False)

        cmd_control = 'python3 controlador.py &'
        cmd_s1 = 'python3 switch.py -n 1 &'
        cmd_s2 = 'python3 switch.py -n 2 &'
        cmd_s3 = 'python3 switch.py -n 3 &'


    elif args.mode == 'clock_off':
        os.system('sudo rm switch1_noclocksync.txt')
        os.system('sudo rm switch2_noclocksync.txt')
        os.system('sudo rm switch3_noclocksync.txt')
        topo = CustomTopo(False)

        cmd_control = 'python3 controlador.py &'
        cmd_s1 = 'python3 switch.py -n 1 -m clock_off &'
        cmd_s2 = 'python3 switch.py -n 2 -m clock_off &'
        cmd_s3 = 'python3 switch.py -n 3 -m clock_off &'
    elif args.mode == 'delay':
        os.system('sudo rm switch1_delay.txt')
        os.system('sudo rm switch2_delay.txt')
        os.system('sudo rm switch3_delay.txt')  
        topo = CustomTopo(True)

        cmd_control = 'python3 controlador.py &'
        cmd_s1 = 'python3 switch.py -n 1 -m delay &'
        cmd_s2 = 'python3 switch.py -n 2 -m delay &'
        cmd_s3 = 'python3 switch.py -n 3 -m delay &'
    else:
        print("Modo inválido, por favor tentar -m = 'clock_on', 'clock_off' ou 'delay'")



    net = Mininet(topo=topo, host=Host, link=TCLink)
    net.start()

    s1 = net.getNodeByName('client1')
    s2 = net.getNodeByName('client2')
    s3 = net.getNodeByName('client3')    
    control = net.getNodeByName('control')

    teste=control.cmd(cmd_control)
    time.sleep(2)

    s1.cmd(cmd_s1)
    s2.cmd(cmd_s2)
    s3.cmd(cmd_s3)

    time.sleep(60)

    net.stop()
    

if __name__ == "__main__":
    sys.exit(main())

