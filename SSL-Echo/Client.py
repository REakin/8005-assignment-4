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
    # connect to the server
    s.connect((host, port))
    # create a SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # create a SSL connection
    ssl_sock = context.wrap_socket(s)
    # send the message
    ssl_sock.sendall(b'Hello, world!')
    # receive the message
    data = ssl_sock.recv(1024)
    print('Received', repr(data))
    # close the connection
    ssl_sock.close()  

if __name__ == "__main__":
    #parse command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <host>")
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    main(host, port)