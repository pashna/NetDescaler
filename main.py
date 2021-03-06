# -*- coding: utf-8 -*-
from MininetHelpers.TopologyBuilder import TopologyBuilder
from mininet.topo import Topo
#from config import CONFIG as config
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
from utils.utils import *
import sys
from Analyzer.GraphVisualizer import GraphVisualizer
from Analyzer.Capturer import TrafficCapturer
from NetworkApps.FlowScheduler import FlowScheduler
from DownScalers.DBProduct import BDProduct
from time import gmtime, strftime, sleep
import os


def run_experiment(config, scale_factor):
    path = config['save_path'] + "last_experiment"
    if "plot_graph" in config and config["plot_graph"]:
        GraphVisualizer().draw_graph(config["links"], config["hosts"])

    bdproduct = BDProduct(scale_factor)
    config_updated = bdproduct.update_config(config)

    topo = TopologyBuilder(config_updated)

    net = Mininet(topo=topo, link=TCLink)
    net.start()

    try:
        os.system("mkdir tmp_files")
        tc = TrafficCapturer(filename=path, switches=config_updated['interface_to_capture'])
        tc.start_capturing()

        net.pingAll()

        flow_scheduler = FlowScheduler()
        results = flow_scheduler.run_commands(net, config_updated["commands"])

        for h, r in results.iteritems():
            print(h, "".join(r))
            print("")
            print("----")

        print("preparing results")
        sleep(30)
        tc.decode_capture(remove_pcap=False)

        os.system("rm -r tmp_files")
    except Exception as ex:
        print(ex)
    finally:
        net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    config = read_json("config.json")
    scale_factor = config["scale_factor"]
    run_experiment(config, scale_factor)