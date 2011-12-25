# A base for the effect plugin system. An Effect is essentially an emitter
# tied to a particle effect. Plugins can extend the effect class to create
# unique effects.

if __name__ == '__main__':
    import main
    main.main()

import sf



# Basic container class for a particle.
class Particle(object):
    
    def __init__(self, texture):
        
        # Holds drawing options such as size, color,
        # texture, and blend mode.
        self.sprite = sf.Sprite(texture)
        
        # When this value is 0 or less, the particle gets murdered.
        # Brutally. 
        self.life = 0
        
        # Added to the position every tick.
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        
        # Position relative to the Effect.
        # DO NOT USE sprite.x or sprite.y.
        self.x = 0.0
        self.y = 0.0
        
# An emitter class. Controls how the particles behave.
class Effect(object):
    
    def __init__(self, x, y):
        
        self._particles = []
        self.x = x
        self.y = y
        
    # Called on each particle that is in the list.
    # Override this to handle behavior of particles.
    def _update_particle(self, p):
        None
        
    # Called once per update automatically.
    # Override this to handle spawning of particles,
    # or whatever you wish to do once per update.
    def _update(self):
        None
        
    # Update the particles in the list.
    # Call the _update method so people can override it.
    def update(self):
        
        self._update()
        for particle in self._particles:
            
            # Velocity handling.
            particle.x = particle.x + particle.x_velocity
            particle.y = particle.y + particle.y_velocity

            self._update_particle(particle)
            
            # Life handling.
            particle.life = particle.life - 1
            if particle.life <= 0:
                self._particles.remove(particle)
                
    # Draw all the particles to the window.
    def draw(self, window):
        for particle in self._particles:
            
            # Camera handling.
            particle.sprite.x = particle.x - camera.x + self.x
            particle.sprite.y = particle.y - camera.y + self.y
            
            window.draw(particle.sprite)
    
    # Draw the particles with a specified x and y origin.
    # Useful for if you want to pattern one effect without
    # having a lot of updates. This can probably be optimized
    # by drawing to a render texture and then just returning
    # that.
    def draw_at(self, x, y, window):
        for particle in self._particles:
            
            # Camera handling.
            particle.sprite.x = particle.x - camera.x + x
            particle.sprite.y = particle.y - camera.y + y
            
            window.draw(particle.sprite)
        
  
import camera
import media
            
            