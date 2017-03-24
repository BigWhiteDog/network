#!/usr/bin/env python

from ripl.dctopo import FatTreeTopo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
import os

def __setCoreRoutes(sw, k):
    ##ovs port index start from 1
    for i in range(0, k):
        ##for ip packets
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0800,nw_dst=10.%d.0.0/16,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, i, i + 1))
        ##for arp packets
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0806,nw_dst=10.%d.0.0/16,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, i, i + 1))

def __setAggRoutes(sw, swid, pod, k):
    ##add prefix
    for i in range(0, k / 2):
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0800,nw_dst=10.%d.%d.0/24,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, pod, i, i + 1))
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0806,nw_dst=10.%d.%d.0/24,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, pod, i, i + 1))
    ##add suffix
    for i in range(0, k / 2):
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0800,nw_dst=0.0.0.%d/0.0.0.255,idle_timeout=0,hard_timeout=0,priority=5,action=output:%d" % (sw, i + 2, (i + swid)%(k / 2) + k / 2 + 1))
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0806,nw_dst=0.0.0.%d/0.0.0.255,idle_timeout=0,hard_timeout=0,priority=5,action=output:%d" % (sw, i + 2, (i + swid)%(k / 2) + k / 2 + 1))

def __setEdgeRoutes(sw, swid, pod, k):
    ##add prefix
    for i in range(0, k / 2):
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0800,nw_dst=10.%d.%d.%d/32,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, pod, swid, i + 2, i + 1))
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0806,nw_dst=10.%d.%d.%d/32,idle_timeout=0,hard_timeout=0,priority=10,action=output:%d" % (sw, pod, swid, i + 2, i + 1))
    ##add suffix
    for i in range(0, k / 2):
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0800,nw_dst=0.0.0.%d/0.0.0.255,idle_timeout=0,hard_timeout=0,priority=5,action=output:%d" % (sw, i + 2, (i + swid)%(k / 2) + k / 2 + 1))
        os.system("sudo ovs-ofctl add-flow %s dl_type=0x0806,nw_dst=0.0.0.%d/0.0.0.255,idle_timeout=0,hard_timeout=0,priority=5,action=output:%d" % (sw, i + 2, (i + swid)%(k / 2) + k / 2 + 1))

def setRoutes(net):
    topo = net.topo
    mg = topo.g
    for s in net.switches:
        layer = mg.node[s.name]["layer"]
        node_id = topo.id_gen(name = s.name)
        if layer == topo.LAYER_CORE:
            __setCoreRoutes(s.name, topo.k)
        elif layer == topo.LAYER_AGG:
            __setAggRoutes(s.name, node_id.sw, node_id.pod, topo.k)
        else:
            __setEdgeRoutes(s.name, node_id.sw, node_id.pod, topo.k)


def FatTreeNet(k = 4, speed=1.0, **kwargs):
    topo = FatTreeTopo(k, speed)
    net = Mininet(topo, **kwargs)
    return net

if __name__ == "__main__":
    setLogLevel("info")
    net = FatTreeNet(link=TCLink, controller=None, autoSetMacs=True)
    net.start()
    setRoutes(net)
    #net.pingAll()
    CLI(net)
    net.stop()
