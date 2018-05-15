import os
import sys
from ftplib import FTP
from time import sleep
import subprocess

import urllib

class HTTPClient():

    def get(self, ip, size):
        contents = urllib.urlopen("http://{}:9191/{}".format(ip, size)).read()
        print(contents)


def main(server_ip, size):
    client = HTTPClient()
    client.get(server_ip, size)


if __name__ == '__main__':

    server = sys.argv[1]
    size = sys.argv[2]

    sleep_time = float(sys.argv[3])

    sleep(sleep_time)
    main(server, size)
