#SSL encrypted echo server
#
#
# ----------------------------------------------------------------------------------------------------------------------

import socket
import ssl
import sys

def main(filepath):
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen on port 8001
    s.bind(('', 8001))
    s.listen(1)
    # create a SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # load the certificate
    context.load_cert_chain(certfile=filepath, keyfile=filepath)
    # create a SSL connection
    while True:
        conn, addr = s.accept()
        # create a SSL connection
        ssl_sock = context.wrap_socket(conn, server_side=True)
        # receive the message
        data = ssl_sock.recv(1024)
        print('Received', repr(data))
        # send the message
        ssl_sock.sendall(data)
        # close the connection
        ssl_sock.close()


if __name__ == "__main__":
    #parse command line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <filepath>")
        sys.exit()
    filepath = sys.argv[1]
    main(filepath)