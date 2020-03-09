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
            prefix = 


    def createCoreLayer(self, NUM):

