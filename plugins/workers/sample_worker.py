# A worker is a function that operates on a level. These are helpful
# things that can be utilized by the world generator. They are not
# classes because as far as I can tell they do not need to be.

# There can be as many worker functions as you want in any one file,
# and they need not have the same parameters. They will all likely
# take in a level object.

from level import Level


# When called this turns an entire column to whatever is passed in.
# See main for an example of calling this worker function.
def crap_work(level, x, tile_key):
    
    for y in xrange(Level.SIZE):
        
        level.set_tile(x, y, tile_key)
    


