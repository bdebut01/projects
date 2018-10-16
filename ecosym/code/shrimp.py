# Shrimp module
# A colony of shrimp to serve as a second-level organism
# Part of the EcoSym Project

import ecosystem
import seablock
import location
import random
from organism import Organism
from helper_functions import with_lock

class Shrimp(Organism):
    def __init__(self, ecosystem, location=None):
        Organism.__init__(self, ecosystem, location)
        self.population = 100
        self.hunger = 50 #h unger is a percentage
    
    def performStandardAction(self):
        loc = self.ecosystem.getSeaBlock(self.location)
        localOrgs = loc.getOrganisms()
        prey = None
        for org in localOrgs:
            if self.ecosystem.isEdible(self, org):
                prey = org # can only eat coccolithophores
                break
        # eat coccolithophores for each member of population
        food = 0
        if prey != None:
            for i in range(self.population):
                food = prey.beEaten()
                self.hunger -= (food/15000)
        # standard increase in hunger
        self.hunger += (self.population / 20)

        # reproduce
        self.population = int(self.population*0.01)

        # if the shrimp were fed well, they will stay
        # otherwise, their speed is based off how barren an area they are in
        self.movementImpact=(20000-food)/20000
        if self.movementImpact < 0: self.movementImpact=0

        #shrimp aren't that bright, so they stay in one direction
        self.randomDirection()
        self.move()

        if self.hunger >= 100:
            self.hunger = 100
            self.population -= 1 #beginning to die of starvation

        if self.population <= 0:
            self.die('population gone')
    
    def beEaten(self):
        def getEaten():
            if not self.wasEaten:
                self.population -= 1
                if self.population <= 0:
                    self.wasEaten = True
                return True
            else:
                return False
        return with_lock(self.beEatenLock, getEaten)


    def printStatus(self):
        #print str(self.population) + " shrimp at ocean location (" + \
        #        str(self.location.row) + ", " + str(self.location.col) + ")"
        return

