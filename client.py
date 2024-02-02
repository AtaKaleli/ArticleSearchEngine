import socket
from tkinter import *
from tkinter import messagebox
import copy
import time
import re

class Article(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("Articles")


        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.yearLbl = Label(self.frame1, text="Year: ")
        self.yearLbl.pack(side=LEFT, padx=5, pady=5)

        self.yearEntry = Entry(self.frame1, name="year")
        self.yearEntry.pack(padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.monthLbl = Label(self.frame2, text="Month No: ")
        self.monthLbl.pack(side=LEFT, padx=5, pady=5)

        self.endMonthEntry = Entry(self.frame2, name="endmonth")
        self.endMonthEntry.pack(side=LEFT, padx=5, pady=5)

        self.startMonthEntry = Entry(self.frame2, name="startmonth")
        self.startMonthEntry.pack(padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.optionList = [
            ("Single Author", BooleanVar())
        ]

        for option in self.optionList:
            self.selectOption = Checkbutton(self.frame3, anchor=W, text=option[0], variable=option[1])
            self.selectOption.pack(expand=YES, fill=BOTH, padx=5, pady=5)

        # self.bookDict = {}  # keys are unique IDs, values are bookName + author
        # for bookInfo in bookData:
        #     nameAndAuthorTuple = (bookInfo[1] + " by " + bookInfo[2], BooleanVar())
        #     self.bookDict[bookInfo[0]] = nameAndAuthorTuple
        #
        # for bookID, nameAndAuthor in self.bookDict.items():
        #     self.selectBookName = Checkbutton(self.frame2, anchor=W, text=nameAndAuthor[0], variable=nameAndAuthor[1])
        #     self.selectBookName.pack(expand=YES, fill=BOTH, padx=5, pady=5)

        self.frame4 = Frame(self)
        self.frame4.pack(padx=5, pady=5)

        self.getArticlesBtn = Button(self.frame4, text="Get Articles", command=self.buttonPressedGetArticles)
        self.getArticlesBtn.pack(side=LEFT,padx=5, pady=5)

        self.closeBtn = Button(self.frame4, text="Close", command=self.buttonPressedClose)
        self.closeBtn.pack(padx=5, pady=5)

    def buttonPressedGetArticles(self):
        year = self.yearEntry.get()
        startMonth = self.startMonthEntry.get()
        endMonth = self.endMonthEntry.get()
        singleAuthor = 0
        for option in self.optionList:
            if option[1].get():
                singleAuthor = 1
            else:
                singleAuthor = 0

        if year == "" or startMonth == "" or endMonth == "":
            messagebox.showerror("error", "Missing value(s)")
        elif int(endMonth) < int(startMonth):
            messagebox.showerror("error", "Invalid range")
        else:
            clientMsg = ";" + year + ";" + startMonth + ";" + endMonth + ";" + str(singleAuthor)
            msg = ("CLIENT>>> " + clientMsg).encode()
            clientSocket.send(msg)
            serverMsg = clientSocket.recv(1024).decode()
            print(serverMsg)
            serverMsg = serverMsg.split(";")  # after getting server message, I splitted it
            if serverMsg[0] == "SERVER>>> noarticle":
                messagebox.showerror("Error", "No article!")
            else:

                articleData = eval(serverMsg[1])
                articleInfo = ""
                for data in articleData:
                    articleInfo += "Name: " + data[0] + "\n"
                messagebox.showinfo("Info", articleInfo)





    def buttonPressedClose(self):
        pass














HOST = "127.0.0.1"
PORT = 5000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect((HOST, PORT))
except socket.error:
    print("Connection error!")



serverMsg = clientSocket.recv(1024).decode()
if serverMsg == "SERVER>>> connectionsuccess":
    print(serverMsg)
    window = Article()
    window.mainloop()



    # serverMsg = clientSocket.recv(1024).decode()

else:
    msg = "CLIENT>>> TERMINATE".encode()
    clientSocket.send(msg)
    print("Connection terminated! ")
    clientSocket.close()
