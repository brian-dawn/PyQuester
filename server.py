# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.


import socket
import time

import constants
import networking
import time



def main():
    networking.register_messages()
    connection = networking.Connection(is_server=True)
    while True:
        connection.update()
        time.sleep(.01)
        
        
    
if __name__ == '__main__':
    main()


