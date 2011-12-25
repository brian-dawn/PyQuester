# This file will dynamically load plugins, this should make
# the game much easier to mod, they can extend classes in new
# python files then it dynamically finds and loads them.

# For now don't use this keep it simple.
# Or we populate a dictionary with an integer id
# I think this should be done, because then we can simply say
# level.add_tile(x, y, "grass")

if __name__ == '__main__':
    import main
    main.main()

import os
import os.path
import imp
import sys

tiles = {}
effects = {}

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
    
    
# Loads a folder of modules (python files) into a dictionary.
def load(dictionary, folder):
    plugin_path = constants.root_path + "/plugins/" + folder

    # List comprehensions! Can probably add rule here to allow only .pyc
    # files, but for not lets only let people distribute mods with original source.
    pluginfiles = [fname[:-3] for fname in os.listdir(plugin_path) \
        if fname.endswith(".py") and not fname=="__init__.py"]

    if not plugin_path in sys.path:
        sys.path.insert(0, plugin_path)
    imported_modules = [__import__(fname) for fname in pluginfiles]
    
    
    for mod in imported_modules:
        print "imported", mod.__name__, "into", folder
        dictionary[mod.__name__] = mod



import constants

    
