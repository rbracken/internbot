import time, urllib2

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.name = "lmgtfy"
     
     
    def run(self, ircmsg):

        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("search") != -1:
           return self.lmgtfy(ircmsg)
    
    
    def lmgtfy(self, ircmsg):
        try:
            search = urllib2.quote(ircmsg.split("search")[1])
            self.sendmsg("Let me google that for you:  " + "https://google.com/search?btnI=&q=" + search)
            return True
        except:
            self.sendmsg("I don't know how to google that")       
    
            
    def stop(self):
        pass
        

def stop():
    pass

