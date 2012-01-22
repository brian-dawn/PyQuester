
from subprocess import Popen

client = Popen(["python", "main.py"])
server = Popen(["python", "server.py"])

client.wait()
server.kill()

print "server closed."
