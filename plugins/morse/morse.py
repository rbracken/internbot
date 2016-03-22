import codes
import random

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.name = "morse"
     
     
    def run(self, ircmsg):

        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("morse") != -1:
           return self.to_morse(ircmsg)
    
    
    def to_morse(self, ircmsg):
        try:
            text = ircmsg.split("morse")[1].strip().upper()
            code  = self.codify(text)
            self.sendmsg("Morse: " + code)
            return True
        except:
            self.sendmsg("I don't know how to codify that")
            return True
    
            
    def codify(self, text):
        code = ""
        
        for letter in text:
            code += codes.chars[letter] + " "
        
        return code
        
            
    def stop(self):
        pass
        

def stop():
    pass

