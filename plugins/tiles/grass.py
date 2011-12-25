
#from tile import Tile
import tile

def initialize():
    None
    
    
class Tile(tile.Tile):
    ID = 1 # This has to be unique from all other possible entities.
           # used for packing tiles into network packets.
           
    def __init__(self, xtile, ytile):
        super(Tile, self).__init__(xtile, ytile)
        
        self._set_texture(media.get_texture("tile"))
        
        
import media