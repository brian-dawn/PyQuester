# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.


import socket
import time

import constants




def main():
    host = "127.0.0.1"
    addr = (host, constants.PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    #sock.settimeout(0)
    sock.bind(addr)
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            print "Received message", data
            sock.sendto( "server says hai", addr)
        except Exception:
            pass
        
        
    sock.close()
    
if __name__ == '__main__':
    main()
