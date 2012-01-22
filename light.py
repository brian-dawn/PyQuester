# Light to be a plugin system?
# same with entity! omg!

import math
import sf

from tile import Tile # This import is needed up here for constants.

class Light(object):
    
    # Lighting is broken up into subtiles for smoother lighting.
    # This means there are 2x2 subtiles per tile.
    SUBDIVIDE = 2
    
    # A scaling factor used to scale the lightmaps when drawn.
    SCALE = Tile.SIZE / SUBDIVIDE
    
    @property
    def color(self):
        return self._sprite.color

    @color.setter
    def color(self, color):
        self._sprite.color = color

    @property
    def x(self):
        return self._xcoord * Light.SCALE

    @x.setter
    def x(self, x_position):
        self._xcoord = x_position / Light.SCALE

    @property
    def y(self):
        return self._ycoord * Light.SCALE

    @y.setter
    def y(self, y_position):
        self._ycoord = y_position / Light.SCALE

    def __init__(self, level, x, y, radius, color=sf.Color.WHITE):
        
        # Pixel map to be used when calculating the light.
        self._light_pixelmap = sf.Image(radius*2+1, radius*2+1, sf.Color(0,0,0,0)) 
        
        # Texture which loads the pixel map so it can be drawn.
        self._texture = sf.Texture(radius*2+1, radius*2+1)
        self._texture.smooth = True

        # Sprite to be used for drawing the light.
        self._sprite = sf.Sprite(self._texture)
        self._sprite.blend_mode = sf.BlendMode.ADD
        self._sprite.scale(Light.SCALE, Light.SCALE)

        # The level this light exists on.        
        self._level = level
        
        # Modifiable configuration options.
        self.radius = radius
        self._xcoord = 10
        self._ycoord = 10
        self.x = x
        self.y = y
        self._sprite.color = color
        
        # Finalize it by calculating the lightmap.
        self.update()
        
    
    # Draws the lightmap at its current location.
    def draw(self, window):
        # Coordinates for the real world 
        x = self._xcoord * Light.SCALE
        y = self._ycoord * Light.SCALE
	    
        self._sprite.x = x - self._sprite.width / 2 + Light.SCALE / 2 - camera.x
        self._sprite.y = y - self._sprite.height / 2 + Light.SCALE / 2 - camera.y
	    
        window.draw(self._sprite)
    
    # Updates the lightmap, must be called whenever the light moves to a new subtile,
    # or when the environment is changed near the light. This is a very intensive
    # function so avoid calling it a lot.
    def update(self):
        
        # Clear/re-initialize the pixels in the lightmap.
        for x in xrange(self._light_pixelmap.width):
            for y in xrange(self._light_pixelmap.height):
                self._light_pixelmap.set_pixel(x, y, sf.Color(0,0,0,0))
        
        # Generate the base intensity that the _place_light function uses.
        base_intensity = math.pow(100.0, 1.0 / (self.radius * self.radius))

        self._place_light(self._xcoord, self._ycoord, 0.0, base_intensity)
        
        # Mid pixel error correction.
        color_center = self._light_pixelmap.get_pixel(self.radius, self.radius)
        color_center.a = 255
        self._light_pixelmap.set_pixel(self.radius, self.radius, color_center)
        
        # Reset the red channel.
        for x in xrange(self._light_pixelmap.width):
            for y in xrange(self._light_pixelmap.height):
                col = self._light_pixelmap.get_pixel(x, y)
                col.r = col.a
                col.g = col.a
                col.b = col.a
                col.a = 255

                self._light_pixelmap.set_pixel(x, y, col)
                
        self._texture.update(self._light_pixelmap)
        
    # The recursive lighting algorithm.
    # The distance to reach a node is stored in the red channel (temporarily).
    # The intensity of the light is stored in the alpha channel.
    def _place_light(self, xcoord, ycoord, dist, base_intensity):
        
        # Coordinates for the pixel the light is currently on.
        x = int(xcoord - self._xcoord + self.radius)
        y = int(ycoord - self._ycoord + self.radius)
	
        color = self._light_pixelmap.get_pixel(x, y)

        olddist = color.r

        if dist < self.radius and (dist < olddist or olddist == 0):
            # Store the intensity in the alpha channel.
            color.a = int(255.0 / math.pow(base_intensity, dist*dist))

            # Store the distance from the origin in the red channel.
            color.r = dist
            
            self._light_pixelmap.set_pixel(x, y, color)
            
            # Coordinates for the tile the light is currently on.
            xtile = int(xcoord / Light.SUBDIVIDE)
            ytile = int(ycoord / Light.SUBDIVIDE)
            
            tile = self._level.get_tile(xtile, ytile)
            
            if tile == None:
                return None
            
            if not tile.is_light_blocking or dist == 0:
                
                # Handle the subtiles adjacent to the current one.
                self._place_light(xcoord+1, ycoord, dist+1, base_intensity)
                self._place_light(xcoord-1, ycoord, dist+1, base_intensity)
                self._place_light(xcoord, ycoord+1, dist+1, base_intensity)
                self._place_light(xcoord, ycoord-1, dist+1, base_intensity)

                # Handle the diagonals.
                self._place_light(xcoord+1, ycoord+1, dist+constants.SQRT2, base_intensity)
                self._place_light(xcoord-1, ycoord-1, dist+constants.SQRT2, base_intensity)
                self._place_light(xcoord-1, ycoord+1, dist+constants.SQRT2, base_intensity)
                self._place_light(xcoord+1, ycoord-1, dist+constants.SQRT2, base_intensity)


import camera
import media
import constants
     
