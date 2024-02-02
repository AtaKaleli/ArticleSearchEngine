import copy
import threading
from threading import *
import socket
import sqlite3



class ClientThread(Thread):

    #clientSocket represents connection
    def __init__(self, clientSocket, clientAddress):
        Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress



    def run(self):

        msg = "SERVER>>> connectionsuccess".encode()
        self.clientSocket.send(msg)
        clientMsg = self.clientSocket.recv(1024).decode()
        originalMessage = copy.deepcopy(clientMsg)
        clientMsg = clientMsg.split(";")
        while True:
            response = self.prepareResponse(clientMsg)
            self.clientSocket.send(response)
            clientMsg = self.clientSocket.recv(1024).decode()
            originalMessage = copy.deepcopy(clientMsg)
            clientMsg = clientMsg.split(";")

        msg = "SERVER>>> TERMINATE".encode()
        self.clientSocket.send(msg)
        print("Connection terminated - ", self.clientAddress)
        self.clientSocket.close()


    def prepareResponse(self, request):
        originalMessage = copy.deepcopy(request)
        # core loop that we will implement our functions
        while request[0] != "CLIENT>>> TERMINATE":
            print(originalMessage)
            startIssue = (request[1] + "-" + request[2])
            endIssue = (request[1] + "-" + request[3])
            print(startIssue)
            print(endIssue)
            conn = sqlite3.connect("articles.db")
            c = conn.cursor()
            c.execute("SELECT articletitle FROM article "
                      "WHERE issueno<=? AND  issueno>=?",(endIssue, startIssue))

            records = c.fetchall()
            if records:
                msg = ("SERVER>>> articlefound; " + str(records)).encode()
            else:
                msg = "SERVER>>> noarticle".encode()

            return msg


            clientMsg = self.clientSocket.recv(1024).decode()
            originalMessage = copy.deepcopy(clientMsg)
            clientMsg = clientMsg.split(";")






HOST = "127.0.0.1"
PORT = 5000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    serverSocket.bind((HOST, PORT))
except socket.error:
    print("Connection failed!")
    exit(1)
print("Waiting for connections")
while True:
    serverSocket.listen()
    clientSocket, clientAddress = serverSocket.accept()
    newThread = ClientThread(clientSocket, clientAddress)
    newThread.start()