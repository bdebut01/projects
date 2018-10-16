# Seablock module
# Stores the unit of location used by the simulation
# which stores aspects of the ocean at the given location
# and coordinates the many creatures that can be resident therein
# Part of the EcoSym Project

from sets import Set
from helper_functions import with_lock
from threading import Lock

class SeaBlock :
    # SeaBlock initializer
    # Takes optional arguments for attributes which can also be set using 
    # provided functions
    def __init__(self, salinity = 1, sun = 0, oxygen = 0, pressure = 0, 
            currentXImpact=0, currentYImpact=0):
        self.__salinity  = salinity
        self.__sunlight  = sun
        self.__oxygen  	 = oxygen
        self.__pressure  = pressure
        self.__currentXImpact = currentXImpact
        self.__currentYImpact = currentYImpact
        self.__organisms = Set()

        # stores which organisms are locally available
        # to be used to see what is organisms neighbor another organism
        self.__orgsLock = Lock()

    # clears an organism from the block
    # to be used if the organism dies or travels to a different block
    def removeOrganism(self, organism):
        def remove():
            if organism in self.__organisms:
                self.__organisms.remove(organism)
        with_lock(self.__orgsLock, remove)

    # adds this organism only to the block
    # used when an organism enters the area or when a new one is added 
    def addOrganism(self, Creature) :
        with_lock(self.__orgsLock, lambda : self.__organisms.add(Creature))

    # getters and setters for the attributes of the block
    def setSunlight(self, val) :
        self.__sunlight = val

    def getSalinity(self): return self.__salinity
    def getSunlight(self): return self.__sunlight
    def getOxygen(self): return self.__oxygen
    def getPressure(self): return self.__pressure

    # Returns a list of the organisms that are in the block at the time the
    # function is called. The list is passed by value, not by reference
    def getOrganisms(self): 
        def getOrgs():
            orgsAsList = list(self.__organisms)
            return orgsAsList[:] # return by value, not by reference
        return with_lock(self.__orgsLock, getOrgs)

    def getCurrent(self):
        return (self.currentXImpact, currentYImpact)


    def printAttributes(self):
        print "Salinity: " + str(self.getSalinity())
        print "Sunlight: " + str(self.getSunlight())
        print "Oxygen: " + str(self.getOxygen())
        print "Pressure: " + str(self.getPressure())


