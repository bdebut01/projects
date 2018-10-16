# Ecosystem module
# Handles the high-level mechanisms of the simulation
# Part of the EcoSym Project

from sets import Set
import sys
from location import Location
from barrier import Barrier
from seablock import SeaBlock
from threading import Lock
from foodchain import Foodchain
from coccolithophores import Coccolithophores
from manatee import Manatee
from shrimp import Shrimp
from grouper import Grouper
from shark import Shark
from tuna import Tuna
from starfish import Starfish
from herring import Herring
from helper_functions import with_lock
import time
import graphic_output

class Ecosystem():

    # Creates an Ecosystem that can simulate a marine ecosystem
    # simMins: maximum number of ticks to run simulation for
    # hdim: width of body of water (i.e. horizontal dimension)
    # vdim: height of body of water (i.e. vertical dimension)
    def __init__(self, simMins, hdim, vdim):
        global TICK_TIME
        TICK_TIME = 1 # we're waiting one sec per tick

        self.simulationRunning = False
        self.maxSimTicks = simMins
        self.globalTicks = 0 # num ticks the simulation has been running for
        self.hdim = hdim
        self.vdim = vdim

        self.orgsList = Set()   # Organisms alive/running in simulation
        self.orgsListMutex = Lock()
        self.newborns = []      # Organisms born during current tick
        self.newbornsMutex = Lock()
        self.creatures = dict()
        self.creature_funcs = dict()

        self.__createOcean(hdim, vdim)
        self.__prepopulateCoccolithophores()
        self.__createFoodchain()

        self.barrier = Barrier(0) # for synchronization between ticks
        self.stdoutLock = Lock()  # for printing to stdout
    
    # Creates a 2D array of Seablocks with parameters passed in
    def __createOcean(self, hdim, vdim):
        self.ocean = []
        for i in range(vdim):# vdim == rows
            row = []
            for j in range(hdim):# hdim == columns
                tempblock = SeaBlock()
                row.append(tempblock)
            self.ocean.append(row)
    
    # The "grass" of the ocean, the whole ocean is filled with
    #   coccolithophores, so prepopulate ocean with them in every block.
    def __prepopulateCoccolithophores(self):
        for i in range(self.vdim):
            for j in range(self.hdim):
                plankton = Coccolithophores(self, Location(i,j))
                self.addOrganism(plankton)

    # Add new organism food chain relationships here.
    def __createFoodchain(self):
        self.__foodchain = Foodchain()

        # we use types as keys and values
        self.__foodchain.addRelationship(Manatee, Coccolithophores)
        self.__foodchain.addMultiRelationship(Shark, [Manatee, Tuna, Starfish, 
            Grouper])
        self.__foodchain.addRelationship(Shrimp, Coccolithophores)
        self.__foodchain.addRelationship(Grouper, Shrimp)
        self.__foodchain.addMultiRelationship(Tuna, [Shrimp, Grouper, Herring])
        self.__foodchain.addRelationship(Starfish, Coccolithophores)
        self.__foodchain.addMultiRelationship(Herring, [Shrimp])

    # Returns true if predator can eat prey
    # predator and prey are instances of an Organism subclass
    def isEdible(self, predator, prey):
        return self.__foodchain.isEdible(type(predator), type(prey))

    # Returns a list of organisms in the same SeaBlock as org. 
    def getNeighbors(self, org):
        return self.getSeaBlock(org.location).getOrganisms()

    # Moves an organism from its old location to the new one
    # The organism itself has to decide where it will go
    # and this function will move it and report the new location
    def moveOrganism(self, org, oldLoc, newLoc):
        # remove from oldLoc
        self.getSeaBlock(oldLoc).removeOrganism(org)
        
        # we are simulating a globe ocean, therefore if an organism moves across
        # a boundary, that organism appears on the other side of the world
        while int(newLoc.col < 0): # off west
            newLoc.col += self.vdim
        while int(newLoc.col) >= self.vdim: # off east
            newLoc.col -= self.vdim
        while int(newLoc.row < 0): # off north
            newLoc.row = 0 - newLoc.row
            newLoc.col = newLoc.col + (self.hdim / 2)
            if newLoc.col >= self.vdim:
                newLoc.col -= self.vdim
        while newLoc.row >= self.hdim: # off south
            newLoc.row = self.hdim - newLoc.row # over the pole
            newLoc.col = newLoc.col + (self.hdim / 2)
            if newLoc.col >= self.vdim:
                newLoc.col -= self.vdim

        newLoc.col = newLoc.col % self.hdim
        newLoc.row = newLoc.row % self.vdim
        
        # having calculated the correct destination, we just move it there
        self.getSeaBlock(newLoc).addOrganism(org)
        return newLoc

    # Called in main to load the creatures the user typed in before the 
    # simulation starts running. 
    def loadCreatures(self, num_and_what_creatures, creature_funcs, creatures):
        self.creatures = creatures
        self.creature_funcs = creature_funcs
        # Loop thru num_and_what_creatures dict for which species and quantities
        for key in num_and_what_creatures:
            # for every creature of that species
            for i in range(num_and_what_creatures[key]): 
                # Instantiate organism using creature function dict, no location
                #   passed so random will be chosen by constructor
                newOrganism = creature_funcs[int(key)](self)
                self.addOrganism(newOrganism)

    def printSimulation(self):
        # Loop through private organism set, calling their print methods
        def print_orgs():
            for org in self.orgsList:
                org.printStatus()
        with_lock(self.orgsListMutex, print_orgs)
        print str(len(self.orgsList)) + " organisms alive"

    # Adds an organism to the Ecosystem's set of organisms
    def addOrganism(self, org):
        self.getSeaBlock(org.location).addOrganism(org)
        with_lock(self.orgsListMutex, lambda : self.orgsList.add(org))

    # Notifies ecosystem that newborn was born
    # newborn: an instance of an Organism subclass
    def reportBirth(self, newborn):
        with_lock(self.newbornsMutex, lambda : self.newborns.append(newborn))
    
    # Notifies ecosystem that organism died
    # organism: the instance of an Organism subclass that died
    # reason: reason for death as string
    def reportDeath(self, organism, reason):
        self.getSeaBlock(organism.location).removeOrganism(organism) 

        def remove():
            if organism in self.orgsList:
                self.orgsList.remove(organism)
        with_lock(self.orgsListMutex, remove)

        def printDeath():
            name = type(organism).__name__.lower()
            print "A " + name + " died because: " + reason
        with_lock(self.stdoutLock, printDeath)

    # Returns a SeaBlock given a location
    # Can take decimal locations, as mobile creatures store this
    def getSeaBlock(self, location):
        return self.ocean[int(location.row)][int(location.col)]
    
    # Used to initiate the simulation when all parameters have been set
    def startSimulation(self):
        self.simulationRunning = True

        self.__setBarrier()

        # start all organism threads
        def startOrganisms():
            for org in self.orgsList:
                org.start()
        with_lock(self.orgsListMutex, startOrganisms)

        # Start infinite control loop
        self.__loop() 
        sys.exit()

    # Control loop
    # Helps with synchronization, updates organisms list and starts newborn
    # threads as necessary, ends the simulation when the simulation is over
    # (either after self.globalTics ticks of time or when all organisms are
    # gone)
    def __loop(self):
        self.printDivider()

        while self.simulationRunning:
            # sleep for TICK_TIME, so entire simulation has a normal heartbeat
            time.sleep(TICK_TIME)

            # after phase1, orgs are done with actions, we can do maintenance 
            self.barrier.phase1()

            self.printSimulation()
            graphic_output.graphicsOutput(self.orgsList, "frame" + 
                    str(self.globalTicks) +".jpg", self.hdim, self.vdim)
            
            self.__addAndStartNewborns()
            with_lock(self.orgsListMutex, self.endSimulationIfNoOrganisms)
            self.__setBarrier()
            self.globalTicks += 1
	    
	    # Print world stats every 10 ticks
            if self.globalTicks % 10 == 0:
                self.printRealStats()
	    
  	    # If exceed the number of ticks set by user, stop simulation
            if self.globalTicks >= self.maxSimTicks:
                self.simulationRunning = False

            if self.simulationRunning:
                self.printDivider()

            # reach barrier, allow everyone to go on to the next step
            self.barrier.phase2()

        self.printFinalStats()

	# End all remaining threads
        def endThreads():
            for org in self.orgsList:
                org.join()
        with_lock(self.orgsListMutex, endThreads)

        return 

    # Prints a divider that contains the current tick number
    def printDivider(self):
        divider = "-" * (54 + len(str(self.globalTicks)))
        print divider
        print "----------------------- Tick " + str(self.globalTicks) \
          + " ------------------------"
        print divider

    # Prints an appropriate divider and stats about the state of the simulation
    def printFinalStats(self):
        print "------------------------------------------------------"
        print "------------------- Final Results --------------------"
        print "------------------------------------------------------"
        self.printRealStats()

    # Prints stats about the number of each type of organism alive
    def printRealStats(self):
        print '----- DEETS -----'
        for c in self.creature_funcs:
            counter = 0
            temp = self.creature_funcs[c]
            for org in self.orgsList:
                if type(org) == temp:
                    counter += 1
            print self.creatures[c] + " population: " + str(counter)
        print '-----------------'
        print ''

    # Adds newborn organisms to the ecosystem's set of organisms and starts the
    #   threads
    # If the thread limit is reached, some newborns will not be started and will
    #   instead be removed from the ecosystem
    def __addAndStartNewborns(self):
        for newborn in self.newborns:
            self.addOrganism(newborn)

        self.__setBarrier() # so that new threads started immediately block

        excessThreads = []
        def startThreadsUpToLimit():
            for org in self.orgsList:
                if not org.isAlive():
                    try:
                        org.start()
                    except Exception as e:
                        # we've reached the thread limit
                        excessThreads.append(org)
        with_lock(self.orgsListMutex, startThreadsUpToLimit)

        # if we've reached the thread limit, some newborns don't get to live
        for thread in excessThreads:
            self.reportDeath(thread, 'too many threads')

        self.__setBarrier() # if there were excess threads, n is incorrect

        self.newborns = []

    def endSimulationIfNoOrganisms(self):
        if len(self.orgsList) <= 0:
            print "No more organisms; ending simulation"
            self.simulationRunning = False

    # Sets the value of the barrier to the appropriate number
    def __setBarrier(self):
        # + 1 because ecosystem itself is being counted
        numThreads = len(self.orgsList) + 1
        with_lock(self.orgsListMutex, lambda : self.barrier.setN(numThreads))


