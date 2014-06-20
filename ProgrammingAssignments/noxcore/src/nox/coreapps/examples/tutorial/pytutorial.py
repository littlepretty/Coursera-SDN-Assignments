# Tutorial Controller
# Starts as a hub, and your job is to turn this into a learning switch.

import logging

from nox.lib.core import *
import nox.lib.openflow as openflow
from nox.lib.packet.ethernet import ethernet
from nox.lib.packet.packet_utils import mac_to_str, mac_to_int

log = logging.getLogger('nox.coreapps.tutorial.pytutorial')


class pytutorial(Component):

    def __init__(self, ctxt):
        Component.__init__(self, ctxt)
        # Use this table to store MAC addresses in the format of your choice;
        # Functions already imported, including mac_to_str, and mac_to_int,
        # should prove useful for converting the byte array provided by NOX
        # for packet MAC destination fields.
        # This table is initialized to empty when your module starts up.
        self.mac_to_port = {} # key: MAC addr; value: port

    def learn_and_forward(self, dpid, inport, packet, buf, bufid):
        """Learn MAC src port mapping, then flood or send unicast."""
        
        # Initial hub behavior: flood packet out everything but input port.
        # Comment out the line below when starting the exercise.
        self.send_openflow(dpid, bufid, buf, openflow.OFPP_FLOOD, inport)

        # Starter psuedocode for learning switch exercise below: you'll need to
        # replace each pseudocode line with more specific Python code.

        # Learn the port for the source MAC
        #self.mac_to_port = <fill in>
        #if (destination MAC of the packet is known):
            # Send unicast packet to known output port
            #self.send_openflow( <fill in params> )
            # Later, only after learning controller works: 
            # push down flow entry and remove the send_openflow command above.
            #self.install_datapath_flow( <fill in params> )
        #else:
            #flood packet out everything but the input port
            #self.send_openflow(dpid, bufid, buf, openflow.OFPP_FLOOD, inport)

    def packet_in_callback(self, dpid, inport, reason, len, bufid, packet):
        """Packet-in handler""" 
        if not packet.parsed:
            log.debug('Ignoring incomplete packet')
        else:
            self.learn_and_forward(dpid, inport, packet, packet.arr, bufid)    

        return CONTINUE

    def install(self):
        self.register_for_packet_in(self.packet_in_callback)
    
    def getInterface(self):
        return str(pytutorial)

def getFactory():
    class Factory:
        def instance(self, ctxt):
            return pytutorial(ctxt)

    return Factory()
