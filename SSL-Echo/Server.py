#SSL encrypted echo server
#
#
# ----------------------------------------------------------------------------------------------------------------------

import socket
import ssl
import sys
import os

os.environ["SSL_CERT_FILE"] = 'server.cert'

def main(certfile, keyfile):
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=None)
    # load the certificate
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    s.bind(('',8001))
    s.listen(1)
    sock, address = s.accept()
    sslsock = context.wrap_socket(sock, server_side=True)
    while True:
        data = sslsock.recv(1024)
        print('Received', repr(data))
        sslsock.send(data)
        sslsock.close()
        break
    s.close()
if __name__ == "__main__":
    #parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <filepath>")
        sys.exit()
    certfile = sys.argv[1]
    keyfile = sys.argv[2]
    main(certfile, keyfile)