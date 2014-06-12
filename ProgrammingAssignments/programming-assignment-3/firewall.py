'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        
        

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        policyFileContent = open(policyFile)
        policyFileContent.readline()
        while True:
            line = policyFileContent.readline()
            if not line:
                break
            print line
            info = line.split(',')
            info[2].strip('\n')
            msg = of.ofp_flow_mod()
            msg_mirror = of.ofp_flow_mod()

            msg.priority = msg_mirror.priority = 42
            #msg.idle_timeout = 100
            #msg.hard_timeout = 200
            msg.match.dl_type = msg_mirror.match.dl_type = 0x0800
            
            msg.match.dl_src = EthAddr(info[1])
            msg_mirror.match.dl_dst = EthAddr(info[1])

            msg.match.dl_dst = EthAddr(info[2])
            msg_mirror.match.dl_src = EthAddr(info[2])

            #msg.actions.append(of.ofp_action_output(port=OFPP_NONE))
            event.connection.send(msg)
            event.connection.send(msg_mirror)
            print 

            
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
