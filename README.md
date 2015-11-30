# Internbot
InternBot - The modular IRC intern


# Description
Internbot is a python irc bot that offers the ability to easily and quickly write plugins
for adding functionality specific to *your* situation. It is written as a set of modular
python packages which are imported into the base bot to add functionality. Plugins can
be loaded beforehand and also swapped in/out at runtime according to the users' need.


# Background
This bot was borne out of a joke at my work that an intern's function can be automated away
with a simple script - thus the name! 


# Bundled Plugins
As its name implies, it comes bundled with plugins to mock-up some intern-like behaviour 
(dig into the 'intern' plugin for more details). Included in the base package are:
- intern : The quintessential intern plugin. Namesake of internbot, most of the original
    bot functionality is encapsulated entirely in this plugin. If loaded, it should be 
    loaded as the last module, to allow proper responses to unknown commands. Commands:
    - `<botnick> get coffee` : when get coffee is found in a message, internbot will 
        part/rejoin with "coffee"
    - `<botnick> say <msg>` : repeat a phrase to the channel
    - `coffee` : Any time the word coffee is mentioned in the 
- lmgtfy : Goes out to google and returns the first "I'm Feeling Lucky" result. Commands:
    - `<botnick> search <phrase>` : Gets the first "I'm Feeling Lucky" page matching <result>
- broadcast : Broadcast messages to all channels internbot has joined. Commands:
    - `<botnick> broadcast <msg>` : Send this message to all channels
- ignore : Ban people from giving internbot commands. Commands:
    - `<botnick> ignore <nick>` : add user to blacklist
    - `<botnick> unignore <nick> : remove user from blacklist 
- loadmod : This module provides the on-the-fly loading/unloading of other modules. 
    If this module is not loaded in the config, you will NOT be able to swap in/out modules
    at runtime! Be aware that it IS possible for users to get the module to unload itself, 
    forcing internbot to be unable to further load new modules on-the-fly. Commands:
    - `<botnick> loadmod <pluginname>` : load the requested plugin into internbot
    - `<botnick> unloadmod <pluginname>` : if loaded, unload the requested plugin from 
        internbot.
- roku : Specialty module, which connects out to ROKU internet radio boxes to display
    marquee text on their displays. Text is displayed until changed or this module is un-
    loaded. Tested and works with ROKU models M1000 and M1001. Commands:
    `<botnick> update roku <message>` : Display a rotating marquee message on ROKU
    `<botnick> show roku` : Print the current message being displayed on ROKU


# Built-in commands:
Some commands are important enough they deserved to be built-in to internbot. These include:

- `<botnick> join <chan>` : Join a new channel
- `<botnick> leave` : Leave the current channel


# Issuing commands
Issuing commands is simple -- simply include the botname in a message to a channel it is
currently in, and the the command desired, eg. `internbot get coffee`. It follows the general
pattern of `<botnick> <command> <args>`. Of course, some modules can circumvent this, 
as the `intern` module does, by simply looking for keywords in *any* text regardless of
whether or not the botnick is mentioned.

If you are joined to the <botnick> channel, you do not need to preface commands with the
bot's nickname. It will read commands directly as if all messages were prefaced with the
bot's nickname.


# Install and Configuration
Simply download / clone into your directory of choice, and run the bot from its root 
directory with `python internbot.py`. Tested with python2.7 - there might be
issues with `super()` when running with python3 - use python2.7 for best results.

The config file is located at `core/config.py`, with the following options:

- server : the address / IP of the IRC server
- port : port on which the IRC server responds. By default, it's port 6667
- botnick : your bot's nickname. By default, it's "internbot"
- channels : channels which your bot will join on start. By default, it will only join
    #<botnick>. Channels can be either added here, or joined by issuing command 
- memorysize : determines how many lines of chat will be recorded/logged per channel. 
    Set to '0' to disable chat logging.
- plugins : list of plugins to be loaded on start. Plugins are loaded IN ORDER, which CAN 
    affect the proper operation of some plugins. If the `loadmod` module is loaded, then
    plugins can also be loaded on-the-fly once internbot is started.
    
In addition, each plugin will have its own `config.py` file located in its folder in the 
`plugins/` directory.


# Building plugins/modules
Internbot allows customization through quick and easy module building. From within modules 
and plugins, the user has the ability to modify and access all of the parent classes and 
their attributes for maximum flexibility. Plugins can range from simple, stand-alones that
return dialogue to complex ones which run background tasks as daemons.

A good example for a beginner plugin can be found in the `plugins/broadcast/` directory. A
more complex example, which requires spawning a thread + having background tasks can be
seen in the roku plugin, in `plugins/roku/`.

Mandatory components:
In your plugin's folder:
- __init__.py : this will tell internbot that this is a plugin package. In it, you
    import your plugin, like so: `from yourpluginname import *`
- yourmodulename.py : the actual code for your plugin/module. This file should contain
    a set of mandatory classes, methods and function definitions (outlined below) as
    well as any additional code to make the plugin function.
- config.py (optional) : your plugin's config file

In yourmodulename.py:
- class Load() : this class is the instance of your plugin. It must contain the following:
    - def __init__(self, channel): All the setup code for the plugin. `channel` is a 
        a reference to the parent Channel() object which is *always* passed in.
    - def __del__(self): when the module is unloaded or internbot quits, this code will
        be executed for cleanup. Complex modules with background tasks or plugins
        which modify channel methods will want to add cleanup code here.
    - def run(self, ircmsg): this method is called every time a new message is inter-
        cepted by internbot. `ircmsg` is the raw textline that was recieved from the 
        IRC server. If your module does not require interaction at runtime, simply
        define this with `pass`.
 - def stop(): this is called when unloading the module or when internbot quits. If 
    there are background tasks running, this method can be used to stop them. If no
    cleanup is needed on halt or unload, then simply define this with `pass`
   
 In addition, the Load() class must include the attribute `self.name`, which should be
 identical to the the file name of yourmodulename.py

    
    
