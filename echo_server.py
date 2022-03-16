#basic echo server
#
import socket
import sys
import threading

def main():
    #create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a port
    sock.bind(('localhost', 7001))
    #listen for connections
    sock.listen(5)
    #loop forever
    while True:
        #accept a connection
        clientsocket, address = sock.accept()
        #create a new thread to handle the connection
        t = threading.Thread(target=handle_connection, args=(clientsocket,))
        t.start()

def handle_connection(clientsocket):
    #loop forever
    while True:
        #read the data
        data = clientsocket.recv(1024)
        #if there is no data, break
        if data:
            #send the data to the server
            clientsocket.send(data)

if __name__ == '__main__':
    main()