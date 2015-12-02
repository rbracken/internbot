# Import some necessary libraries.
import sys, time
from utils import *
from config import *
from channel import *


class Privmsg(Channel):
    """ Wraps around channel class to provide private message capabilities """
    def __init__(self, owner, ircsock, botnick, memorysize, modules):
        self.ircsock = ircsock
        self.owner = owner
        self.channel = botnick
        self.botnick = botnick
        self.memorysize = memorysize
        self.memory = []
        self.modules = owner.modules
        self.plugins = []
        self.sender = None
        for module in self.modules:
            self.plugins.append(module.Load(self))
    
    
    def read(self, ircmsg):
            # Reset the sender so messages don't randomly get sent back
            self.sender = None
            # Check if the message
            badval = "#" + self.channel + " :"
            if ircmsg.lower().find(self.channel) != -1 and badval not in ircmsg.lower():
                self.elephant(ircmsg)
                self.sender = ircmsg.split('!')[0].split(':')[1]
                
                if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("replay") != -1:
                    self.replay(ircmsg.lower().split('replay')[1])
                
                elif ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("join") != -1:
                    newchan = ircmsg.split("join")[1]
                    newchan = newchan.strip()
                    channels = []
                    for channel in self.owner.channels:
                        channels.append(channel.channel)
                    if newchan not in channels:
                        self.owner.channels.append(Channel(self.owner, self.ircsock, newchan, 
                            self.botnick, self.memorysize, self.modules))             
                
                else:
                    for plugin in self.plugins:
                        if plugin.run(ircmsg) == True:
                            break               
        
               
    def sendmsg(self, msg, remember=True):
        ''' Overrides the default sendmsg, allowing PM'ing '''
        if self.sender != None:
            self.ircsock.send("PRIVMSG "+ self.sender +" :"+ msg +"\n") 
            if remember == True: 
                if len(self.memory) >= self.memorysize:
                    self.memory.pop(0)
                self.memory.append(self.botnick +": " +msg)


