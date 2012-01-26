
# Look at the Legume library for entity interpolation.
import zlib
import socket
import struct
import inspect

import constants


class Connection():
    
    
    def __init__(self, host="127.0.0.1", port=constants.PORT, is_server=False):
        
        if is_server:
            host=""
            
        self._addr = (host, port)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(False)
        
        # Not sure how the following code will work on an external server.
        if is_server:
            self._socket.bind(self._addr)
        
        self._packets_to_send = []
        self._packets_received = []
        
        self._home_packet_counter = 0
        self._client_packet_counter = 0
        
    def update(self):
        data = None
        try:
            data, addr = self._socket.recvfrom(4096)
            print "Received message", data

        except Exception:
            pass
        
        if not data == None:
            message = _unpack(data)
            message.callback()
        
    def send(self, message):
        #format = "I" + message.format
        #data = [self._home_packet_counter] + packet.data
        
        message_format, message_packed = message._pack()
        print len(message_packed)
        #bits = struct.pack(format, *data)
        
        self._socket.sendto(message_packed, self._addr)
        #print struct.unpack(format, bits)
        
# format of a data packet is [id, [stuff]]
class BaseMessage(object):
    message_values = None
    
    def __init__(self):
        
        if self.message_values == None:
            raise Exception("message_values dict not set!")
            
        for val in self.message_values:
            self.__dict__[val] = None
    
    # Called when the packet is unpacked. This allows us to act upon the message.
    def callback(self):
        pass
    
    def get_message_id(self):
        return name_to_id[self.__class__.__name__]
              
    def _pack(self):
        
        format = ""
        data = []
        
        for val in self.message_values:
            datum = self.__dict__[val]
            if datum == None:
                raise Exception(val + " has not been assigned to in message " + self.__class__.__name__)
            
            data.append(datum)
            format = format + self.message_values[val]
            
        pack = struct.pack(format, *data)
        
        return format, struct.pack("II" + str(len(pack)) + "s", self.get_message_id(), len(pack), pack)

def _unpack(data):
    
    message_id, packet_length = struct.unpack_from("II", data, 0)

    a, b, packet_data = struct.unpack("II" + str(packet_length) + "s", data)
    packet = instance_from_name(id_to_name[message_id])
    
    format = ""
    for val in packet.message_values:
        format = format + packet.message_values[val]
    
    data = struct.unpack(format, packet_data)
    
    for val, data in zip(packet.message_values, data):
        
        # Right now the way strings are handled are goofy, because we fill them with padding.
        # This trims any padding characters from the string before we add it to our object.
        if isinstance(data, str):
            data = data.strip('\x00')
        
        packet.__dict__[val] = data
        
    
    return packet

import messages

id_to_name = {}
name_to_id = {}

def instance_from_name(name):
    return messages.__dict__[name]()
    
def register_messages():
    counter = 0
    for name, obj in inspect.getmembers(messages):
        if inspect.isclass(obj):
            
            id_to_name[counter] = name
            name_to_id[name] = counter
            
            counter = counter + 1


    q = instance_from_name(id_to_name[0])
    q.player_model_id = 2
    q.player_name = "hel loo"
    
    p = _unpack(q._pack()[1])
    p.callback()


