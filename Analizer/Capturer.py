import os
from time import gmtime, strftime, sleep


class TrafficCapturer:

    def __init__(self, filename=None, eths=None):
        """
        :param filename:
        :param eths: list of interfaces to capture
        """
        if filename is None:
            date = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
            filename = os.getcwd() + os.sep + 'csv' + os.sep + date

        self.__eths = "" if eths is None else " ".join(eths)
        self.__filename = filename

    def start_capturing(self):
        print("Saving Capture To {}".format(self.__filename))
        os.system("tcpdump -w {}.pcap -i {} & ".format(self.__filename,
                                                       self.__eths))
        sleep(2)

    def decode_capture(self, remove_old=False):
        os.system("tshark -r {}.pcap -T fields -e frame.number -e frame.time "
                  " -e ip.src -e ip.dst -e frame.len -e tcp.seq > {}.csv".format(self.__filename,
                                                                                 self.__filename))
        if remove_old:
            os.system("rm {}.pcap".format(self.__filename))


    def get_filename(self):
        return self.__filename

