from mininet.topo import Topo


class TopologyBuilder(Topo):
    "Single switch connected to n hosts."

    def __init__(self, config):
        self.config = config
        super(TopologyBuilder, self).__init__()

    def build( self ):
        for s in self.config['switches']:
            self.addSwitch(s)

        for h in self.config['hosts']:
            self.addHost(h)

        for l in self.config['links']:
            self.addLink(l["node1"], l["node2"], bw=l['bw'], delay=l['delay'])