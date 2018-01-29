# -*- coding: utf-8 -*-

from config import CONFIG
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
from time import sleep
from signal import SIGINT
from datetime import datetime
import os
from Analizer.Capturer import TrafficCapturer
from Analizer.ResultAnalizer import ResultAnalyzer
from time import sleep
from datetime import datetime, timedelta
from NetworkApps.FlowScheduler import FlowScheduler

class Topology(Topo):
    "Single switch connected to n hosts."

    def __init__(self):
        super(Topology, self).__init__()

    def build( self ):
        for s in CONFIG['switches']:
            self.addSwitch(s)

        for h in CONFIG['hosts']:
            self.addHost(h)

        for l in CONFIG['links']:
            self.addLink(l["node1"], l["node2"], bw=l['bw'], delay=l['delay'])

def pingAll():

    "Create network and run simple performance test"
    topo = Topology()

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    eths_to_capture = ['{}-eth0'.format(h) for h in CONFIG["interfaces_to_capture"]]

    tc = TrafficCapturer(eths=['s1-eth1'])
    tc.start_capturing()

    net.pingAll()

    flow_scheduler = FlowScheduler()
    results = flow_scheduler.run_commands(net, CONFIG["commands"])

    for h, r in results.iteritems():
        print(h, "".join(r))
        print("----")

    tc.decode_capture(remove_old=False)

    ra = ResultAnalyzer(pathes=[tc.get_filename() + '.csv'],
                        ip_dsts=['10.0.0.2'],
                        freq='50ms')
    ra.plot()
    os.system("rm tmp_files/*")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    pingAll()
