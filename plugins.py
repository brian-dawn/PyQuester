# Plugins allow us to dynamically load modules that we, or users write.
# It registers ID codes associated with each plugin which can be used
# later for network transfer. We can also retrieve modules using
# the functions found in this file.

# We can call the module as though it were imported by, for example
# using get_tile("grass").Tile() instead of
# import grass
# grass.Tile()
# Much simpler and easier for mods because we can call it with a string
# rather than having to modify some higher level python file.


import os
import os.path
import imp
import sys

# Dictionary of all light plugins.
lights = {}

# Dictionary of all tile plugins.
tiles = {}

# Dictionary of all effect plugins.
effects = {}

# Dictionary of all worker plugins.
workers = {}

# Dictionary of all plugins ids, used for network handling.
ids = {}


# Request a tile module. If it's not found error.
def get_tile(key):
    
    if not key in tiles:
        print "error: tile", key, "not found"
        sys.exit(0)
    return tiles[key]
   
# Request an effect module. If it's not found error.
def get_effect(key):
    
    if not key in effects:
        print "error: effect", key, "not found" 
        sys.exit(0)
    return effects[key]
    
# Request a light module. If it's not found error.
def get_light(key):
    
    if not key in lights:
        print "error: light", key, "not found"
        sys.exit(0)
    return lights[key]
    
# Request a light module. If it's not found error.
def get_worker(key):
    
    if not key in workers:
        print "error: worker", key, "not found"
        sys.exit(0)
    return workers[key]

    
# Loads a folder of modules (python files) into a dictionary.
def load(dictionary, folder, needs_id=True):
    
    plugin_path = constants.ROOT_PATH + "/plugins/" + folder

    # List comprehensions! Can probably add rule here to allow only .pyc
    # files, but for not lets only let people distribute mods with original source.
    pluginfiles = [fname[:-3] for fname in os.listdir(plugin_path) \
        if fname.endswith(".py") and not fname=="__init__.py"]

    if not plugin_path in sys.path:
        sys.path.insert(0, plugin_path)
    imported_modules = [__import__(fname) for fname in pluginfiles]
    
    
    for mod in imported_modules:
        print "imported", mod.__name__, "into", folder
        
        # Insert the module into the passed in dictionary.
        if mod.__name__ in dictionary:
            print "error:", mod.__name__, "already exists."
            sys.exit(0)
        dictionary[mod.__name__] = mod
        
        # Register the modules ID.
        # If ID is not defined in the module notify and exit.
        if needs_id:
            if not "ID" in dir(mod):
                print "error: ID is not defined in", mod.__name__, ("(" + folder + ")")
                sys.exit(0)
        
            _register_id(mod.ID, mod.__name__)


    
# Register a unique integer ID system for all imported plugins.

# For example, I make a new sword class, it has the ID of 5. If the server
# tells me that I picked up a 5, we can do a lookup to see that it was
# a sword. Furthermore if there are any special properties that the sword
# had to send over the network we can call the sword classes packing/unpacking
# routine on the bytes.

# None of this is really implemented yet, but we will need it once we introduce
# networking into the mix.
def _register_id(id, module_name):
    
    # id must be of the int type and nothing else!
    if not isinstance(id, int):
        print "error: ID must be an integer in", module_name
        sys.exit(0)
    
    # Check to make sure there isn't a duplicate ID.
    if id in ids:
        print "error: conflicting IDs in", module_name, "and", ids[id]
        sys.exit(0)
    ids[id] = module_name




import constants

    
