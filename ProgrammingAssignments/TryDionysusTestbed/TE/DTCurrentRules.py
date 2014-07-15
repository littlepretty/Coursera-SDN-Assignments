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
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()

h1 = EthAddr("00-00-00-00-00-01")
h2 = EthAddr("00-00-00-00-00-02")
h3 = EthAddr("00-00-00-00-00-03")
h4 = EthAddr("00-00-00-00-00-04")
h5 = EthAddr("00-00-00-00-00-05")
h6 = EthAddr("00-00-00-00-00-06")
h7 = EthAddr("00-00-00-00-00-07")
h8 = EthAddr("00-00-00-00-00-08")
broadcast = EthAddr("ff-ff-ff-ff-ff-ff")



class DTCurrentRules (EventMixin):

	def __init__(self):
		self.listenTo(core.openflow)
		core.openflow_discovery.addListeners(self)

	
	def install_fwdrule(self, event, packet, outport):
		msg = of.ofp_flow_mod()
		msg.idle_timeout = 100
		msg.hard_timeout = 60

		msg.match = of.ofp_match.from_packet(packet, event.port)
		
		msg.actions.append(of.ofp_action_output(port = outport))
		
		msg.data = event.ofp
		
		msg.in_port = event.port
		
		event.connection.send(msg)            

	def flood (self, event, message = None):
		msg = of.ofp_packet_out()
		
		msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
		
		msg.data = event.ofp
		
		msg.in_port = event.port
		
		event.connection.send(msg)

	def installRuleForSW1(self, event):
		packet = event.parsed
		# F1
		if packet.dst == broadcast:
			self.flood(event)

		if packet.src == h1 and packet.dst == h6:
			port = 1
			self.install_fwdrule(event, packet, port)

		if packet.src == h6 and packet.dst == h1:
			port = 3
			self.install_fwdrule(event, packet, port)

	def installRuleForSW2(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F4
		if packet.src == h5 and packet.dst == h7:
			port = 3
			self.install_fwdrule(event, packet, port)

		if packet.src == h7 and packet.dst == h5:
			port = 1
			self.install_fwdrule(event, packet, port)

		# F7
		if packet.src == h2 and packet.dst == h5:
			port = 2
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h2:
			port = 4
			self.install_fwdrule(event, packet, port)

	def installRuleForSW3(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F2
		if packet.src == h3 and packet.dst == h5:
			port = 4
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h3:
			port = 5
			self.install_fwdrule(event, packet, port)

		# F6
		if packet.src == h8 and packet.dst == h6:
			port = 3
			self.install_fwdrule(event, packet, port)
		if packet.src == h6 and packet.dst == h8:
			port = 2
			self.install_fwdrule(event, packet, port)


	def installRuleForSW4(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F2
		if packet.src == h3 and packet.dst == h5:
			port = 2
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h3:
			port = 1
			self.install_fwdrule(event, packet, port)
		# F3
		if packet.src == h4 and packet.dst == h7:
			port = 4
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h4:
			port = 5
			self.install_fwdrule(event, packet, port)
		# F7
		if packet.src == h2 and packet.dst == h5:
			port = 2
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h2:
			port = 3
			self.install_fwdrule(event, packet, port)

	def installRuleForSW5(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F2
		if packet.src == h3 and packet.dst == h5:
			port = 5
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h3:
			port = 2
			self.install_fwdrule(event, packet, port)

		# F4
		if packet.src == h5 and packet.dst == h7:
			port = 3
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h5:
			port = 5
			self.install_fwdrule(event, packet, port)

		# F5
		if packet.src == h6 and packet.dst == h7:
			port = 4
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h6:
			port = 1
			self.install_fwdrule(event, packet, port)
		# F7
		if packet.src == h2 and packet.dst == h5:
			port = 5
			self.install_fwdrule(event, packet, port)
		if packet.src == h5 and packet.dst == h2:
			port = 2
			self.install_fwdrule(event, packet, port)


	def installRuleForSW6(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F1
		if packet.src == h1 and packet.dst == h6:
			port = 4
			self.install_fwdrule(event, packet, port)
		if packet.src == h6 and packet.dst == h1:
			port = 1
			self.install_fwdrule(event, packet, port)
		# F5
		if packet.src == h6 and packet.dst == h7:
			port = 3
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h6:
			port = 4
			self.install_fwdrule(event, packet, port)
		# F6
		if packet.src == h8 and packet.dst == h6:
			port = 4
			self.install_fwdrule(event, packet, port)
		if packet.src == h6 and packet.dst == h8:
			port = 2
			self.install_fwdrule(event, packet, port)

	def installRuleForSW7(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F3
		if packet.src == h4 and packet.dst == h7:
			port = 5
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h4:
			port = 3
			self.install_fwdrule(event, packet, port)

		# F4
		if packet.src == h5 and packet.dst == h7:
			port = 5
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h5:
			port = 2
			self.install_fwdrule(event, packet, port)
		# F5
		if packet.src == h6 and packet.dst == h7:
			port = 5
			self.install_fwdrule(event, packet, port)
		if packet.src == h7 and packet.dst == h6:
			port = 4
			self.install_fwdrule(event, packet, port)

	def installRuleForSW8(self, event):
		packet = event.parsed

		if packet.dst == broadcast:
			self.flood(event)

		# F1
		if packet.src == h1 and packet.dst == h6:
			port = 3
			self.install_fwdrule(event, packet, port)

		if packet.src == h6 and packet.dst == h1:
			port = 1
			self.install_fwdrule(event, packet, port)
		# F6
		if packet.src == h8 and packet.dst == h6:
			port = 2
			self.install_fwdrule(event, packet, port)
		if packet.src == h6 and packet.dst == h8:
			port = 5
			self.install_fwdrule(event, packet, port)


	def installForwardRuleByDPID(self, event):

		dpid = dpid_to_str(event.dpid)

		if dpid == '00-00-00-00-00-01':
			self.installRuleForSW1(event)
		if dpid == '00-00-00-00-00-02':
			self.installRuleForSW2(event)
		if dpid == '00-00-00-00-00-03':
			self.installRuleForSW3(event)    	
		if dpid == '00-00-00-00-00-04':
			self.installRuleForSW4(event)
		if dpid == '00-00-00-00-00-05':
			self.installRuleForSW5(event)
		if dpid == '00-00-00-00-00-06':
			self.installRuleForSW6(event)
		if dpid == '00-00-00-00-00-07':
			self.installRuleForSW7(event)
		if dpid == '00-00-00-00-00-08':
			self.installRuleForSW8(event)
		else:
			log.debug("No rule has been installed at switch %s", dpid)


	def _handle_PacketIn(self, event):

		packet = event.parsed
		self.installForwardRuleByDPID(event)
		print "At switch ", event.dpid, " packet dump: ", packet.dump()



	def _handle_ConnectionUp(self, event):
		dpid = dpid_to_str(event.dpid)
		log.debug("Switch %s has come up.", dpid)



def launch():
	# Run spanning tree so that we can deal with topologies with loops
	pox.openflow.discovery.launch()
	pox.openflow.spanning_tree.launch()

	'''
	Starting the Dionysus current rules module
	'''
	core.registerNew(DTCurrentRules)
