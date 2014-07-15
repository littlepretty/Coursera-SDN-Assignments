'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()

h1 = EthAddr("00-00-00-00-00-01")
h2 = EthAddr("00-00-00-00-00-02")
broadcast = EthAddr("ff-ff-ff-ff-ff-ff")


class SimplePingController (EventMixin):

	def __init__(self):
		self.listenTo(core.openflow)
		core.openflow_discovery.addListeners(self)

	def flood (self, event, message = None):
		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
		msg.data = event.ofp
		msg.in_port = event.port
		event.connection.send(msg)

	
	def install_fwdrule(self, event, outport):
		packet = event.parsed

		msg = of.ofp_flow_mod()
		msg.priority = 42
		msg.idle_timeout = 1000
		msg.hard_timeout = 6000

		msg.match = of.ofp_match.from_packet(packet, event.port)
		msg.in_port = event.port
		msg.data = event.ofp

		msg.actions.append(of.ofp_action_output(port = outport))
		event.connection.send(msg)

	"""	
	def installRuleForSW1(self, event):
		print "1 Install Rule for Switch ", event.dpid
		# F1
		src = EthAddr("00:00:00:00:00:01")
		dst = EthAddr("00:00:00:00:00:02")
		port = 2
		self.install_fwdrule(event, src, dst, port)
		src = EthAddr("00:00:00:00:00:02") 
		dst = EthAddr("00:00:00:00:00:01")
		port = 1
		self.install_fwdrule(event, src, dst, port)

	def installRuleForSW2(self, event):
		print "2 Install Rule for Switch ", event.dpid
		# F4
		src1 = EthAddr("00:00:00:00:00:01") 
		dst1 = EthAddr("00:00:00:00:00:02")
		port1 = 9000
		self.install_fwdrule(event, src1, dst1, port1)

		src2 = EthAddr("00:00:00:00:00:02") 
		dst2 = EthAddr("00:00:00:00:00:01")
		port2 = 9000
		self.install_fwdrule(event, src2, dst2, port2)

	def installRuleForSW3(self, event):
		print "3 Install Rule for Switch ", event.dpid
		# F2
		src = EthAddr("00:00:00:00:00:01") 
		dst = EthAddr("00:00:00:00:00:02")
		port = 1
		self.install_fwdrule(event, src, dst, port)

		src = EthAddr("00:00:00:00:00:02") 
		dst = EthAddr("00:00:00:00:00:01")
		port = 2
		self.install_fwdrule(event, src, dst, port)
	
	"""
	def installRuleForSW1(self, event):
		packet = event.parsed
		ip = packet.find('ipv4')

		log.debug("1 Install Rule for Switch %d", event.dpid)
		# F1
		if packet.src == h1 and packet.dst == h2:
			port = 2
			self.install_fwdrule(event, port)

		if packet.src == h2 and packet.dst == h1:
			port = 1
			self.install_fwdrule(event, port)

		if packet.dst == broadcast:
			self.flood(event)

	def installRuleForSW2(self, event):
		packet = event.parsed
		ip = packet.find('ipv4')

		log.debug("2 Install Rule for Switch %d", event.dpid)
		# F4
		if packet.src == h1 and packet.dst == h2:
			port = 2
			self.install_fwdrule(event, port)

		if packet.src == h2 and packet.dst == h1:
			port = 1
			self.install_fwdrule(event, port)

		if packet.dst == broadcast:
			self.flood(event)


	def installRuleForSW3(self, event):
		log.debug("3 Install Rule for Switch %d", event.dpid)
		# F2
		packet = event.parsed
		ip = packet.find('ipv4')

		if packet.src == h1 and packet.dst == h2:
			port = 1
			self.install_fwdrule(event, port)

		if packet.src == h2 and packet.dst == h1:
			port = 2
			self.install_fwdrule(event, port)

		if packet.dst == broadcast:
			self.flood(event)
	

	def installForwardRuleByDPID(self, event):
		dpid = dpid_to_str(event.dpid)

		if dpid == '00-00-00-00-00-01':
			self.installRuleForSW1(event)
		elif dpid == '00-00-00-00-00-02':
			self.installRuleForSW2(event)
		elif dpid == '00-00-00-00-00-03':
			self.installRuleForSW3(event)   	
		else:
			print "No rule has been installed at switch ", event.dpid, " ", dpid


	def _handle_PacketIn(self, event):
		packet = event.parsed

		self.installForwardRuleByDPID(event)

		print "At switch ", event.dpid, " packet dump: ", packet.dump()

		# if packet.type == IPV4:
		# 	print "IPV4 part ", packet.ipv4
		# 	print "Packet from ", packet.ipv4.srcip, " to ", packet.ipv4.dstip
		# else:
		# 	print "Packet from ", packet.src, " to ", packet.dst


	def _handle_ConnectionUp(self, event):
		log.debug("Switch %016x has come up.", event.dpid)
		# self.installForwardRuleByDPID(event)



def launch():
	pox.openflow.discovery.launch()
	core.registerNew(SimplePingController)




