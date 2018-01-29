from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer as FTP
import os
import subprocess

def get_ip():
    proc = subprocess.Popen(["ifconfig | grep -Po '(?<=inet addr:)[0-9\.]+'"], stdout=subprocess.PIPE, shell=True)
    out, _ = proc.communicate()
    ip_address = str(out).split('\\n')[0]
    return ip_address


class FTPServer:

    def __init__(self):
        self.__authorizer = DummyAuthorizer()
        server_files = os.getcwd() + os.sep + "tmp_files"
        perm = "elradfmw"
        self.__authorizer.add_user(
                            "user",
                            "12345",
                            server_files,
                            perm="elradfmw")
        self.__authorizer.add_anonymous(server_files, perm=perm)

    def run(self):
        handler = FTPHandler
        handler.authorizer = self.__authorizer
        self.__server = FTP((get_ip(), 1026), handler)
        self.__server.serve_forever()


def main():
    ftp_server = FTPServer()
    ftp_server.run()


if __name__ == "__main__":
    main()
