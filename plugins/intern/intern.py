from config import *
import time
from core.utils import *
import markov

class Load():

    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.leavechan = chan.leavechan
        self.joinchan = chan.joinchan
        self.name = "intern"
        self.sendmsg("Caution: module 'intern' should be last loaded module." 
            + " Please `unloadmod intern` and `loadmod intern` if this is not the case")


    def run(self, ircmsg):

        if logchat == True:
            self.log(ircmsg)

        if ircmsg.lower().find(self.channel) != -1 and self.hello(ircmsg):
            return True
        elif ircmsg.lower().find(self.channel) != -1 and self.get_coffee(ircmsg):
            return True
        elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) and ircmsg.lower().find("coffee") != -1:
            self.sendmsg(pickone(coffees))
            return True
        elif ircmsg.lower().find(self.channel) != -1 and self.echo(ircmsg):
            return True
        elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("PRIVMSG") != -1:
            self.respond(ircmsg)
            return True


    def hello(self, ircmsg): # This function responds to a user that inputs "Hello Mybot"
        for entry in hellos:
                if ircmsg.lower().find(entry.lower() + " "+ self.botnick) != -1: 
                    self.sendmsg(pickone(hellos))
                    return True


    def get_coffee(self, ircmsg):
        if ircmsg.lower().find(self.botnick) and ircmsg.lower().find("get " + "coffee") != -1:
            self.sendmsg("Get coffee? Sure!") 
            self.leavechan()
            time.sleep(3)
            self.joinchan(self.channel)
            self.sendmsg( pickone(return_coffees))
            return True

    def echo(self, ircmsg):
        if ircmsg.lower().find(":" + self.botnick + " say") != -1: 
            repeat = ircmsg.split("say")
            self.sendmsg(repeat[1])
            return True

    def log(self, ircmsg):
        if ircmsg.lower().find(self.channel) != -1 and ircmsg.find("PRIVMSG") != -1:
            try:
                with open(logfile, 'a') as f:
                    f.write(ircmsg.split(self.channel + " :")[1] + " ")
            except:
                print "Couldn't log entry to file" 

    def respond(self, ircmsg):
        """ Generates text based on markov chains """
        try:
            text = ircmsg.lower().split(self.channel + " :")[0]
            file_ = open(logfile)
            kov = markov.Markov(file_)
            try:
                self.sendmsg(kov.generate_markov_response(seed_word=text.split()[-2], next_word=text.split()[-1]))
            except:
                self.sendmsg(kov.generate_markov_text())
        except:
            self.sendmsg(pickone(generics))
        return True

    def stop(self):
        pass


def stop():
    pass

