#echo client

from email import message
import socket
import sys

def main():
    #create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect to the server
    sock.connect(('localhost', 8000))
    while True:
        #read the data
        message = input('> ')
        #send the data to the server
        sock.send(message.encode())
        #recieve the data from the server
        data = sock.recv(1024)
        #if there is no data, break
        if not data:
            print('No data received')
            break
        #print the data
        print(data.decode())
        break
    #close the socket
    sock.close()


if __name__ == '__main__':
    main()