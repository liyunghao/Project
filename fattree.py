from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import logging
import os

class fatTree(Topo):
    coreLayer[]
    aggreLayer[]
    edgeLayer[]
    hosts[]
    def __init__(self, k):
        self.podNum = k
        self.coreSwitchNum = (k/2)**2
        self.aggreSwitchNum = (k*k)/2
        self.edgeSwitchNum = (k*k)/2
        self.density = k/2
        self.hostNum = self.edgeSwitchNum * self.density

        Topo.__init__(self)
        self.createTopo()

    def createTopo():
        self.createCoreLayer(self.coreSwitchNum)
        self.createAggreLayer(self.aggreSwitchNum)
        self.createEdgeLayer(self.edgeSwitchNum)
        self.createHost(self.hostNum)

    def _addSwitch(self, NUM, level, switchList):
        for x in range(1, NUM+1):
            prefix = level + '00'
            if x >= int(10):
                prefix = level + '0'
            switchList.append(self.addSwitch(prefix + str(x)))

    def createCoreLayer(self, NUM):
        for x in range(1, NUM+1):
            self._addSwitch(NUM, 'Core', self.coreLayer)
    
    def createAggreLayer(self, NUM):
        for x in range(1, NUM+1):
            self._addSwitch(NUM, 'Aggre', self.aggreLayer)

    def createEdgeLayer(self, NUM):
        for x in range(1, NUM+1):
            self._addSwitch(NUM, 'Edge', self.edgeLayer)   

    def createHost(self, NUM):
        for x in range(1, NUM+1):
            prefix = 'Host00'
            if x >= int(10):
                prefix = 'Host0'
            self.hosts.append(self.addHost(prefix + str(x)))