# All messages for networking must be created here.

import networking
    

            
class PlayerJoin(networking.BaseMessage):
    message_id = 100
    message_values = {
        'player_name'     : '10s',
        'player_model_id' : 'i'
    }
    
    def callback(self):
        print self.player_name, self.player_model_id
    
    
class Text(networking.BaseMessage):
    message_id = 100
    message_values = {
        'player_name'     : 's',
        'player_model_id' : 'i'
    }
    
    def callback(self):
        print self.player_name

