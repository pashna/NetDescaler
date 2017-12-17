from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
SERVER_FILES = "/home/pkochetk/msu/diploma/repo/ftp/server_files"
authorizer.add_user("user",
                    "12345",
                    SERVER_FILES,
                    perm="elradfmw")
authorizer.add_anonymous(SERVER_FILES, perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("10.0.0.1", 1026), handler)
server.serve_forever()