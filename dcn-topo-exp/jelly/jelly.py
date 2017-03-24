#!/usr/bin/env python

"""
Create a 1024-host network, and run the CLI on it.
If this fails because of kernel limits, you may have
to adjust them, e.g. by adding entries to /etc/sysctl.conf
and running sysctl -p. Check util/sysctl_addon.
"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.link import TCLink
from jellyfish.topologies.jellyfish import JellyfishTopo

import sys
sys.path.append("..")
from tools.tools import iperfTest, minCut


def JellyfishNet(seed=0, switches=16, nodes=4, ports_per_switch=4, hosts_per_switch=1, bw=1, **kwargs):
    topo = JellyfishTopo(seed, switches, nodes, ports_per_switch, hosts_per_switch, bw)
    return Mininet(topo, **kwargs)

if __name__ == '__main__':
    setLogLevel( 'info' )
    network = JellyfishNet(switch=OVSSwitch, link=TCLink, controller=RemoteController, autoSetMacs=True)
    network.start()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    iperfTest(network, pairs = 2)
    CLI(network)
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    network.stop()
