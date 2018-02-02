# -*- coding: utf-8 -*-

from config import CONFIG as config
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
from DownScalers.DBProduct import BDProduct
from copy import copy

class Topology(Topo):
    "Single switch connected to n hosts."

    def __init__(self, config):
        self.config = config
        super(Topology, self).__init__()

    def build( self ):
        for s in config['switches']:
            self.addSwitch(s)

        for h in config['hosts']:
            self.addHost(h)

        for l in config['links']:
            self.addLink(l["node1"], l["node2"], bw=l['bw'], delay=l['delay'])

def run_ftp_experiment():

    bdproduct = BDProduct(0.5)
    config_updated = bdproduct.update_config(config)

    topo = Topology(config_updated)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    try:

        tc = TrafficCapturer(eths=['s1-eth1'])
        tc.start_capturing()

        net.pingAll()

        flow_scheduler = FlowScheduler()
        results = flow_scheduler.run_commands(net, config_updated["commands"])
        for h, r in results.iteritems():
            print(h, "".join(r))
            print("----")

        tc.decode_capture(remove_old=False)

        ra = ResultAnalyzer(pathes=[tc.get_filename() + '.csv'],
                            ip_dsts=['10.0.0.2'],
                            freq='500ms')
        ra.plot()
        os.system("rm tmp_files/*")
    except Exception as ex:
        print(ex)
    finally:
        net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run_ftp_experiment()
