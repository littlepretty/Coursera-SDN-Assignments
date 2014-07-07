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


class DTCurrentRules (EventMixin):

	def __init__(self):
		self.listenTo(core.openflow)
		core.openflow_discovery.addListeners(self)

	"""
	# Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
	self.adjacency = defaultdict(lambda:defaultdict(lambda:None))

	
	def _handle_LinkEvent (self, event):
	l = event.link
	sw1 = dpid_to_str(l.dpid1)
	sw2 = dpid_to_str(l.dpid2)
	log.debug ("link %s[%d] <-> %s[%d]",sw1, l.port1,sw2, l.port2)
	self.adjacency[sw1][sw2] = l.port1
	self.adjacency[sw2][sw1] = l.port2
	"""

	
	def install_fwdrule(self, event, packet, outport):
		msg = of.ofp_flow_mod()
		msg.idle_timeout = 30
		msg.hard_timeout = 60
		msg.match = of.ofp_match.from_packet(packet, event.port)
		msg.actions.append(of.ofp_action_output(port = outport))
		msg.data = event.ofp
		msg.in_port = event.port
		event.connection.send(msg)            

	def flood (self, message = None):
		# Floods the packet
		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
		msg.data = event.ofp
		msg.in_port = event.port
		event.connection.send(msg)

	def installRuleForSW1(self, event):
		packet = event.parsed
		# F1
		if src == EthAddr('00:00:00:00:00:01') and dst == EthAddr('00:00:00:00:00:06'):
			port = 1
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:01'):
			port = 3
			self.install_fwdrule(event, packet, port)
		else:
			pass


	def installRuleForSW2(self, event):
		# F4
		if src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:07'):
			port = 3
			self.install_fwdrule(event, packet, port)

		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:05'):
			port = 1
			self.install_fwdrule(event, packet, port)

		# F7
		elif src == EthAddr('00:00:00:00:00:02') and dst == EthAddr('00:00:00:00:00:05'):
			port = 2
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:02'):
			port = 4
			self.install_fwdrule(event, packet, port)
		else:
			pass

	def installRuleForSW3(self, event):
		# F2
		if src == EthAddr('00:00:00:00:00:03') and dst == EthAddr('00:00:00:00:00:05'):
			port = 4
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:03'):
			port = 5
			self.install_fwdrule(event, packet, port)

		# F6
		elif src == EthAddr('00:00:00:00:00:08') and dst == EthAddr('00:00:00:00:00:06'):
			port = 3
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:08'):
			port = 2
			self.install_fwdrule(event, packet, port)
		else:
			pass


	def installRuleForSW4(self, event):
		# F2
		if src == EthAddr('00:00:00:00:00:03') and dst == EthAddr('00:00:00:00:00:05'):
			port = 2
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:03'):
			port = 1
			self.install_fwdrule(event, packet, port)
		# F3
		elif src == EthAddr('00:00:00:00:00:04') and dst == EthAddr('00:00:00:00:00:07'):
			port = 4
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:04'):
			port = 5
			self.install_fwdrule(event, packet, port)
		# F7
		elif src == EthAddr('00:00:00:00:00:02') and dst == EthAddr('00:00:00:00:00:05'):
			port = 2
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:02'):
			port = 3
			self.install_fwdrule(event, packet, port)
		else:
			pass

	def installRuleForSW5(self, event):
		# F2
		if src == EthAddr('00:00:00:00:00:03') and dst == EthAddr('00:00:00:00:00:05'):
			port = 5
			self.install_rule(event ,src, dst, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:03'):
			port = 2
			self.install_rule(event ,src, dst, port)

		# F4
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:07'):
			port = 3
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:05'):
			port = 5
			self.install_fwdrule(event, packet, port)

		# F5
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:07'):
			port = 4
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:06'):
			port = 1
			self.install_fwdrule(event, packet, port)
		# F7
		elif src == EthAddr('00:00:00:00:00:02') and dst == EthAddr('00:00:00:00:00:05'):
			port = 5
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:02'):
			port = 2
			self.install_fwdrule(event, packet, port)
		else:
			pass


	def installRuleForSW6(self, event):
		# F1
		if src == EthAddr('00:00:00:00:00:01') and dst == EthAddr('00:00:00:00:00:06'):
			port = 4
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:01'):
			port = 1
			self.install_fwdrule(event, packet, port)
		# F5
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:07'):
			port = 3
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:06'):
			port = 4
			self.install_fwdrule(event, packet, port)
		# F6
		elif src == EthAddr('00:00:00:00:00:08') and dst == EthAddr('00:00:00:00:00:06'):
			port = 4
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:08'):
			port = 2
			self.install_fwdrule(event, packet, port)

	def installRuleForSW7(self, event):
		# F3
		if src == EthAddr('00:00:00:00:00:04') and dst == EthAddr('00:00:00:00:00:07'):
			port = 5
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:04'):
			port = 3
			self.install_fwdrule(event, packet, port)

		# F4
		elif src == EthAddr('00:00:00:00:00:05') and dst == EthAddr('00:00:00:00:00:07'):
			port = 5
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:05'):
			port = 2
			self.install_fwdrule(event, packet, port)
		# F5
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:07'):
			port = 5
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:07') and dst == EthAddr('00:00:00:00:00:06'):
			port = 4
			self.install_fwdrule(event, packet, port)

	def installRuleForSW8(self, event):
		# F1
		if src == EthAddr('00:00:00:00:00:01') and dst == EthAddr('00:00:00:00:00:06'):
			port = 3
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:01'):
			port = 1
			self.install_fwdrule(event, packet, port)
		# F6
		elif src == EthAddr('00:00:00:00:00:08') and dst == EthAddr('00:00:00:00:00:06'):
			port = 2
			self.install_fwdrule(event, packet, port)
		elif src == EthAddr('00:00:00:00:00:06') and dst == EthAddr('00:00:00:00:00:08'):
			port = 5
			self.install_fwdrule(event, packet, port)


	def installForwardRuleByDPID(self, dpid, event):
		if dpid == '00-00-00-00-00-01':
			self.installRuleForSW1(event)
		elif dpid == '00-00-00-00-00-02':
			self.installRuleForSW2(event)
		elif dpid == '00-00-00-00-00-03':
			self.installRuleForSW3(event)    	
		elif dpid == '00-00-00-00-00-04':
			self.installRuleForSW4(event)
		elif dpid == '00-00-00-00-00-05':
			self.installRuleForSW5(event)
		elif dpid == '00-00-00-00-00-06':
			self.installRuleForSW6(event)
		elif dpid == '00-00-00-00-00-07':
			self.installRuleForSW7(event)
		elif dpid == '00-00-00-00-00-08':
			self.installRuleForSW8(event)
		else:
			log.debug("No rule has been installed at switch %s", dpid)


	def _handle_PacketIn(self, event):
		dpid = dpidToStr(event.dpid)
		tcpp = event.parsed.find('tcp')

		self.installForwardRuleByDPID(dpid, event)

	def _handle_ConnectionUp(self, event):
		dpid = dpidToStr(event.dpid)
		log.debug("Switch %s has come up.", dpid)


def launch():
	# Run spanning tree so that we can deal with topologies with loops
	pox.openflow.discovery.launch()
	pox.openflow.spanning_tree.launch()

	'''
	Starting the Dionysus current rules module
	'''
	core.registerNew(DTCurrentRules)
