
import tile

ID = 2

    
class Tile(tile.Tile):

           
    def __init__(self, xtile, ytile):
        super(Tile, self).__init__(xtile, ytile)
        
        self.is_light_blocking = False
        self.is_under_sky = False
        
        self._set_texture(media.get_texture("b"))
        
        
import media
