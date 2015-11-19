import importlib
import sys

class Load():
    
    def __init__(self, chan):
        self.channel = chan.channel
        self.botnick = chan.botnick
        self.sendmsg = chan.sendmsg
        self.owner = chan.owner
        self.name = "loadmod"
     
     
    def run(self, ircmsg):

        if ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("unloadmod") != -1:
           return self.unloadmod(ircmsg)
        elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("loadmod") != -1:
           return self.loadmod(ircmsg)
        elif ircmsg.lower().find(self.channel) != -1 and ircmsg.lower().find(self.botnick) != -1 and ircmsg.find("lsmod") != -1:
           return self.lsmod()
    
    def loadmod(self, ircmsg):
        try:
            import plugins
            reload(plugins)
            plugin = (ircmsg.split("loadmod")[1])
            if "plugins." + plugin.strip() in sys.modules:
                self.sendmsg("Module already loaded")
                return True
            module = importlib.import_module("plugins.%s" % plugin.strip())
            self.owner.modules.append(module)
            for channel in self.owner.channels:
                channel.plugins.append(module.Load(channel))
            self.sendmsg("Loaded module")
            return True
        except:
            self.sendmsg("No module known by that name")
            return True     

    def unloadmod(self, ircmsg):
        try:
            plugin = (ircmsg.split("unloadmod")[1])
            if "plugins." + plugin.strip() not in sys.modules:
                self.sendmsg("Module not loaded")
                return True
            del self.owner.modules[self.owner.modules.index(sys.modules["plugins."+plugin.strip()])]
            del sys.modules["plugins."+plugin.strip()]
            for channel in self.owner.channels:
                print channel.plugins
                for plug in channel.plugins:
                    if plug.name == plugin.strip():
                        del channel.plugins[channel.plugins.index(plug)]
            self.sendmsg("Unloaded module")
            return True
        except:
            self.sendmsg("Could not unload")
            return True  
    
    def lsmod(self):
        modules =  str(self.owner.modules)
        self.sendmsg("Modules loaded: " + modules)
        return True
            
    def stop(self):
        pass
        

def stop():
    pass

