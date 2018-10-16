# Organism module
# The general superclass for all organisms in the simulation
# Part of the EcoSym Project

import threading
import sys
import random
from location import Location
from helper_functions import random_pick
from helper_functions import with_lock

# This class represents one organism of some type
# It includes two major components:
# 1. Functions for general initialization and running of an organism
#    and handling the concurrent nature of the organisms (which are 
#    also threads)
# 2. Functions useful for most if not all organisms
#    that are commonly used in most subclasses

class Organism(threading.Thread):
    # Creates an organism given the host ecosystem and an optional location 
    # (useful if the creature is a newborn or specifically placed).
    # If no location is provided, the organism will be randomly placed
    def __init__(self, ecosystem, location=None):
        threading.Thread.__init__(self)
        if location is None: # If called w/o specific location,
			     # give random
            random.seed() # This seed is actually globally important
            row = random.randint(0, ecosystem.vdim - 1) # these are inclusive
            col = random.randint(0, ecosystem.hdim - 1)
            location = Location(row, col)
        self.location = location
        self.wasEaten = False
        self.beEatenLock = threading.Lock()
        self.survivalProbability = 0 # probability of surviving being eaten

        # variables for motion
        # the direction impacts mark the orientation of the creature and should 
        #   be between -1 and 1
        # the movement impact is the speed of the creature and should logically 
        #   be positive although negative speeds and high/low directions will 
        #   be calculated without errors
        self.directionXImpact = 0
        self.directionYImpact = 0
        self.movementImpact = 0 # this is actually "speed" 
        self.ecosystem = ecosystem

    # calling (the built-in threading function) start on a thread runs the run()
    # function, so the actions we want the thread to run go in the run() func
    def run(self) :
        while self.ecosystem.simulationRunning == True:
            self.ecosystem.barrier.wait()

            # in case simulation ended while thread was blocked
            if self.ecosystem.simulationRunning == False: 
                break

            if self.wasEaten == True:
                self.die('eaten!')

            self.performStandardAction()
    
    # To be filled out by every inheriting organism.
    # Contains the actions an organism carries out during one tick; defaults to
    #   doing nothing
    def performStandardAction(self):
        return
    
    # Chooses a random direction to face
    # To be overwritten if you have a more sophisticated movement algorithm
    def randomDirection(self):
        self.directionXImpact = random.uniform(-1,1)
        self.directionYImpact = random.uniform(-1,1)
    
    # Using previously-set direction variables, move self in that direction
    def move(self):
        newX = self.location.row+(self.directionXImpact*self.movementImpact)
        newY = self.location.col+(self.directionYImpact*self.movementImpact)
        self.location = self.ecosystem.moveOrganism(self, self.location, 
                Location(newX, newY))
    
    # beEaten is called by predators to attempt to consume this organism
    # It returns data based on success or failure of the attempt
    # This default version, which can be overriden, returns True if the organism
    #   was eaten, False otherwise
    def beEaten(self):
        def getEaten():
            if not self.wasEaten: # in case we've already been eaten
                self.wasEaten = random_pick([True, False], 
                    [1 - self.survivalProbability, self.survivalProbability])
                return self.wasEaten
            else:
                # was eaten but whoever called beEaten wasn't the one who did it
                return False 
        return with_lock(self.beEatenLock, getEaten)
    
    # To handle the death of the organism
    # This function is meant only to be called internally
    def die(self, reason):
        self.ecosystem.reportDeath(self, reason)

        # if we end the thread before calling barrier.wait() we'll have deadlock
        self.ecosystem.barrier.wait() 
                                      
        sys.exit() # Close this thread
    
    # A debug function to print data from this organism
    # Also can be used for output to the user
    def printStatus(self):
        # depends on type of organism
        return



