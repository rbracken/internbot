from choices import *
import random

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.name = "pick"
     
     
    def run(self, ircmsg):

        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("pick") != -1:
           return self.pick(ircmsg)
    
    
    def pick(self, ircmsg):
        try:
            options = situations[ircmsg.split("pick")[1].strip().lower()]
            choice = random.choice(options)
            self.sendmsg("I say... pick " + choice)
            return True
        except:
            self.sendmsg("I don't know how to pick that")
            return True
    
            
    def stop(self):
        pass
        

def stop():
    pass

