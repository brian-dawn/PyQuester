
import sf

floor_texture = sf.Texture.load_from_file("media/b.jpg")
tile_texture = sf.Texture.load_from_file("media/tile.png")
grass_texture = sf.Texture.load_from_file("media/tilegrass2.png")

import os
import os.path
import imp
import sys

textures = {}

def get_texture(key):
    if not key in textures:
        print "Error texture", key, "not loaded"
        sys.exit(0)
    return textures[key]
    
# Loads a folder of images (python files) into a dictionary.
def load_textures():

    images_path = constants.root_path + "/media"

    # List comprehensions!
    files = [fname for fname in os.listdir(images_path) \
        if fname.endswith(".png") or fname.endswith(".jpg")]

    for img in files:
        textures[img[:-4]] = sf.Texture.load_from_file(images_path + "/" + img)
        print "Loaded", img, "as", img[:-4]

import constants