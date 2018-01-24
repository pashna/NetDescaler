# -*- coding: utf-8 -*-

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

FOLDER_TO_SAVE = "/home/pkochetk/images/data/MSU/capture/exp_2"


class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."

    def __init__(self, bw, delay, n_hosts, loss=0):
        self.bw = bw
        self.delay = str(delay) + 'ms'
        self.loss = loss
        self.n_hosts = n_hosts
        super(SingleSwitchTopo, self).__init__()


    def build( self ):
        """
        switch = self.addSwitch( 's1' )

        for h in range(self.n_hosts):
            # Each host gets 50%/n of system CPU
            host = self.addHost( 'h%s' % (h + 1),
                             cpu=.5/self.n_hosts )

            self.addLink( host,
                          switch,
                          bw=self.bw,
                          delay=self.delay,
                          loss=self.loss,
                          use_htb=True)

        """
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(s1, s2, bw=self.bw, delay=self.delay, loss=self.loss, use_htb=True)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        self.addLink(h1, s1, bw=self.bw, delay=self.delay, loss=self.loss, use_htb=True)
        self.addLink(h2, s1, bw=self.bw, delay=self.delay, loss=self.loss, use_htb=True)
        self.addLink(h3, s2, bw=self.bw, delay=self.delay, loss=self.loss, use_htb=True)
        self.addLink(h4, s2, bw=self.bw, delay=self.delay, loss=self.loss, use_htb=True)



def ftp(bw, delay, scale=1, loss=0, n_hosts=4):
    bw = bw * scale
    delay = int(delay / scale)

    "Create network and run simple performance test"
    topo = SingleSwitchTopo(bw=bw,
                            delay=delay,
                            n_hosts=n_hosts,
                            loss=loss)

    # controller = RemoteController('controller', ip='127.0.0.1', port=6633)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)#, controller=controller)

    date = datetime.now().strftime("%m_%d_%H_%M")

    net.start()
    file_name = "date__{}mb_{}".format(date, BW, DELAY)
    SCALE_FOLDER = str(scale).replace('.', '_')

    path_to_file = FOLDER_TO_SAVE + '/' + SCALE_FOLDER + '/' + file_name
    os.system("tcpdump -w {}.pcap -i s1-eth1 & ".format(path_to_file))

    sleep(2)
    net.pingAll()
    print("Dumping host connections")
    dumpNodeConnections( net.hosts )
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

    h1.cmd("rm *.log")

    print("========")

    print("start_test. RUN WIRESHARK!!!")

    print("Running server 1")
    print(h1.cmd('python ftp_server.py &'))


    sleep(2)
    print(h2.cmd('python ftp_client.py &'))

    sleep(1 * (1/scale))
    print(h3.cmd('python ftp_client.py &'))

    sleep(2 * (1 / scale))
    print("Running h4")
    print(h4.cmd('python ftp_client.py'))

    print("Waiting for results")
    #sleep(40)

    h1.shell.send_signal(SIGINT)
    h2.shell.send_signal(SIGINT)
    h3.shell.send_signal(SIGINT)
    h4.shell.send_signal(SIGINT)

    print("closing sessions")
    print("tshark -r {}.pcap -T fields -e frame.number -e frame.timestamp "
              " -e ip.src -e ip.dst -e frame.len -e tcp.seq > {}.csv".format(path_to_file,
                                                                             path_to_file))

    os.system("tshark -r {}.pcap -T fields -e frame.number -e frame.time "
              " -e ip.src -e ip.dst -e frame.len -e tcp.seq > {}.csv".format(path_to_file,
                                                                             path_to_file))


    os.system("chmod 777 {}.*".format(path_to_file))

    print("All started and supposed to finish. RESULT:")
    #print(h1.cmd('../software/D-ITG/bin/ITGDec sender.log'))
    #print(h2.cmd('../software/D-ITG/bin/ITGDec receiver.log'))

    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    BW = 50
    DELAY = 50
    scale = 1
    for scale in [1.]:
        ftp(BW, DELAY, scale=scale)