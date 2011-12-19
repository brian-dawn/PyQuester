#This is akin to World only it only handles one z-level.
import sf
import math



class Level(object):
    # The width/height in number of tiles.
    # Small right now for speed/testing.
    SIZE = 64
    
    # Max distance in light coordinates at which sunlight
    # will disperse into shadows.
    SUNLIGHT_DISTANCE = 10
    
    @property
    def sunlight_color(self):
        return self._sunlight_sprite.color

    @sunlight_color.setter
    def sunlight_color(self, color):
        self._sunlight_sprite.color = color
    
    def __init__(self):
        # Populate a 2D list with tiles.
        self._tiles = []
        for i in xrange(Level.SIZE):
            self._tiles.append([])
            for j in xrange(Level.SIZE):
                self._tiles[i].append(Tile(i, j))
                
        # Test delete this when sunlight is working.
        for i in xrange(10,16):
            for j in xrange(10,16):
                self._tiles[i][j].is_under_sky = False
                self._tiles[i][j]._set_texture(media.floor_texture)
                
                
        for i in xrange(19,36):
            for j in xrange(19,36):
                self._tiles[i][j].is_under_sky = False
                self._tiles[i][j]._set_texture(media.floor_texture)
        
          
        for i in xrange(10, 16):
            self._tiles[i][10].is_light_blocking = True
            self._tiles[i][10].is_under_sky = False
            self._tiles[i][10]._set_texture(media.tile_texture)
            
            self._tiles[i][16].is_light_blocking = True
            self._tiles[i][16].is_under_sky = False
            self._tiles[i][16]._set_texture(media.tile_texture)
            
        for i in xrange(10, 17):
            self._tiles[10][i].is_light_blocking = True
            self._tiles[10][i].is_under_sky = False
            self._tiles[10][i]._set_texture(media.tile_texture)
            
            self._tiles[16][i].is_light_blocking = True
            self._tiles[16][i].is_under_sky = False
            self._tiles[16][i]._set_texture(media.tile_texture)
        
        self._tiles[10][15].is_light_blocking = False
        self._tiles[10][15]._set_texture(media.floor_texture)
        self.add_tile(1, 1, "grass")
        
        
        
        # Used to determine if we need to bake more tiles because
        # the camera has moved too far.
        self._old_camera_x = -1337
        self._old_camera_y = -1337
        
        # Generate a list to store our lights in.
        self._lights = []
        
        self._lights.append(Light(self, x=1770, y=1730, radius=8, color=sf.Color(255,111,5)))
        
        # Sunlight handling.
        map_width = camera.width / Tile.SIZE * Light.SUBDIVIDE + 5
        map_height = camera.height / Tile.SIZE * Light.SUBDIVIDE + 5
        scale = Tile.SIZE / Light.SUBDIVIDE
        self._sunlight_pixelmap = sf.Image(map_width, map_height)
        self._sunlight_texture = sf.Texture(map_width, map_height)
        self._sunlight_texture.smooth = True
        self._sunlight_sprite = sf.Sprite(self._sunlight_texture)
        self._sunlight_sprite.color = sf.Color.WHITE
        self._sunlight_sprite.blend_mode = sf.BlendMode.ADD
        self._sunlight_sprite.scale(scale, scale)
        
        # RenderTexture to act as our lightmap.
        self._lightmap = sf.RenderTexture(camera.width, camera.height)
        self._lightmap.display() # Force the RenderTexture to display.
        
        # Sprite for the lightmap with correct options set.
        self._lightmap_sprite = sf.Sprite(self._lightmap.texture)  
        self._lightmap_sprite.blend_mode = sf.BlendMode.MULTIPLY

        # The color that is the base for all lighting. Will likely
        # want to remain black, darkness isn't bright right?
        self.ambient_color = sf.Color.BLACK
        self.sunlight_color = sf.Color(225,185,122)
    
    def add_tile(self, xtile, ytile, module_name):
        tile = plugins.tiles[module_name].Tile(xtile, ytile)
        self._tiles[xtile][ytile] = tile
        
    def update(self):
        # If the camera has moved sufficiently far, we need to
        # bake new tiles.
        if abs(self._old_camera_x - camera.x) > Tile.SIZE or \
           abs(self._old_camera_y - camera.y) > Tile.SIZE:
            self._old_camera_x = camera.x
            self._old_camera_y = camera.y
            
            # Bake the tiles within the range of the camera.
            r = camera.tile_ranges()
            t = Level.SUNLIGHT_DISTANCE / Light.SUBDIVIDE + 2
            for i in xrange(r[0]-t, r[1]+t):
                for j in xrange(r[2]-t, r[3]+t):
                    self._bake_sunlight(i, j) 
        
        
    def draw(self, window):
        """
        Diffuse Drawing
        """
	    # Draw the tiles that are visible on the screen.
        r = camera.tile_ranges()
        for i in xrange(r[0], r[1]):
            for j in xrange(r[2], r[3]):
                    tile = self.get_tile(i,j)
                    if not tile == None:
                        tile.draw(window)
        
        """
        Lightmap Drawing
        """ 
        # Draw the lights onto the lightmap RenderTexture.
        self._lightmap.clear(self.ambient_color)
        
        # Update the sunlight from the tiles on the screen.
        self._update_sunlight()
        
        # Fixes modulo problems when the camera goes negative.
        xtemp = camera.x % Tile.SIZE
        ytemp = camera.y % Tile.SIZE
        if camera.x < 0:
            xtemp = xtemp - Tile.SIZE
            if xtemp % Tile.SIZE == 0: xtemp = 0
        if camera.y < 0:
            ytemp = ytemp - Tile.SIZE
            if ytemp % Tile.SIZE == 0: ytemp = 0
        
        # Calculate the position of the sunlight sprite.
        self._sunlight_sprite.x = -xtemp#-Tile.SIZE - xtemp
        self._sunlight_sprite.y = -ytemp#-Tile.SIZE - ytemp
        self._lightmap.draw(self._sunlight_sprite)
        
        # Draw the lights the level has.
        for light in self._lights:
            light.draw(self._lightmap)

        # Make sure the RenderTexture is ready to display.
        self._lightmap.display() 
       
        # Draw the lightmap to the main window.       
        window.draw(self._lightmap_sprite)
        
    # Returns: a tile at the specified coordinates. Returns None
    # if the coordinates are outside the ranges of the level.
    def get_tile(self, xtile, ytile):
        if xtile >= Level.SIZE or ytile >= Level.SIZE or xtile < 0 or ytile < 0:
            return None
        return self._tiles[xtile][ytile]
    
    # "Baking" a tile refers to the act of propagating sunlight that hits
    # the tile, and propagating it into interior spaces so as to give a nice
    # transition effect between indoors and outdoors.
    def _bake_sunlight(self, xtile, ytile):
        tile = self.get_tile(xtile, ytile)
        
        # Only bake once fool.
        if not tile == None and not tile.was_baked:
            tile.was_baked = True
            
            # Walls can't propagate sunlight. Bleeding sunlight is bad for
            # ones health.
            if (not tile.is_light_blocking) and tile.is_under_sky:
                
                # Calculate out the base intensity for the lighting algorithm
                # to use. This is a constant, so can probably be calculated
                # once way above.
                base_intensity = math.pow(15.0, 1.3 / (Level.SUNLIGHT_DISTANCE * \
                                                       Level.SUNLIGHT_DISTANCE - 10))
                
                # Propagate sunlight for each subtile.
                for i in xrange(Light.SUBDIVIDE):
                    for j in xrange(Light.SUBDIVIDE):
                        self._propagate_sunlight(xtile * Light.SUBDIVIDE + i, \
                                                 ytile * Light.SUBDIVIDE + j, \
                                                 0.0, base_intensity)
                                                 
    # Updates the sunlight texture to represent the sunlight hitting
    # all the current tiles that are visible to the camera.
    def _update_sunlight(self):
        # Left hand side of the camera in light coordinates.
        xstart = camera.tile_coord_x1() * Light.SUBDIVIDE
        ystart = camera.tile_coord_y1() * Light.SUBDIVIDE

        # Go through the entire pixelmap.
        for i in xrange(self._sunlight_pixelmap.width):
            for j in xrange(self._sunlight_pixelmap.height):
                # Calculate the tile that corresponds to the current pixel.
                xtile = (i + xstart) / Light.SUBDIVIDE
                ytile = (j + ystart) / Light.SUBDIVIDE
                
                tile = self.get_tile(xtile, ytile)
                if not tile == None:
                    
                    x = i % Light.SUBDIVIDE
                    y = j % Light.SUBDIVIDE
                    
                    # Set the intensity found in the tile to the pixel.
                    intensity = tile.sunlight_propagation_intensity[x][y]
                    self._sunlight_pixelmap.set_pixel(i, j, sf.Color(255, 255, 255, intensity))
        
        self._sunlight_texture.update(self._sunlight_pixelmap)
        
    # Sunlight propagation algorithm. Handles dispersing sunlight into
    # tiles. Thus giving a transition into interior spaces. This is the
    # same algorithm found in the Light class.
    def _propagate_sunlight(self, xcoord, ycoord, dist, base_intensity):
        xtile = xcoord / Light.SUBDIVIDE
        ytile = ycoord / Light.SUBDIVIDE
        
        tile = self.get_tile(xtile, ytile)

        # Constraints, or as I like to call them... kill conditions.
        if tile == None:
            return None
                
        if (dist != 0 and tile.is_under_sky) or \
            dist > Level.SUNLIGHT_DISTANCE:
            return None
        
        # Intensity comparison to see if we continue moving forward.
        x = xcoord % Light.SUBDIVIDE
        y = ycoord % Light.SUBDIVIDE
        tile_intensity = tile.sunlight_propagation_intensity[x][y]
        
        intensity = int(255.0 / math.pow(base_intensity, dist*dist))

        if intensity > tile_intensity:
            tile.sunlight_propagation_intensity[x][y] = intensity

            if not tile.is_light_blocking:
                # Handle adjacents.
                self._propagate_sunlight(xcoord, ycoord+1, dist+1, base_intensity)
                self._propagate_sunlight(xcoord, ycoord-1, dist+1, base_intensity)
                self._propagate_sunlight(xcoord+1, ycoord, dist+1, base_intensity)
                self._propagate_sunlight(xcoord-1, ycoord, dist+1, base_intensity)
                
                # Handle diagonals.
                self._propagate_sunlight(xcoord+1, ycoord+1, dist+constants.sqrt2, base_intensity)
                self._propagate_sunlight(xcoord-1, ycoord-1, dist+constants.sqrt2, base_intensity)
                self._propagate_sunlight(xcoord+1, ycoord-1, dist+constants.sqrt2, base_intensity)
                self._propagate_sunlight(xcoord-1, ycoord+1, dist+constants.sqrt2, base_intensity)

            
        

#from tiles.grass import Grass
#from tiles import grass

from light import Light
from tile import Tile
import camera
import media
import constants
import plugins
    
		
