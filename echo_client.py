#echo client

import socket
import sys

def main():
    #create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server
    sock.connect(('localhost', 8001))
    while True:
        #read the data
        data = input('> ')
        #if there is no data, break
        if not data:
            break
        #send the data to the server
        sock.send(data.encode())
        #recieve the data from the server
        data = sock.recv(1024)
        #if there is no data, break
        if not data:
            break
        #print the data
        print(data.decode())


if __name__ == '__main__':
    main()