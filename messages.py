# All messages for networking must be created here.
# Each class must inherit from networking.BaseMessage and they
# must contain a message_values dictionary. Each class must also
# contain a callback function, they do not need to be defined in
# the class, if different behavior is needed depending on
# whether or not it is a client or server then it should not
# be handled here.

import util
import networking
import vector
            
class PlayerJoin(networking.BaseMessage):
    message_values = {
        'player_name'     : '10s',
        'player_model_id' : 'i'
    }
    
class EntityUpdate(networking.BaseMessage):
    message_values = {
        'x_pos'        : 'f',
        'y_pos'        : 'f',
        #'x_vel'        : 'f',
        #'y_vel'        : 'f',
        'tick'         : 'I'
    }
    
class InputState(networking.BaseMessage):
    message_values = {
        'direction'       : 'B', # Direction as an unsigned byte 0-255.
        'tick'            : 'I'
    }
    
        
class Text(networking.BaseMessage):
    message_values = {
        'player_name'     : 's',
        'player_model_id' : 'i'
    }
    
class PingReturn(networking.BaseMessage):
    message_values = {
        'milliseconds'    : 'i'
    }
    
    def callback(self, connection):
        
        print "Ping", (util.get_milliseconds() - self.milliseconds)

class Ping(networking.BaseMessage):
    message_values = {
        'milliseconds'    : 'i'
    }
    
    def __init__(self):
        super(networking.BaseMessage, self).__init__()
        
        self.milliseconds = util.get_milliseconds()
        
    def callback(self, connection):
        
        p = PingReturn()
        p.milliseconds = self.milliseconds
        connection.send(p)