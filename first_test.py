# -*- coding: utf-8 -*-

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController


class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, n=2 ):
        switch = self.addSwitch( 's1' )
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1),
                             cpu=.5/n )

            self.addLink( host, switch, bw=20)

def perfTest():
    "Create network and run simple performance test"
    topo = SingleSwitchTopo(n=4)
    controller = RemoteController('controller', ip='127.0.0.1', port=6633)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=controller)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    h1, h2 = net.get('h1', 'h2')
    #print("h1: ", h1.cmd("ifconfig"))
    #print("h2: ", h2.cmd("ifconfig"))
    h2.cmd('./D-ITG-2.8.1-r1023/bin/ITGRecv')
    h1.cmd('./D-ITG-2.8.1-r1023/bin/ITGSend –T UDP  –a 10.0.0.2 –c 100 –C 10 –t 5000 -l sender.log –x receiver.log ')

    #print("Testing network connectivity")
    #net.pingAll()
    #print("Testing bandwidth between h1 and h4")
    #h1, h4 = net.get('h1', 'h4')
    #h1.sendCmd('./D-ITG-2.8.1-r1023/bin/ITGRecv')
    #h4.sendCmd('./D-ITG-2.8.1-r1023/bin/ITGSend –T UDP  –a 10.0.0.2 –c 100 –C 10 –t 15000 -l sender.log –x receiver.log ')

    #results = {}
    #for h in [h1, h4]:
    #    results[h.name] = h.waitOutput()

    #print(results)
    #net.iperf((h1, h4))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    perfTest()