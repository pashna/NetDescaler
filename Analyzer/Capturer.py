import os
from time import gmtime, strftime, sleep
import pandas as pd

class TrafficCapturer:

    def __init__(self, filename=None, eths=None):
        """
        :param filename:
        :param eths: list of interfaces to capture
        """
        if filename is None:
            date = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
            filename = os.getcwd() + os.sep + 'csv' + os.sep + date

        self.__eths = eths
        self.__filename = filename

    def start_capturing(self):
        print("Saving Capture To {}".format(self.__filename))
        for eth in self.__eths:
            os.system("tcpdump -w {}_{}.pcap -i {} &".format(self.__filename, eth, eth))
        sleep(2)

    def decode_capture(self, remove_pcap=False):

        for eth in self.__eths:
            os.system("tshark -r {}_{}.pcap -T fields -e frame.number -e frame.time "
                      " -e ip.src -e ip.dst -e frame.len > {}_{}.csv".format(self.__filename,
                                                                             eth,
                                                                             self.__filename,
                                                                             eth))
            if remove_pcap:
                os.system("rm {}_{}.pcap".format(self.__filename, eth))


    def get_filename(self):
        return self.__filename
