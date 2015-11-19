# Import some necessary libraries.
import socket 
import time
import sys


class Server(object):

    def __init__(self, ircsock, botnick):
        self.botnick = botnick
        self.ircsock = ircsock
    

    def sendmsg(self, msg): # This is the send message function, it simply sends messages to the channel.
        self.ircsock.send("PRIVMSG "+ self.channel +" :"+ msg +"\n") 
        if len(self.memory) >= self.memorysize:
            self.memory.pop(0)
        self.memory.append(self.botnick +": " +msg)


    def joinchan(self, chan): # This function is used to join channels.
        self.ircsock.send("JOIN "+ chan +"\n")


    def listen(self):
        ircmsg = self.ircsock.recv(2048) # receive data from the server
        ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
        return ircmsg


    def leavechan(self):
        self.ircsock.send("PART "+ self.channel +"\n")

