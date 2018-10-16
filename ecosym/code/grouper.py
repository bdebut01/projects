import random
from organism import Organism
from fish import Fish

# Example of how easy it is to add a new organism, 
#    in this case, a fish so it inherits from Fish
#    sub-class
class Grouper(Fish):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Fish.__init__(self, ecosystem, 3, 1, location)
        self.survivalProbability = .4
        self.movementImpact = .4

    def reproduce(self):
        newGrouper = Grouper(self.ecosystem, self.location, True)
        self.ecosystem.reportBirth(newGrouper)

    def printStatus(self):
        return
                

