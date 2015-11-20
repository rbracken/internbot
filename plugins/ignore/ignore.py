from config import *
import time

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.leavechan = chan.leavechan
        self.joinchan = chan.joinchan
        self.name = "ignore"
        self.sendmsg("Caution: module 'ignore' should be first loaded module")
     
    def run(self, ircmsg):
        
        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1:
            user = ircmsg 
            user = user.lower().split(":")[1].split('!')[0]
            if user in blacklist:
                self.sendmsg("I don't take orders from you, " + user + "!")
                return True
            elif "unignore" in ircmsg.lower() and not "loadmod" in ircmsg.lower() :
                ignuser = ircmsg.lower().split("unignore")[1].strip()
                if ignuser in blacklist:
                    self.sendmsg("Unignoring " + ignuser + " from now on")
                    del blacklist[blacklist.index(ignuser)]
                else:
                    self.sendmsg("User not ignored")   
                return True
            elif "ignore" in ircmsg.lower() and not "loadmod" in ircmsg.lower():
                ignuser = ircmsg.lower().split("ignore")[1].strip()
                if ignuser not in blacklist:
                    blacklist.append(ignuser)
                    self.sendmsg("Ignoring " + ignuser + " from now on")
                else:
                    self.sendmsg("Already ignoring " + ignuser)
                return True
    
            
    def stop(self):
        pass
        

def stop():
    pass

