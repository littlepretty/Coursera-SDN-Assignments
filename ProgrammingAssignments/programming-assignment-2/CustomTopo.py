#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet

from mininet.link import TCLink
from mininet.util import irange, dumpNodeConnections
from mininet.log import setLogLevel


class CustomTopo(Topo):
	"Simple Data Center Topology"

	def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
		# Initialize topo and default options
		Topo.__init__(self, **opts)

		self.fanout = fanout

		# Init Core Layer
		j = 1
		core = self.addSwitch('s%s' % j)
		print core

		# Init Aggregation Layer
		aggregations = []

		for i in irange(1, fanout):
			switch = self.addSwitch('s%s' % j)
			j = j + 1
			self.addLink(core, switch, **linkopts1)
			aggregations.append(switch)
		print aggregations
		
		# Init Edge Layer
		edges = []
		# j = 0
		for agg in aggregations:
			for i in irange(1, fanout):
				k = i+j*fanout
				switch = self.addSwitch('s%s' % j)
				j = j + 1
				self.addLink(agg, switch, **linkopts2)
				edges.append(switch)
			# j = j + 1
		print edges
		
		# Init Host Layer
		hosts = []
		j = 1
		for eg in edges:
			for i in irange(1, fanout):
				k = i+j*fanout
				host = self.addHost('h%s' % j)
				j = j + 1
				self.addLink(eg, host, **linkopts3)
				hosts.append(host)
			# j = j + 1
		print hosts



def perfTest():
	"Create network and run perf test"
	linkopts1 = dict(bw=50, delay='5ms') #, loss=1, max_queue_size=1000, use_htb=True)
	linkopts2 = dict(bw=30, delay='10ms') #, loss=3, max_queue_size=2000, use_htb=True)
	linkopts3 = dict(bw=10, delay='15ms') #, loss=5, max_queue_size=3000, use_htb=True)

	topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=3)
	net = Mininet(topo=topo, link=TCLink)
	net.start()
	
	"""
	print "Dump host connections"
	dumpNodeConnections(net.hosts)
	
	print "Testing network connectivity"
	net.pingAll()
    """
	
	print "Testing bandwidth between h1 and h27"
	h1 = net.get('h1')
	h27 = net.get('h27')
	net.iperf((h1, h27))
	outputString = h1.cmd('ping', '-c6', h27.IP())
	print "output: " + outputString.strip()
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	perfTest()

