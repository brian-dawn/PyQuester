


# Direction based constants.
UP = 2
DOWN = 4
LEFT = 8
RIGHT = 16

# Convert a byte 0-255 into a tuple indicating the following:
# (1, 0)  = RIGHT
# (0, 1)  = DOWN
# (-1, 0) = LEFT
# (0, -1) = UP
# Combine to get diagonals.
def get_vector(direction):
    x = y = 0
    if not direction / RIGHT == 0:
        direction = direction % RIGHT
        x = 1
        
    if not direction / LEFT == 0:
        direction = direction % LEFT
        x = -1
        
    if not direction / DOWN == 0:
        direction = direction % DOWN
        y = 1
    
    if not direction / UP == 0:
        y = -1
        
    return (x,y)
