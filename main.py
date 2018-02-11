# -*- coding: utf-8 -*-

from config import CONFIG as config
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSSwitch, Controller, RemoteController
import sys
from Analizer.GraphVisualizer import GraphVisualizer

import os
from Analizer.Capturer import TrafficCapturer
from Analizer.ResultAnalizer import ResultAnalyzer
from NetworkApps.FlowScheduler import FlowScheduler
from DownScalers.DBProduct import BDProduct
from time import sleep
from time import gmtime, strftime

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

def run_ftp_experiment(path, scale_factor):
    if "plot_graph" in config and config["plot_graph"]:
        GraphVisualizer().draw_graph(config["links"], config["hosts"])

    bdproduct = BDProduct(scale_factor)
    config_updated = bdproduct.update_config(config)

    topo = Topology(config_updated)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    try:

        tc = TrafficCapturer(filename=path, eths=['s1-eth1'])
        tc.start_capturing()

        net.pingAll()

        flow_scheduler = FlowScheduler()
        results = flow_scheduler.run_commands(net, config_updated["commands"])
        for h, r in results.iteritems():
            print(h, "".join(r))
            print("")
            print("----")

        tc.decode_capture(remove_pcap=True)

        os.system("rm tmp_files/*")
    except Exception as ex:
        print(ex)
    finally:
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')

    if len(sys.argv) > 1:
        scale_factor = float(sys.argv[1])
        path = sys.argv[2] + strftime("%Y_%m_%d__%H_%M_%S", gmtime())
    else:
        scale_factor = config["scale_factor"]
        path = config["save_path"] + strftime("%Y_%m_%d__%H_%M_%S", gmtime())
    print(config)
    print("Experiment is starting. {}, {}".format(scale_factor, path))
    run_ftp_experiment(path, scale_factor)
