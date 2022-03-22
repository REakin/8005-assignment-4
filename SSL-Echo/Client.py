#SSL encrypted echo client
#
#
# ----------------------------------------------------------------------------------------------------------------------

import socket
import os
import sys
import ssl


def main(host, port):
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(cafile="ca.crt", capath=None)
    # context.verify_mode = ssl.CERT_OPTIONAL
    context.check_hostname = False
    # create a SSL connection
    ssl_sock = context.wrap_socket(s)
    ssl_sock.connect((host, port))
    # send the message
    ssl_sock.send(b'Hello, world!')
    # receive the message
    data = ssl_sock.recv(1024)
    print('Received', repr(data))
    # close the connection
    ssl_sock.close()  

if __name__ == "__main__":
    #parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <host> <port>")
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    main(host, port)