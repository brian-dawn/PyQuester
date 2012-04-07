# Houses code for the various entity systems. These can't be plugins because we are limited to how many we can have
# via bitstring.
# TODO: Maybe we want to have tiles be entities, and level just be a system.
# If they are going to have health we may want to do that... but for now this will work.
import sf
from entity import System, Entity
from components import *

class PlayerControlSystem(System):

    def mappings(self):
        self.map_component_class(PlayerControlComponent)
        self.map_component_class(VelocityComponent)

    def process(self, entity):
        x = y = 0.0
        if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
            y = y + 1.0      
        if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
            y = y - 1.0
        if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
            x = x - 1.0
        if sf.Keyboard.is_key_pressed(sf.Keyboard.D):
            x = x + 1.0

        velocity_comp = entity.get_component(VelocityComponent)
        velocity_comp.x = x * velocity_comp.speed
        velocity_comp.y = y * velocity_comp.speed

# TODO: Do we want each level to have a collision
class CollisionSystem(System):


    def mappings(self):

        self.map_component_class(CollisionComponent)
        self.map_component_class(PositionComponent)

    # TODO: We want the tile system to be implemented using geospatial hashing of some sort... or quadtree.
    # For all other collision entities it may be a quadtree would be acceptable.

    # Return a list of entities that the entity has collided with in the scan.
    def get_collisions(self, entity, entity_list=None, boolean_response=False):
        result = []

        if not entity_list:
            entity_list = self._entities

        collision_comp_a = entity.get_component(CollisionComponent)
        position_comp_a = entity.get_component(PositionComponent)

        # Handle collision with the level.
        level = level_manager.get_level(self.level_z_index)
        x = position_comp_a.x
        y = position_comp_a.y
        r = [int(x / Tile.SIZE), int((x+Tile.SIZE) / Tile.SIZE + 1), \
             int(y / Tile.SIZE), int((y+Tile.SIZE) / Tile.SIZE + 1)]

        for i in xrange(r[0], r[1]):
            for j in xrange(r[2], r[3]):
                    tile = level.get_tile(i,j)
                    if not tile == None:
                        if tile.has_collision:
                            if util.rectangles_overlap(position_comp_a.x, position_comp_a.y, \
                                                       collision_comp_a.width, collision_comp_a.height, \
                                                       i * Tile.SIZE, j * Tile.SIZE, Tile.SIZE, Tile.SIZE):
                                if boolean_response:
                                    return True

                          

        # Handle collision with other entities.
        for entity_b in entity_list:

            collision_comp_b = entity_b.get_component(CollisionComponent)
            position_comp_b = entity_b.get_component(PositionComponent)

            if not entity_b == entity:
                if util.rectangles_overlap(position_comp_a.x, position_comp_a.y, \
                                      collision_comp_a.width, collision_comp_a.height, \
                                      position_comp_b.x, position_comp_b.y, \
                                      collision_comp_b.width, collision_comp_b.height):
                    if boolean_response:
                        return True
                    result.append(entity_b)

        if boolean_response:
            return False
        return result


class DrawSystem(System):
    def __init__(self, window):
        super(DrawSystem, self).__init__()
        self.window = window

        self.light_layer_entities = []

    def register_entity(self, entity):
        draw_comp = entity.get_component(DrawComponent)
        if draw_comp.layer == DrawComponent.LIGHT_LAYER:
            self.light_layer_entities.append(entity)

    def unregister_entity(self, entity):
        draw_comp = entity.get_component(DrawComponent)
        if draw_comp.layer == DrawComponent.LIGHT_LAYER:
            self.light_layer_entities.remove(entity)

    def mappings(self):
        self.map_component_class(PositionComponent)
        # then draw component   

    def draw_entity(self, entity):
        position_comp = entity.get_component(PositionComponent)

        rect = sf.Shape.rectangle(position_comp.x - camera.x, position_comp.y - camera.y, 50, 50, sf.Color.WHITE)
        self.window.draw(rect)

    def draw_light_layer(self):

        for entity in self.light_layer_entities:
            self.draw_entity(entity)

# Unfortunately tied intimately to the collision system.
class MoveSystem(System):

    def __init__(self, collision_system):
        super(MoveSystem, self).__init__()
        self.collision_system = collision_system

    def mappings(self):
        
        self.map_component_class(VelocityComponent)
        self.map_component_class(PositionComponent)
    
    def process(self, entity):
        
        position_comp = entity.get_component(PositionComponent)
        velocity_comp = entity.get_component(VelocityComponent)

        position_comp.old_x = position_comp.x
        position_comp.old_y = position_comp.y

        collision_comp = entity.get_component(CollisionComponent)
        if collision_comp:

            # Get the direction to push the entity if it collided.
            yc = 1 if velocity_comp.y < 0 else -1
            xc = 1 if velocity_comp.x < 0 else -1

            position_comp.x = position_comp.x + velocity_comp.x

            # TODO: Have the overlap return how deep it is, so we can just return the max distance.
            # Perform x axis collision detection and response.
            result = self.collision_system.get_collisions(entity)
            while self.collision_system.get_collisions(entity, result, True):
                position_comp.x = position_comp.x + xc

            position_comp.y = position_comp.y + velocity_comp.y
            # Perform y axis collision detection and response.

            result = self.collision_system.get_collisions(entity)
            while self.collision_system.get_collisions(entity, result, True):
                position_comp.y = position_comp.y + yc
        else:
            position_comp.x = position_comp.x + velocity_comp.x
            position_comp.y = position_comp.y + velocity_comp.y

import camera
import util
import level_manager
from tile import Tile