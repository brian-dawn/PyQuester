# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.
import legume
import time

import constants

def main():
    s = legume.Server()
    s.listen(('', constants.PORT))

    t = time.time()
    print "server: started."
    while True:
        s.update()

        if time.time() > t + 1.0:
            t = time.time()
            for peer in s.peers:
                print peer.address, peer.latency

        time.sleep(0.0001)

if __name__ == '__main__':
    main()