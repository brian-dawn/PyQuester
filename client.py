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
import legume


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

from tile import Tile
from light import Light
from level import Level




def main():
    # Load the tiles folder.
    media.load_textures()
    plugins.load(plugins.tiles, "tiles")
    plugins.load(plugins.effects, "effects")
    plugins.load(plugins.lights, "lights")
    plugins.load(plugins.workers, "workers", needs_id=False)
    
    window.framerate_limit = 60
    window.vertical_sync_enabled = True
    running = True

    # Connect to server.
    client = legume.Client()
    client.connect(("localhost", constants.PORT))

    
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
        
        print client.state, client.CONNECTED, client.ERRORED, client.DISCONNECTED
        try:
            client.update()
        except RuntimeError:
            pass
            
        if (client.state == client.CONNECTED):
            print client.latency
                             
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

if __name__ == '__main__':
    main()
