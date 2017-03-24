"Library of potentially useful topologies for Mininet"

from mininet.topo import Topo
from mininet.net import Mininet

# The build() method is expected to do this:
# pylint: disable=arguments-differ

class TreeTopo( Topo ):
    "Topology for a tree network with a given depth and fanout."

    def build( self, depth=1, fanout=2 , bw=1):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        self.bw = bw
        # Build topology
        self.addTree( depth, fanout )

    def addTree( self, depth, fanout ):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth > 0
        if isSwitch:
            node = self.addSwitch( 's%s' % self.switchNum )
            self.switchNum += 1
            for _ in range( fanout ):
                child = self.addTree( depth - 1, fanout )
                #link = 100Mbps
                self.addLink( node, child , bw = self.bw)
        else:
            node = self.addHost( 'h%s' % self.hostNum )
            self.hostNum += 1
        return node


def TreeNet( depth=1, fanout=2, bw=1, **kwargs ):
    "Convenience function for creating tree networks."
    topo = TreeTopo( depth, fanout, bw)
    return Mininet( topo, **kwargs)

