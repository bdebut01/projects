import random
from organism import Organism
from fish import Fish

class Tuna(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 15, 5, location)
        self.survivalProbability = .7
        self.movementImpact = .4

    def reproduce(self):
        newTuna = Tuna(self.ecosystem, self.location, True)
        self.ecosystem.reportBirth(newTuna)

    def printStatus(self):
        return
                

