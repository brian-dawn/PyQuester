# BitString.py
# Author: Brian Dawn

# Constant time BitString code. Find if something belongs in a set super fast! Limit to
# sets of 64 only.
# This will be used for the entity system. This means we can't have more than 64 different
# components or systems but that should be ok.

class BitString:
    # Max size of bitstring.
    SIZE = 64

    def __init__(self, *initial_elements):
        self.set = long(0)
        
        for element in initial_elements:
            self.add_to_set(element)
            
    def copy(self):
        b = BitString()
        b.set = self.set
        return b 
        
    def is_empty(self):
        return self.set == 0
        
    def contains(self, n):
        return (self.set & (long(1) << n)) != 0
       
    def remove_from_set(self, n):
        self.set = ~self.set
        self.set |= long(1) << n
        self.set = ~self.set
    
    def add_to_set(self, n):
        self.set |= long(1) << n
        
    def __eq__(self, other):
        return self.set == other.set
        