#basic port fowarder for tcp using sockets and select

import socket
import os
import json
import threading
import sys


def config():
    #open the config file
    with open('config.json', "r") as f:
        #read the file
        data = json.load(f)
    #return the data
    return data

def forward(src, dst):
    #loop forever
    while True:
        #read data from the source
        data = src.recv(1024)
        #if there is data send it to the destination
        if data:
            dst.send(data)
        #if there is no data, break
        else:
            break


def handle_connections(port, dest):
    #create the main socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a port
    serversocket.bind(('localhost', port))
    #listen for connections
    serversocket.listen(5)
    #create the destination
    dst = (dest[0], dest[1])
    #loop forever
    while True:
        #accept a connection
        clientsocket = serversocket.accept()[0]
        #create a new socket for the destination
        dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #connect to the destination
        dst_socket.connect(dst)
        #create a new thread to forward the data
        t = threading.Thread(target=forward, args=(clientsocket, dst_socket))
        t.start()
        t2 = threading.Thread(target=forward, args=(dst_socket, clientsocket))
        t2.start()


def main():
    #get the config
    #create sockets for the ports
    threads = []
    for o in config():
        t = threading.Thread(target=handle_connections, args=(o['source'], o['dest']))
        t.start()  
        threads.append(t)
    #wait for the threads to finish
    for t in threads:
        t.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting by user request.\n")
        sys.exit(0)