from config import *
import telnetlib, threading, sys, time

# Globals
instance = None

def stop():
    global instance    
    instance.stop()


class RokuMessage():
    def __init__(self, message):
        self.message = message
        self.stop = False


class RokuListener():

    def __init__(self):
        self.roku_message = RokuMessage(default_roku_message)
        self.thread = threading.Thread(target=self.roku, args=([self.roku_message]))
        self.thread.start()

    def roku(self, roku_struct):
        """
        open telnet port to soundbridge
        go into sketch subshell
        quit out of sketch subshell to release display
        """
        tn = telnetlib.Telnet(address, port)
        while not roku_struct.stop:                            # run forever
            tn.read_until("SoundBridge> ")      # wait for prompt from soundbridge
            tn.write("sketch\n")                # use this session to enter sketch subshell
            tn.read_until("sketch> ")           # wait for prompt
            tn.write("marquee \"" + roku_struct.message +"\"\n")
            time.sleep(1)
            tn.read_until("sketch> ")
            time.sleep(1)
            tn.write("quit\n")                  # exit sketch subshell, clears display
            tn.write("\n")

    def stop(self):
        self.roku_message.stop = True

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.name = "roku"
        global instance
        if instance == None:
            instance = RokuListener()
     
    def run(self, ircmsg):
        global instance
        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("update roku") != -1:
            self.sendmsg("Updating roku")

            instance.roku_message.message = ircmsg.split("roku")[1]
            return True
                    
        elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("show roku") != -1:  
            self.sendmsg("Current roku message: \"" + instance.roku_message.message + "\"")
            return True
    
    def stop(self):
        global instance
        instance.stop()
        instance = None 
    
    def __exit__(self):
        self.stop()
    
    def __del__(self):
        self.stop()


