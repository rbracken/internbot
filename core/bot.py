# Import some necessary libraries.
import time
import sys, time
import importlib
import traceback

#Base modules and configurations
from utils import *
from server import *
from channel import *


class Bot(Server):
    def __init__(self, server, port, channels, botnick, memorysize, plugins):
        # Init server class
        super(Bot, self).__init__(connect(server,port,botnick), botnick)
        # Import plugins
        self.modules = []
        for plugin in plugins:
            module = importlib.import_module("plugins.%s" % plugin)
            self.modules.append(module)
        self.channels = []
        for channel in channels:
            time.sleep(1)
            self.channels.append(Channel(self, self.ircsock, channel, botnick, memorysize, self.modules))
        self.listener() 
     
    def listener(self):
        while 1: # Be careful with these! it might send you to an infinite loop
            try:
                ircmsg = listen(self.ircsock)
                ping(ircmsg, self.ircsock)
                for channel in self.channels:
                    channel.read(ircmsg)
            except:
                print "\nError caught:", sys.exc_info()[0]
                print "\nStarting shutdown\n"
                for module in self.modules:
                    module.stop()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.print_exception(exc_type, exc_value, exc_traceback) 
                exit()


