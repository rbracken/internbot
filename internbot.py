from core.config import * 
from core.bot import Bot
import time

#Initialize Bot
internbot = Bot(server, port, channels, botnick, memorysize, plugins)

#Wait loop to catch user input
# TODO find better implementation
while 1:
    try:
        time.sleep(1)
    except:
        internbot.halt = 1 
        exit()
        
