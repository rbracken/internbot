""" This is the interbot configuration file for the bot"""

# Address of the server
server = "brackyard.net"
# Server port
port = 6667
# Your bot's IRC nick
botnick = "internbot"
# Default channels to join
channels = ["#"+botnick] 
# Number of lines to remember per channel
memorysize = 500 


# Plugins list; default is empty list. Plugins are loaded in order of their listing.
plugins = ["ignore", "loadmod", "lmgtfy", "broadcast", "intern"]


