#!/usr/bin/evn python                                                                            
                                 
#inclusão das bibliotecas necessárias no mininet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, Host, Node
from mininet.nodelib import NAT

#Topo

#  -  s2 -     -  T1
#s1         H - T2
#  -  s3 -     -  T3


#criação da classe que contém a tpopologia
class Custom(Topo):

    #aqui, o construtor da nossa classe, chama o construtor de topologias do mininet, para construir a rede
    def __init__(self):
        Topo.__init__(self)

        #declaracao da subrede dos 'T'
        t1 = self.addHost('temp1', ip='10.1.1.1')
        t2 = self.addHost('temp2', ip='10.1.1.2')
        t3 = self.addHost('temp3', ip='10.1.1.3')

        #declaracao da subrede dos 'Switches'
        h1 = self.addHost('switch1', ip='10.1.2.1')
        h2 = self.addHost('switch2', ip='10.1.2.2')
        h3 = self.addHost('switch3', ip='10.1.2.3')

        controller = self.addHost('control', ip='10.1.1.4')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        #conecta host com seu switch
        self.addLink(s3, controller)
        self.addLink(s1, s3)
        self.addLink(s2, s3)       

        #criação dos links entre os 'Switches'
        self.addLink(s1, h1)
        self.addLink(s1, h2)
        self.addLink(s1, h3)
        
        #criação dos links entre os 'T'
        self.addLink(s2, t1)
        self.addLink(s2, t2)
        self.addLink(s2, t3)

        #criação dos links entre os 'T' e o Host 'H'


#dicionário da topologia, utilizado como parâmetro no momento da execução no ambinente mininet
topos = { 'custom': ( lambda: Custom() ) }
