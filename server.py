# This will handle collision detection, world generation, etc.

# Design the entire thing so that it only uses one thread, with sockets that should be possible.
# We may want to instead build some reliability abstraction ourselves.
# Lets look into Twisted, it might be possible.


import socket
import time

import constants
import networking

import messages
import util
import vector

x_pos = y_pos = x_vel = y_vel = 0
last_tick = 0
def main():
    global x_pos, y_pos
    networking.register_messages()
    connection = networking.Connection(is_server=True)
    
    
    target_fps = 60
    old_time = 0
    counter = 0
    while True:
        connection.update()
        time.sleep(.001)
        
        new_time = util.get_milliseconds()
        if (new_time - old_time) >= 1000.0 / target_fps:
            old_time = new_time
            
            x_pos = x_pos + x_vel
            y_pos = y_pos + y_vel
            
            counter = counter + 1
            if counter == 50:
                counter = 0
                print x_pos, y_pos
                send_player_state(connection)
            
        #connection.send(messages.Ping())

def send_player_state(connection):
    e = messages.EntityUpdate()
    e.x_pos = x_pos
    e.y_pos = y_pos
    e.tick = last_tick
    #print last_tick
    
    connection.send(e)
    
def on_input_state(m, connection):
    global x_vel, y_vel, last_tick, x_pos, y_pos
    vec = vector.get_vector(m.direction)
    x_vel = vec[0] * 5
    y_vel = vec[1] * 5

    
    
    last_tick = m.tick
    send_player_state(connection)
    
    
messages.InputState.callback = on_input_state
       
    
if __name__ == '__main__':
    main()


