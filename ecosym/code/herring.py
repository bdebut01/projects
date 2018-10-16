import random
from organism import Organism
from fish import Fish

class Herring(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 19, 10, location, isNewborn)
        self.survivalProbability = 1
        self.movementImpact = .75

    def reproduce(self):
        baby = Herring(self.ecosystem, self.location, True)
        self.ecosystem.reportBirth(baby)

    def printStatus(self):
        return
                

