# Coccolithophores module
# A basic phytoplankton algae to serve as the lowest-level organism
# Part of the EcoSym Project


import ecosystem
import seablock
import location
from organism import Organism
from helper_functions import with_lock

class Coccolithophores(Organism):
    def __init__(self, ecosystem, location=None):
        Organism.__init__(self, ecosystem, location)
        self.population = 10000000

        # coccolithophores fight an interminable war with viruses:
        self.virusWaxWane = -1 # starts waning strength virus
        self.virusEfficiency = 5000 # relatively weak
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        if loc.getSunlight() > 0:
            # reproduce photosynthetically
            self.population += (self.population * (1 / loc.getSunlight()))
        
        self.population -= self.virusEfficiency

        # simple power-growth
        self.virusEfficiency += (self.virusWaxWane * (self.virusEfficiency / 2))

        # the tables turn
        if self.virusEfficiency <= 100:
            self.virusWaxWane = 1
        elif self.virusEfficiency >= 1000000:
            self.virusWaxWane = -1
        
        if self.population <= 0:
            self.die('population gone')
    
    def beEaten(self):
        def getEaten():
            if not self.wasEaten:
                removed = self.population * 0.0015
                self.population -= removed
                if self.population <= 0:
                    self.wasEaten = True
                return removed
            else:
                return 0
        return with_lock(self.beEatenLock, getEaten)

    def printStatus(self):
        return

