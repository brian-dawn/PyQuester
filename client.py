# PyQuester
#

# Must be done (on Windows) before we append dlls to the system path.
import constants

# Handle Windows, append dlls to the system path.
import os
import sys
import inspect
if os.name == "nt":
    cmd_folder = os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]) + \
                 "\\bin\windows"
    
    if cmd_folder not in sys.path:
        
        sys.path.insert(0, cmd_folder)
        os.environ['PATH'] = cmd_folder + ';' + os.environ['PATH']

import datetime
import random
import sf
import socket
import time

# Seed the random number generator before we import anything (just in case).
random.seed(7)

# We have to create the window as we need a rendering context for loading textures.
# This can likely be cleaned up later by controlling all the main imports down below.
width = 800
height = 600
window = sf.RenderWindow(sf.VideoMode(width, height),
                         'PyQuester')
import camera
camera.width = width
camera.height = height

import media
import plugins
import networking
import messages
import util
import vector

from tile import Tile
from light import Light
from level import Level


actions = [] # Keep track of all recorded actions (one added each tick) untill we receive an update from the server.
             # Then we use this to replay all the actions the player took.
last_x = last_y = 0
last_tick = 0
command_counter = 0
def main():
    global actions, command_counter
    # Load the tiles folder.
    media.load_textures()
    plugins.load(plugins.tiles, "tiles")
    plugins.load(plugins.effects, "effects")
    plugins.load(plugins.lights, "lights")
    plugins.load(plugins.workers, "workers", needs_id=False)
    
    
    networking.register_messages()
    
    
    window.framerate_limit = 60
    window.vertical_sync_enabled = True
    running = True

    old_direction = 0
    speed = 5
    command_counter = 0
    
    connection = networking.Connection()

    # FPS variables.
    frame_counter = 0
    fps = 0
    old_time = datetime.datetime.now()
    
    # Camera variables.
    speed = 10
    
    em = plugins.get_effect("fire").Effect(0, 0)
    #print dir(em)
    level = Level()
    plugins.get_worker("sample_worker").crap_work(level, 2, "stone_wall")
    while running:

        
        for event in window.iter_events():
            if event.type == sf.Event.CLOSED:
                running = False

        if sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
            running = False

        # Super basic camera controls.
        if sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
            camera.y = camera.y + speed            
        if sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
            camera.y = camera.y - speed
        if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
            camera.x = camera.x - speed
        if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
            camera.x = camera.x + speed           
        
        
        direction = 0
        if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            direction = direction + vector.DOWN           
        if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            direction = direction + vector.UP 
        if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
            direction = direction + vector.LEFT 
        if sf.Keyboard.is_key_pressed(sf.Keyboard.D):
            direction = direction + vector.RIGHT 
            
        connection.update()
        command_counter = command_counter + 1
        if not direction == old_direction:
            old_direction = direction
            
            
            message = messages.InputState()
            message.direction = direction
            message.tick = command_counter
            
            
            connection.send(message)

        if not direction == 0:
            actions.append((command_counter, direction))
            
        
        
        
        x_pos = last_x #util.lerp(float(inter_x), float(last_x), len(actions) / 80.0)
        y_pos = last_y #util.lerp(float(inter_y), float(last_y), len(actions) / 80.0)

        #for d in actions:
        #    if d[0] <= last_tick:
        #        actions.remove(d)
        #print len(actions)
                
        for d in actions:

            x, y = vector.get_vector(d[1])
            
            x_pos = x_pos + x * 5
            y_pos = y_pos + y * 5
                

        #print last_tick, command_counter 

        #print x_pos, y_pos
        
        
        
        
        window.clear(sf.Color.BLACK)
        #window.draw(sprite)
        
        #Draw the tiles.
        level.update()
        level.draw(window)
        
        # Calculate mouse coordinates.
        xp = int(sf.Mouse.get_position(window)[0] + camera.x)
        yp = int(sf.Mouse.get_position(window)[1] + camera.y)
        # Draw fps text.
        t = sf.Text(str(fps) + " x:" + str(xp) + " y:" + str(yp))
        t.color = sf.Color(155,55,55);
        window.draw(t)
        
        em.update()
        em.draw(window)
        
        rect = sf.Shape.rectangle(x_pos - camera.x, y_pos - camera.y, 50, 50, sf.Color.WHITE)
        window.draw(rect)
        
        window.display()
        
        # Calculate the FPS.
        frame_counter = frame_counter + 1
        new_time = datetime.datetime.now()
        if new_time.second - old_time.second >= 1:
            fps = frame_counter
            old_time = new_time
            frame_counter = 0
            
        

    window.close()
    print "exiting gracefully."
    sys.exit(0)

def on_entity_update(m, connection):
    global last_x, last_y, actions, last_tick

    last_x = m.x_pos
    last_y = m.y_pos
    
    
    last_tick = m.tick
    print "updating", command_counter - last_tick
    actions = []

    

messages.EntityUpdate.callback = on_entity_update

def on_player_join(m, connection):
    print m.player_name, m.player_model_id
    
messages.PlayerJoin.callback = on_player_join

if __name__ == '__main__':
    main()
