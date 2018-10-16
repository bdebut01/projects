# Foodchain module
# A system to coordinate what organisms can be eaten by each organism
# Organisms can be represented by any type the user chooses (e.g. strings, ints,
#   Organism class instances, types, etc)
# Part of the EcoSym Project

class Foodchain():
    def __init__(self):
        self.__foodchain = {}

    # Adds a predator-prey relationship to the foodchain.
    def addRelationship(self, predator, prey):
        if predator in self.__foodchain:
            self.__foodchain[predator].append(prey)
        else:
            self.__foodchain[predator] = [prey]

    # Associates all prey in listOfPrey (an array) with the predator
    def addMultiRelationship(self, predator, listOfPrey):
        for prey in listOfPrey:
            self.addRelationship(predator, prey)

    # Returns True if the pred is a predator of prey, False otherwise.
    def isEdible(self, pred, prey):
        if pred in self.__foodchain and prey in self.__foodchain[pred]:
            return True
        else:
            return False

