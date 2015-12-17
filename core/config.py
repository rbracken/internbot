""" This is the interbot configuration file for the bot"""

# Address of the server
server = "www.brack.xyz"
# Server port
port = 6667
# Your bot's IRC nick
botnick = "internbot"
# Default channels to join
channels = ["#"+botnick] 
# Number of lines to remember per channel
memorysize = 500 


# Plugins list; default is empty list. Plugins are loaded in order of their listing.
plugins = ["loadmod", "lmgtfy", "broadcast"]


