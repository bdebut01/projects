# Fish module
# An abstract superclass for various types of fish that implements standard 
#   behaviors
# Part of the EcoSym Project

import random
from organism import Organism

# Defines behaviors common to most fish. Inherits from Organism.
class Fish(Organism):

    # Constructor for Fish
    # lifespanYears: lifespan in years as an int or float of the Fish
    # maturityYears: age in years as an int or float at which to reach maturity
    def __init__(self, ecosystem, lifespanYears, maturityYears, location = None,
            isNewborn = False):
        Organism.__init__(self, ecosystem, location)

        self.lifespanTicks = lifespanYears * 365 * 24 * 60 # convert to mins
        self.maturityTicks = maturityYears * 365 * 24 * 60
        self.hunger = 10
        self.starvationLevel = 20

        self.__initializeSex()
        self.__initializeAgeAndMaturity(isNewborn)

    # Looks for prey and mates, moves, and does lifespan maintenance.
    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age

        self.__updateMaturityLevel()
        self.__lookForPreyAndMates()
        self.__handleAndUpdateHunger()
        self.__chooseDirectionAndMove()
        self.ticksAlive += 1

    def printStatus(self):
        return

    def __initializeSex(self):
        if random.randint(0, 1) == 0:
            self.sex = "M"
        else:
            self.sex = "F"

    def __initializeAgeAndMaturity(self, isNewborn):
        if isNewborn:
            self.ticksAlive = 0
        else:
            self.ticksAlive = random.randint(0, self.lifespanTicks - 1)

        self.isMature = self.ticksAlive >= self.maturityTicks

    # Checks if Fish has matured and updates self.isMature accordingly
    def __updateMaturityLevel(self):
        if self.isMature == False and self.ticksAlive >= self.maturityTicks:
            self.isMature = True

    def __lookForPreyAndMates(self):
        neighborOrgs = self.ecosystem.getNeighbors(self)
        for org in neighborOrgs:
            if type(org) == type(self): # found a fellow fish!
                if self.isMature and org.isMature:
                    if self.sex == "F" and org.sex == "M":
                        self.reproduce()
                        break
            elif self.hunger > 0 and self.ecosystem.isEdible(self, org):
                ate = org.beEaten()
                if ate: # if the prey didn't manage to get away
                    self.hunger -= 1
                    break

    # Checks if Fish has starved; if yes dies, else increments hunger.
    def __handleAndUpdateHunger(self):
        if self.hunger > self.starvationLevel:
            self.die('starvation!')

        self.hunger += 1 # every tick get 1 more hunger unit

    def __chooseDirectionAndMove(self):
        self.randomDirection()
        self.move()



                


