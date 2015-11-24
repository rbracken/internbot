
def stop(): 
    pass

class Load():
    def __init__(self, chan):
        self.channel = chan.channel
        self.all_channels = chan.owner.channels
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.name = "broadcast"
        
     
    def run(self, ircmsg):
        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1:
            if ircmsg.lower().find("broadcast") != -1:
                try:
                    msg = ircmsg.split("broadcast")[1]
                    for channel in self.all_channels:
                        channel.sendmsg(msg)
                finally:
                    return True

     
    def __del__(self):
        pass
        
        
        
