# Import some necessary libraries.
import sys, time
from server import *
from utils import *
from config import *


class Channel(Server):
    def __init__(self, owner, ircsock, channel, botnick, memorysize, modules):
        super(Channel, self).__init__(ircsock, botnick)
        self.owner = owner
        self.channel = channel
        self.memorysize = memorysize
        self.memory = []
        self.modules = owner.modules
        self.joinchan(self.channel)
        self.plugins = []
        for module in self.modules:
            self.plugins.append(module.Load(self))


    def elephant(self, msg):
        if msg.find("PRIVMSG"):
            try:
                privmsg = msg.split("PRIVMSG " + self.channel + " :")[1]
                usrname = msg.split('!')[0].split(':')[1]
                if len(self.memory) >= memorysize:
                    self.memory.pop(0)
                self.memory.append(usrname +": " +privmsg)
            except:
                pass


    def replay(self, criteria):
        if "last" in criteria.lower():
            line = len(self.memory) - int(criteria.lower().split("last ")[1])
            if line < 0 or line > len(self.memory):
                line = 0
            while line < len(self.memory):
                self.ircsock.send("PRIVMSG "+ self.channel +" :"+ self.memory[line]+"\n")
                line += 1
        elif "first" in criteria.lower():
            line = int(criteria.lower().split("first ")[1])
            temp = 0
            while temp < len(self.memory) and temp < line:
                self.ircsock.send("PRIVMSG "+ self.channel +" :"+ self.memory[line]+"\n")
                temp += 1
        elif "status" in criteria.lower() or "free" in criteria.lower():
            size = len(self.memory)
            self.ircsock.send("PRIVMSG "+ self.channel +" :"+"Currently memorized " + str(size) + " lines of this conversation." +"\n")
            self.ircsock.send("PRIVMSG "+ self.channel +" :"+ str(self.memorysize-size) + " additional slots remaining in buffer." +"\n") 
        else:
            self.ircsock.send("PRIVMSG "+ self.channel +" :"+"Say '" + self.botnick + "' replay <first/last/status> <numlines>"+"\n") 
    
    
    def read(self, ircmsg):
            # Necessary functions
            if ircmsg.lower().find(self.channel) != -1:
                self.elephant(ircmsg)
                
            if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("replay") != -1:
                self.replay(ircmsg.lower().split('replay')[1])
            
            elif ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("join") != -1:
                newchan = ircmsg.split("join")[1]
                newchan = newchan.strip()
                channels = []
                for channel in self.owner.channels:
                    channels.append(channel.channel)
                if newchan not in channels:
                    self.owner.channels.append(Channel(self.owner, self.ircsock, newchan, self.botnick, self.memorysize, self.modules))             
                
            elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("leave") != -1:
                self.sendmsg("Bye!")
                self.leavechan()
                del self.owner.channels[self.owner.channels.index(self)]
                del self
            
            else:
                for plugin in self.plugins:
                    if plugin.run(ircmsg) == True:
                        break


