import sf

import effects

ID = 3464

# An example of an effect plugin.
class Effect(effects.Effect):
    
    def __init__(self, x, y):
        super(Effect, self).__init__(x, y)
        
    
    def _update_particle(self, p):
        color = p.sprite.color
        
        if color.a >= 4:
            color.a = p.sprite.color.a - 4
            
        if color.r >= 4:
            color.r = p.sprite.color.r - 4
        
        p.sprite.color = color

        
    def _update(self):

        p = effects.Particle(media.get_texture("particle"))
        
        p.life = 80
        #p.sprite.blend_mode = sf.BlendMode.ADD
        p.sprite.color = sf.Color(255,5,155)
        p.sprite.scale(2, 2)

        p.x_velocity = random.randrange(-100, 100) / 100.0
        p.y_velocity = random.randrange(-100, 100) / 100.0
        
        
        self._particles.append(p)


import random
import media
    