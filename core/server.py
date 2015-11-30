# Import some necessary libraries.
import socket 
import time
import sys


class Server(object):

    def __init__(self, ircsock, botnick):
        self.botnick = botnick
        self.ircsock = ircsock
    

    def sendmsg(self, msg):
        ''' Sends messages to the channel '''
        self.ircsock.send("PRIVMSG "+ self.channel +" :"+ msg +"\n") 
        if len(self.memory) >= self.memorysize:
            self.memory.pop(0)
        self.memory.append(self.botnick +": " +msg)


    def joinchan(self, chan):
        self.ircsock.send("JOIN "+ chan +"\n")


    def listen(self):
        ''' Grab messages from the TCP socket to the server '''
        ircmsg = self.ircsock.recv(2048)
        ircmsgs = ircmsg.splitlines() 
        print(ircmsg) # Print incoming message (unformatted)
        return ircmsgs


    def leavechan(self):
        self.ircsock.send("PART "+ self.channel +"\n")

