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
broadcast = EthAddr("ff-ff-ff-ff-ff-ff")

class TopologySlice (EventMixin):


	def __init__(self):
		self.listenTo(core.openflow)
		log.debug("Enabling Slicing Module")






	def _handle_PacketIn(self, event):
		"""Handle packet in messages from the switch to implement above algorithm"""
		
		# flood, but don't install the rule
		def flood (message = None):
			""" Floods the packet """
			msg = of.ofp_packet_out()
			msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
			msg.data = event.ofp
			msg.in_port = event.port
			event.connection.send(msg)

		def drop (message = None):
			""" Drop the packet """
			msg = of.ofp_packet_out()
			msg.data = event.ofp
			msg.in_port = event.port
			event.connection.send(msg)

		def install_fwdrule(event,packet,outport):
			msg = of.ofp_flow_mod()
			msg.idle_timeout = 10
			msg.hard_timeout = 30
			msg.match = of.ofp_match.from_packet(packet, event.port)
			msg.actions.append(of.ofp_action_output(port = outport))
			msg.data = event.ofp
			msg.in_port = event.port
			event.connection.send(msg)

		def forward():

			packet = event.parsed
			tcpp = event.parsed.find('tcp')
			dpid = dpid_to_str(event.dpid)
			

			if packet.dst.is_multicast:
				""" Floods the packet """
				flood()
				log.debug("At %s (input port %d) got multicast packet from %s to %s :", dpid, event.port, packet.src, packet.dst)
				return

			else:
				log.debug("At %s (input port %d) got unicast packet from %s to %s",dpid, event.port, packet.src, packet.dst)

				if dpid == '00-00-00-00-00-02': 
					if packet.dst == h3:
						install_fwdrule(event, packet, 2)

					elif packet.dst == h1:
						install_fwdrule(event, packet, 1)
						
					else:
						drop()
						log.debug("No suitable rule to install for this packet, drop it")

				elif dpid == '00-00-00-00-00-03':
					if packet.dst == h4:
						install_fwdrule(event, packet, 2)
						
					elif packet.dst == h2:
						install_fwdrule(event, packet, 1)
						
					else:
						drop()
						log.debug("No suitable rule to install for this packet, drop it")

				elif dpid == '00-00-00-00-00-01':
					if packet.dst == h4 and packet.src != h1 and packet.src != h3:
						install_fwdrule(event, packet, 2)
					elif packet.dst == h3 and packet.src != h2 and packet.src != h4:
						install_fwdrule(event, packet, 1)
					elif packet.dst == h2 and packet.src != h3 and packet.src != h1:
						install_fwdrule(event, packet, 4)
					elif packet.dst == h1 and packet.src != h4 and packet.src != h2:
						install_fwdrule(event, packet, 3)
					else:
						drop();
						log.debug("No suitable rule to install")

				elif dpid == '00-00-00-00-00-04':
					if packet.dst == h4 and packet.src != h1 and packet.src != h3:
						install_fwdrule(event, packet, 4)
					elif packet.dst == h3 and packet.src != h2 and packet.src != h4:
						install_fwdrule(event, packet, 3)
					elif packet.dst == h2 and packet.src != h3 and packet.src != h1:
						install_fwdrule(event, packet, 2)
					elif packet.dst == h1 and packet.src != h4 and packet.src != h2:
						install_fwdrule(event, packet, 1)
					else:
						drop();
						log.debug("No suitable rule to install")
				else:
					log.debug("Unknown switch dpid")

		forward()


        
	""""This event will be raised each time a switch will connect to the controller"""
	def _handle_ConnectionUp(self, event):
		# Use dpid to differentiate between switches (datapath-id)
		# Each switch has its own flow table. As we'll see in this 
		# example we need to write different rules in different tables.
		dpid = dpidToStr(event.dpid)
		log.debug("Switch %s has come up.", dpid)
		
		""" Add your logic here """
			
def launch():
	# Run spanning tree so that we can deal with topologies with loops
	pox.openflow.discovery.launch()
	pox.openflow.spanning_tree.launch()
	'''
	Starting the Topology Slicing module
	'''
	core.registerNew(TopologySlice)
