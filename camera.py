# camera.py
# This file stores various variables for handling the offset that all drawing functions
# go through. They also have functions which allow us to get the tile coordinates of
# the corners of the viewport. This allows us to easily grab a chunk of tiles to draw.
#
#
#



x = float(0.0)
y = float(0.0)

width = 800
height = 600

#Returns a tuple of the following format:
# [0]        [1]
#
#
# [2]        [3]
#where the coordinates are in tile coordinates.
def tile_ranges():
    return tile_coord_x1(), tile_coord_x2(), tile_coord_y1(), tile_coord_y2()
           
def tile_coord_x1():
    return int(x / Tile.SIZE)

def tile_coord_y1():
    return int(y / Tile.SIZE)

def tile_coord_x2():
    return int((x+width) / Tile.SIZE + 1)
    
def tile_coord_y2():
    return int((y+height) / Tile.SIZE + 1)
    
from tile import Tile
    