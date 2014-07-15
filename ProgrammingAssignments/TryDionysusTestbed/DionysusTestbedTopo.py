#!/usr/bin/python

"""
Start off Dionysus Testbed Topology:
-- Author: YJQ

"""

import inspect
import os
import atexit
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.topo import SingleSwitchTopo
from mininet.node import RemoteController


net = None

class DionysusTestbedTopo(Topo):
    # credit: https://github.com/onstutorial/onstutorial/blob/master/flowvisor_scripts/flowvisor_topo.py
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {'inNamespace':True}

        switch_link_config = {'bw': 10}
        host_link_config = {}

        # Create switch nodes
        for i in range(8):
            sconfig = {'dpid': "%016x" % (i+1)}
            self.addSwitch('s%d' % (i+1), **sconfig)
        # Create host nodes
        for i in range(8):
            self.addHost('h%d' % (i+1), **hconfig)

        # Add switch links
        # Specified to the port numbers to avoid any port number consistency issue
        self.addLink('h1', 's1', port1=1, port2=0, **host_link_config)
        self.addLink('h2', 's2', port1=1, port2=0, **host_link_config)
        self.addLink('h3', 's3', port1=1, port2=0, **host_link_config)
        self.addLink('h4', 's4', port1=1, port2=0, **host_link_config)
        self.addLink('h5', 's5', port1=1, port2=0, **host_link_config)
        self.addLink('h6', 's6', port1=1, port2=0, **host_link_config)
        self.addLink('h7', 's7', port1=1, port2=0, **host_link_config)
        self.addLink('h8', 's8', port1=1, port2=0, **host_link_config)

        self.addLink('s1', 's8', port1=1, port2=1, **switch_link_config)
        self.addLink('s1', 's3', port1=2, port2=1, **switch_link_config)

        self.addLink('s2', 's5', port1=1, port2=3, **switch_link_config)
        self.addLink('s2', 's4', port1=2, port2=3, **switch_link_config)
        self.addLink('s2', 's7', port1=3, port2=2, **switch_link_config)

        self.addLink('s3', 's8', port1=2, port2=2, **switch_link_config)
        self.addLink('s3', 's6', port1=3, port2=2, **switch_link_config)
        self.addLink('s3', 's4', port1=4, port2=1, **switch_link_config)

        self.addLink('s4', 's5', port1=2, port2=2, **switch_link_config)
        self.addLink('s4', 's7', port1=4, port2=3, **switch_link_config)

        self.addLink('s5', 's6', port1=1, port2=3, **switch_link_config)
        self.addLink('s5', 's7', port1=4, port2=4, **switch_link_config)

        self.addLink('s6', 's8', port1=1, port2=3, **switch_link_config)
        
        self.addLink('s7', 's8', port1=1, port2=4, **switch_link_config)
        
        info('\n*** printing and validating the ports running on each interface\n')
        


def startNetwork():
    info('** Creating Dionysus testbed network topology\n')
    topo = DionysusTestbedTopo()
    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='127.0.0.1'),
                  listenPort=6633, autoSetMacs=True)

    info('** Starting the network\n')
    net.start()


    info('** Running CLI\n')


def stopNetwork():
    if net is not None:
        info('** Tearing down testbed network\n')
        net.stop()

def networkReachableTest():

    if net is not None:
        h1 = net.get('h1')
        h2 = net.get('h2')
        h3 = net.get('h3')
        h4 = net.get('h4')
        h5 = net.get('h5')
        h6 = net.get('h6')
        h7 = net.get('h7')
        h8 = net.get('h8')

        info('** Test testbed network with host pings\n')

        outputString = h1.cmd('ping', '-c6', h6.IP())
        print outputString

        outputString = h2.cmd('ping', '-c6', h5.IP())
        print outputString

        outputString = h3.cmd('ping', '-c6', h5.IP())
        print outputString

        outputString = h4.cmd('ping', '-c6', h7.IP())
        print outputString

        outputString = h5.cmd('ping', '-c6', h7.IP())
        print outputString

        outputString = h6.cmd('ping', '-c6', h7.IP())
        print outputString

        outputString = h8.cmd('ping', '-c6', h6.IP())
        print outputString
        CLI(net)


def testbedUpdateRuleValidate():
    startNetwork()
    networkReachableTest()

    
    # stopNetwork()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    
    # startNetwork()
    testbedUpdateRuleValidate()






