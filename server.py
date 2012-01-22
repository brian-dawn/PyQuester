# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.

import twisted.internet.task
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


import constants

class Helloer(DatagramProtocol):

    def startProtocol(self):
        host = "127.0.0.1"
        port = constants.PORT

        self.transport.connect(host, port)
        print "now we can only send to host %s port %d" % (host, port)
        self.transport.write("hello") # no need for address

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

    # Possibly invoked if there is no server listening on the
    # address to which we are sending.
    def connectionRefused(self):
        print "No one listening"


def main():
    scheduleUpdate = twisted.internet.task.LoopingCall(loop)
    scheduleUpdate.start(1.0 / 60.0, False)   # 60 Hz

    # 0 means any port, we don't care in this case
    reactor.listenUDP(constants.PORT, Helloer())
    reactor.run()
    
def loop():
    print "hai"
    

"""
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
"""
if __name__ == '__main__':
    main()
