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

class SimplePingTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {'inNamespace':True}
        #http_link_config = {'bw': 1}
        #video_link_config = {'bw': 10}

        switch_link_config = {'bw': 10}
        host_link_config = {}

        self.addHost('h1', **hconfig)
        self.addHost('h2', **hconfig)

        sconfig = {'dpid': "%016x" % 1}
        self.addSwitch('s1', **sconfig)

        sconfig = {'dpid': "%016x" % 2}
        self.addSwitch('s2', **sconfig)

        sconfig = {'dpid': "%016x" % 3}
        self.addSwitch('s3', **sconfig)

        # Add switch links
        # Specified to the port numbers to avoid any port number consistency issue

        self.addLink('h1', 's1', port1=1, port2=1, **host_link_config)
        self.addLink('h2', 's3', port1=1, port2=1, **host_link_config)

        self.addLink('s1', 's2', port1=2, port2=1, **switch_link_config)
        self.addLink('s2', 's3', port1=2, port2=2, **switch_link_config)

        info('\n*** printing and validating the ports running on each interface\n')
        


def startNetwork():
    info('** Creating Dionysus testbed network topology\n')
    topo = SimplePingTopo()
    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='127.0.0.1'),
                  listenPort=6633, autoSetMacs=True)

    info('** Starting the network\n')
    net.start()


    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    if net is not None:
        info('** Tearing down testbed network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
