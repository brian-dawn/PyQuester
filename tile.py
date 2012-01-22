
import random
import sf



class Tile(object):
    # The width/height in pixels of one tile. Must be powers of 2.    
    SIZE = 64
    ID = 0
    def __init__(self, xtile, ytile):
        
        # Position of the tile within the level.
        # may want to just pass these as parameters.
        self._xtile = xtile
        self._ytile = ytile

        
        # For space constraints maybe move all these booleans into a bitstring?
        
        # Is light able to propagate through this tile?
        self.is_light_blocking = False#random.choice([True, False, False, False, False])
        
        # Is sunlight hitting this tile? This causes sunlight to propagate
        # from the tile in addition to it gaining an ambient light.
        self.is_under_sky = True
        
        # Has sunlight been calculated for this tile? Note this needs
        # to be reset to False if a nearby tile is changed.
        self.was_baked = False
        
        self._sprite = None
        self._set_texture(media.get_texture("tilegrass2"))
        

        
        # This stores the intensity of the sunlight in a 2d array. The
        # size is determined by the Light.SUBDIVIDE variable. This
        # is used to draw the ambient lightmap, which allows us to
        # have sunlight "bleed" into interior spaces and fall off
        # like a normal light should.
        self.sunlight_propagation_intensity = []
        for i in xrange(Light.SUBDIVIDE):
            self.sunlight_propagation_intensity.append([])
            for j in xrange(Light.SUBDIVIDE):
                self.sunlight_propagation_intensity[i].append(0)
        

    # Properly resets the sprite to the new texture.
    def _set_texture(self, texture):
        self._sprite = sf.Sprite(texture)
        
        # Map a large image that is a power of 2, to the current tile.
        # this allows us to have tiles of the same type that look different.
        # much less patterns.
        xsub = self._xtile * Tile.SIZE % texture.width
        ysub = self._ytile * Tile.SIZE % texture.height
        self._sprite.set_sub_rect(sf.IntRect(xsub, ysub, Tile.SIZE, Tile.SIZE))
        
        
    # Draw the tile at the specified x and y coordinate.
    # this is the tiles position within the level object.
    def draw(self, window):
        
        self._sprite.x = self._xtile * Tile.SIZE - camera.x
        self._sprite.y = self._ytile * Tile.SIZE - camera.y

        
        window.draw(self._sprite)


import camera
import media
from light import Light
