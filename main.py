# -*- coding: utf-8 -*-
from MininetHelpers.TopologyBuilder import TopologyBuilder
from config import CONFIG as config
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.log import setLogLevel
import sys
from Analyzer.GraphVisualizer import GraphVisualizer
from Analyzer.Capturer import TrafficCapturer
from NetworkApps.FlowScheduler import FlowScheduler
from DownScalers.DBProduct import BDProduct
from time import gmtime, strftime
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

        tc = TrafficCapturer(filename=path, eths=config_updated['interface_to_capture'])
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
    import os

    #if len(sys.argv) > 1:
    #    scale_factor = float(sys.argv[1])
    #    path = sys.argv[2] + strftime("%Y_%m_%d__%H_%M_%S", gmtime())
    #else:
    #scale_factor = config["scale_factor"]
    #path = config["save_path"] + strftime("last_experiment", gmtime())
    #print(config)
    #print("Experiment is starting. {}, {}".format(scale_factor, path))
    #run_experiment(path, scale_factor)
