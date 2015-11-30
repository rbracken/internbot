# Import some necessary libraries.
import time
import sys, time
import importlib
import traceback
import threading

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
                     
        # Spawn thread to listen on port
        self.channels = []
        t_listen = threading.Thread(target=self.listener)
        t_listen.start()
        time.sleep(3) 
        
        # Create channel instances
        for channel in channels:
            self.channels.append(Channel(self, self.ircsock, channel, botnick, memorysize, self.modules))
            time.sleep(0.5)
        
        # Wait on thread exit 
        t_listen.join()
        
     
    def listener(self):
        #Polls to get traffic from socket 
        while 1: 
            try:
                ircmsgs = self.listen()
                for ircmsg in ircmsgs:
                    if ping(ircmsg, self.ircsock):
                        break
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


