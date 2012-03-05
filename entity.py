"""
This system is a component based design built around the following ideas:

Entity: Bags of components, no logic should be involved.
Components: Bags of data, no logic should be involved.
Systems: Hook into entities and operate on them.

The internals "should be" constant time for all operations. I use dictionaries and
bitstrings as often as I can. Utilizing bitstrings means we can't have more than
64 components, and we can't have more than 64 systems. This should not be a problem,
but if it is, we can redesign the bitstring class to allow for more.

"""
#http://www.reddit.com/r/gamedev/comments/pzdxv/how_do_you_structure_your_game_code_mvc/


# Just bags of data.
class Component:
    ID = -1
    
class PositionComponent(Component):
    ID = 1
    def __init__(self):
        self.x = 2
    
class VelocityComponent(Component):
    ID = 0
    
# Base class new systems can extend from. A system operates on components.
class System(object):

    def _init(self):
        # This will be assigned by the SystemManager later.
        self.ID = -1
        
        # Stores all current entities in the system.
        self._entities = []
        
        # The bitstring that contains the components mapped to this system.
        self._component_bitstring = BitString()
        
        # Map all components to this system.
        self.mappings()
        
    # Override this method to handle new mappings.
    def mappings(self):
        raise Exception("system " + self.__class__.__name__ + " has not defined mappings.")
        
    def _remove_entity(self, entity):
        self._entities.remove(entity)
        
    def _add_entity(self, entity):
        self._entities.append(entity)
        
    # Map what kind of components the system must have to gain control of an entity.
    def map_component_class(self, class_name):

        # Ensure the component has ID overridden.
        if class_name.ID == -1:
            raise Exception(class_name.__name__ + " does not define ID.")

        # Ensure ID fits within BitString range.
        if not (class_name.ID >= 0 and class_name.ID < BitString.SIZE):
            raise Exception(class_name.__name__ + " has an invalid ID must be [0..63].")

        self._component_bitstring.add_to_set(class_name.ID)
    
    # Override this method to process entities.
    def process(self, entity):
        pass
        
    # Process all components.
    def update(self):
        
        for entity in self._entities:
            self.process(entity)

class MoveSystem(System):
    
    def mappings(self):
        
        self.map_component_class(VelocityComponent)
        self.map_component_class(PositionComponent)
    
    def process(self, entity):
        
        print entity.get_component(PositionComponent).x
  
# Handles a collection of systems. Only one instance is needed.      
class SystemManager:
    
    def __init__(self):
        self._system_id_counter = -1
        self._systems = []
        
    def add_system(self, system):
        system.ID = self._register_id()
        system._init()
        self._systems.append(system)
        return system
        
    def _register_id(self):
        self._system_id_counter = self._system_id_counter + 1
        if self._system_id_counter == 64:
            raise Exception("too many systems, exceeds 64 limit.")
        return self._system_id_counter
      

class Entity:
    # Keep track of the latest ID for entities to ensure they get unique IDs.
    _id_counter = 0
    
    def __init__(self, system_manager):
        # Fairly certain we don't need this to be a dict, as
        # we are unlikely to want to reference specific
        # systems by id.
        self._systems = []
        
        # A dict of all components inside this entity.
        # The keys are the IDs of the components.
        self._components = {}
        
        # The components this entity has.
        self._component_bitstring = BitString()
        
        # Keep track of the old bitstring so we can see
        # what has changed when we call refresh twice.
        self._old_component_bitstring = BitString()
        
        # Systems that this entity belongs to.
        self._systems_bitstring = BitString()
        
        # Ensure unique IDs.
        self.ID = Entity._id_counter
        Entity._id_counter = Entity._id_counter + 1
        
        # The system manager the entity belongs to.
        # Gives access to the existing systems.
        self.system_manager = system_manager
        
    # Remove an entity from all systems it is hooked into.
    def kill(self):
        for system in self._systems:
            system._remove_entity(self)
            
    # Allow all systems to hook into (or out of) the entity.
    def refresh(self):

        # If the entity is already hooked in remove them, so we don't add them twice.
        # This design can be optimized, but low priority.
        if not self._old_component_bitstring.is_empty():
            self.kill()
                
        self._old_component_bitstring = self._component_bitstring    
        
        for system in self.system_manager._systems:
            
            # Add the entity if it maps correctly to the system.
            if self._component_bitstring.contains_subset(system._component_bitstring):
                system._add_entity(self)
                self._systems.append(system)

    # Return a component that the entity contains based on the class.
    def get_component(self, component_class):
        
        return self._components[component_class.ID]

    # Add a component to the entity. Be sure to refresh afterwards.
    def add_component(self, component):

        # Fairly certain we don't want two PositionComponents for example.
        if component.__class__.ID in self._components:
            raise Exception(component.__class__.__name__ + " already inside of entity!")
            
        self._components[component.__class__.ID] = component
        
        #self._components.append(component)
        self._component_bitstring.add_to_set(component.ID)

from bitstring import BitString


sm = SystemManager()
s2 = sm.add_system(MoveSystem())

e = Entity(sm)
e.add_component(PositionComponent())
e.add_component(VelocityComponent())
e.refresh()
#e.kill()

s2.update()
