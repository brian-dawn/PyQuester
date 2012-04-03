# Part of the entity system. Houses all components, which should idealy simply be bags of data.

from entity import Component


class PlayerControlComponent(Component):
    ID = 0
    def __init__(self):
        pass

class PositionComponent(Component):
    ID = 1
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.old_x = x
        self.old_y = y
    
class VelocityComponent(Component):
    ID = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4

class DrawComponent(Component):
    ID = 3
    LIGHT_LAYER = 0
    def __init__(self, layer):
        self.layer = layer

class CollisionComponent(Component):
    ID = 4

    def __init__(self, width, height):
        self.width = width
        self.height = height

