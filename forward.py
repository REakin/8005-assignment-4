#basic port fowarder for tcp using sockets and select

import socket
import os
import json
import threading
import sys
import ssl

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
        try:
            data = src.recv(1024)
            #if there is no data, pass
            if not data:
                pass
            #write the data to the destination
            dst.send(data)
        except:
            #if there is an error, break
            print("connection closed: \n" + "source: "+str(src.getpeername())+"\ndestination: "+str(dst.getpeername()))
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
        #print the connection info
        print("connection established: \n" + "source: "+str(clientsocket.getpeername())+" - destination: "+str(dst_socket.getpeername()))
        #create a new thread to forward the data
        t = threading.Thread(target=forward, args=(clientsocket, dst_socket))
        t.start()
        t2 = threading.Thread(target=forward, args=(dst_socket, clientsocket))
        t2.start()

def handle_ssl_connections(port, dest,cafile):
    #create the main socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a port
    serversocket.bind(('localhost', port))
    #listen for connections
    serversocket.listen(5)
    #create the destination
    dst = (dest[0], dest[1])
    #create the ssl context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(cafile=cafile, capath=None)
    context.check_hostname = False
    #loop forever
    while True:
        #accept a connection
        clientsocket = serversocket.accept()[0]
        #create a new socket for the destination
        dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #wrap the socket with ssl
        dst_socket = context.wrap_socket(dst_socket)
        #connect to the destination
        dst_socket.connect(dst)
        #print the connection info
        print("SSL connection established: \n" + "source: "+str(clientsocket.getpeername())+" - destination: "+str(dst_socket.getpeername()))
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
        if o['ssl']:
            t=threading.Thread(target=handle_ssl_connections, args=(o['source'], o['dest'],o['ssl_cert']))
        else:
            t = threading.Thread(target=handle_connections, args=(o['source'], o['dest']))
        t.daemon = True
        t.start()  
        threads.append(t)
    #loop forever
    while True:
        #get input from the keyboard
        command = input()
        #if the command is quit, exit
        if command == 'quit':
            #exit
            sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting by user request.\n")
        sys.exit(0)