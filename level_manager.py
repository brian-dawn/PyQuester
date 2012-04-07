
_levels = {}

def register_level(level):
    _levels[level.z_index] = level

def update_level(z_index):
    _levels[z_index].update()

def draw_level_diffuse(z_index, window):
    _levels[z_index].draw_tiles(window)

def draw_level_lightmap(z_index, window):
    _levels[z_index].draw_lightmap(window)

def get_level(z_index):
    return _levels[z_index]