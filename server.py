# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.
import socket

import threading

class StoppableThread(threading.Thread):

    def __init__(self, target):
        super(StoppableThread, self).__init__(target=target)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


 
def start():
    global thread
    thread = StoppableThread(target=run)
    thread.start()
    
    
def stop():           
    thread.stop() 

def run():
    UDP_IP="127.0.0.1"
    UDP_PORT=5005
    
    #print "starting server."

    sock = socket.socket( socket.AF_INET, # Internet
                          socket.SOCK_DGRAM ) # UDP
                          
    sock.setblocking(False)
    sock.bind( (UDP_IP, UDP_PORT) )
    
    while not thread.stopped():
        #print thread.stopped()
        data, addr = sock.recv_from( 1024 ) # buffer size is 1024 bytes
        print "received message:", data
        
    print "server: stopping."
    