#!/usr/bin/python

"""
Create a 1024-host network, and run the CLI on it.
If this fails because of kernel limits, you may have
to adjust them, e.g. by adding entries to /etc/sysctl.conf
and running sysctl -p. Check util/sysctl_addon.
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.util import pmonitor
from topolib import TreeNet

import sys
sys.path.append("..")
from tools.tools import iperfTest, minCut

if __name__ == '__main__':
    setLogLevel( 'info' )
    network = TreeNet( depth=2, fanout=4, bw=1, switch=OVSSwitch, link=TCLink)
    network.start()
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    iperfTest(network, pairs = 2)
    #CLI(network)
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    network.stop()
