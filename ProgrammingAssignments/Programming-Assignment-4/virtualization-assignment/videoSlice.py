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


class VideoSlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)
        # Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda:defaultdict(lambda:None))
        
        '''
        The structure of self.port_map is a four-tuple key and a string value.
        The type is:
        (dpid string, src MAC addr, dst MAC addr, port (int)) -> dpid of next switch
        '''
		
        self.port_map = {
						('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'), EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'), EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'), EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'), EthAddr('00:00:00:00:00:04'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'), EthAddr('00:00:00:00:00:01'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'), EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'), EthAddr('00:00:00:00:00:01'), 80): '00-00-00-00-00-03',
						('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'), EthAddr('00:00:00:00:00:02'), 80): '00-00-00-00-00-03'
						 }

        self.same_side = {
						 ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'), EthAddr('00:00:00:00:00:02')):4,
						 ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:02'), EthAddr('00:00:00:00:00:01')):3,
						 ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:03'), EthAddr('00:00:00:00:00:04')):4,
						 ('00-00-00-00-00-04', EthAddr('00:00:00:00:00:04'), EthAddr('00:00:00:00:00:03')):3
						 }
				

    def _handle_LinkEvent (self, event):
		l = event.link
		sw1 = dpid_to_str(l.dpid1)
		sw2 = dpid_to_str(l.dpid2)
		log.debug ("link %s[%d] <-> %s[%d]",sw1, l.port1,sw2, l.port2)
		self.adjacency[sw1][sw2] = l.port1
		self.adjacency[sw2][sw1] = l.port2


    def _handle_PacketIn (self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed
        tcpp = event.parsed.find('tcp')
        

        def install_fwdrule(event,packet,outport):
            msg = of.ofp_flow_mod()
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.actions.append(of.ofp_action_output(port = outport))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def forward (message = None):
            this_dpid = dpid_to_str(event.dpid)

            if packet.dst.is_multicast:
                flood()
                return
            else:
				log.debug("Got unicast packet for %s at %s (input port %d):", packet.dst, dpid_to_str(event.dpid), event.port)
				
				try:
					thisHop = dpid_to_str(event.dpid)
					traffic = (thisHop, packet.src, packet.dst)
					if self.same_side.get(traffic) is not None:
						""" h1<->h2 or h3<->h4"""
						outPort = self.same_side.get(traffic)
						log.debug("At %s Packet from port %d goes to the same side, forward it to %d at %s", thisHop, event.port, outPort, this_dpid)
						install_fwdrule(event, packet, outPort)
					else: 
						""" cross line: need to check if in port_map"""
						log.debug("TCP dst port: %d, src port: %d", tcpp.dstport, tcpp.srcport)
						if tcpp.srcport == 80 or tcpp.dstport == 80:
							traffic = (thisHop, packet.src, packet.dst, 80)
						else:
							traffic = (thisHop, packet.src, packet.dst, tcpp.srcport)

						if self.port_map.get(traffic) is not None:
							# video traffic
							nextHop = self.port_map.get(traffic) # e.g. '00-00-00-00-00-03'
							#outPort = self.adjacency[thisHop][nextHop] # e.g. port 2 for sw1 and sw4
							outPort = 2
							log.debug("At %s Video packet from port %d goes cross, forward it to %d so that it hops to %s", thisHop, event.port, outPort, nextHop)
							install_fwdrule(event, packet, outPort)
						else:
							# non-video traffic
							if this_dpid == '00-00-00-00-00-01': 
								if packet.dst == EthAddr('00-00-00-00-00-01'):
									nextHop = '10.0.0.1'
									outPort = 3
								elif packet.dst == EthAddr('00-00-00-00-00-02'):
									nextHop = '10.0.0.2'
									outPort = 4
								else:
									nextHop = '00-00-00-00-00-02'
									outPort = 1
							elif this_dpid == '00-00-00-00-00-04':
								if packet.dst == EthAddr('00-00-00-00-00-03'):
									nextHop = '10.0.0.3'
									outPort = 3
								elif packet.dst == EthAddr('00-00-00-00-00-04'):
									nextHop = '10.0.0.4'
									outPort = 4
								else:
									nextHop = '00-00-00-00-00-02'
									outPort = 1
							else:
								nextHop = packet.dst
								if packet.dst == EthAddr('00-00-00-00-00-03') or packet.dst == EthAddr('00-00-00-00-00-04'):
									nextHop = '00-00-00-00-00-04'
									outPort = 2
								else: #if packet.dst == EthAddr('00-00-00-00-00-01') or packet.dst == EthAddr('00-00-00-00-00-02'):
									nextHop = '00-00-00-00-00-01'
									outPort = 1

							log.debug("At %s Regular packet from port %d goes cross, forward it to %d so that it hops to %s", thisHop, event.port, outPort, nextHop)
							install_fwdrule(event, packet, outPort)

				except AttributeError:
					log.debug("packet type has no transport ports, flooding")
					if tcpp is None:
						log.debug("TCP segment is None")
					else:
						log.debug("TCP dst port: %d, src port: %d", tcpp.dstport, tcpp.srcport)
					# flood and install the flow table entry for the flood
					install_fwdrule(event,packet,of.OFPP_FLOOD)
					
        # flood, but don't install the rule
        def flood (message = None):
            """ Floods the packet """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        forward()


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        log.debug("Switch %s has come up.", dpid)
        

def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Video Slicing module
    '''
    core.registerNew(VideoSlice)
