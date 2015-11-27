import socket 
import random

""" Contains often used functions """

def connect(server, port, botnick):                  
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, port)) # Here we connect to the server using the port 6667
    ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :InternBot\n") # user authentication
    ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
    return ircsock

def pickone(alist):
    sumnum = random.random()
    sumnum = int(sumnum * len(alist))
    return alist[sumnum]

def ping(ircmsg, ircsock): # This is our first function! It will respond to server Pings.
    if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
        pingmsg = ircmsg.split(':')[1]
        ircsock.send("PONG :" + pingmsg + "\n")
        return True 

def listen(ircsock):
    ircmsg = ircsock.recv(2048) # receive data from the server
    ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server
    return ircmsg


