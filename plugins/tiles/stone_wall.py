
import tile

ID = 3

    
class Tile(tile.Tile):

           
    def __init__(self, xtile, ytile):
        super(Tile, self).__init__(xtile, ytile)
        
        self.is_light_blocking = True
        self.is_under_sky = False
        
        self.has_collision = True
        self._set_texture(media.get_texture("tile"))
        
        
import media
