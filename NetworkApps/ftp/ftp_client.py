import os
import sys
from ftplib import FTP
from time import sleep
import subprocess


def get_ip():
    proc = subprocess.Popen(["ifconfig | grep -Po '(?<=inet addr:)[0-9\.]+'"], stdout=subprocess.PIPE, shell=True)
    out, _ = proc.communicate()
    ip_address = str(out).split('\\n')[0][2:]
    return ip_address

class FTPClient:

    def __init__(self):
        self.__ftp = FTP('')

    def connect(self, server_ip):
        self.__ftp.connect(server_ip, 1026)
        self.__ftp.login()
        self.__ftp.cwd('/')  # replace with your directory
        self.__ftp.retrlines('LIST')

    def upload(self, filename):
        self.__ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
        self.__ftp.quit()
        print("uploaded")

    def download(self, filename):
        localfile = 'tmp_files/{}_{}'.format(filename, get_ip())
        print('LOCALF = ', localfile)
        with open(localfile, 'wb') as localfile:
            self.__ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
            self.__ftp.quit()

        print("downloaded")


def main(filename, server, cmd):
    client = FTPClient()

    client.connect(server)
    if cmd == 'download':
        client.download(filename)
    else:
        client.upload()


if __name__ == '__main__':
    filesize = sys.argv[1]

    # create a file
    # TODO: ADD CHECHING IF IT EXISTS

    filename = "ftp_file_{}".format(filesize)
    filepath = os.getcwd() + os.sep + 'tmp_files' + os.sep + filename
    os.system("dd if=/dev/zero of={}  bs={}  count=1".format(filepath, filesize))

    print(filename)
    server = sys.argv[2]
    cmd = sys.argv[3]
    sleep_time = 0
    if len(sys.argv) == 5:
        sleep_time = float(sys.argv[4])

    sleep(sleep_time)
    main(filename, server, cmd)
