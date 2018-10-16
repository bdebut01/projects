# Primary predator of coccolithophores, tho in real life, they eat plants not 
# plankton
import random
from organism import Organism

class Manatee(Organism):
    def __init__(self, ecosystem, location = None, isNewborn = False):
        Organism.__init__(self, ecosystem, location)
        
        if isNewborn:
            self.ticksAlive = 0
        else: # Give insantiated manatee random age
            self.ticksAlive = random.randint(0, 60)

        # Set gender
        self.sex = "M" if random.randint(0, 1) == 0 else "F"
	
	# Only needed for random age setter, but either way, check maturity
        self.checkMaturity()

        # Who knew? Manatees can live up to 60 years old
        self.lifespanTicks = 60 * 365 * 24 * 60 # years * days * hours * mins
        self.survivalProbability = 0.2 # don't think they are the best survivors
        self.movementImpact = .1
        self.hunger = 50
        self.ticksSinceLastChild = 0

    def performStandardAction(self):
        if self.ticksAlive >= self.lifespanTicks:
            self.die('old age!') # die of old age
	
	# Needed to keep track of how old children are, reproduction reasons
        if self.ticksSinceLastChild != 0: self.ticksSinceLastChild += 1
        
        self.checkMaturity()

        # Seablock Details
        prey = None
        neighborOrgs = self.ecosystem.getNeighbors(self)
        for org in neighborOrgs:
            if type(org) == type(self): # found a fellow manatee!
                if org.sex != self.sex: # opposite gender
                    if self.canReproduce(): # if i am eligible
                        self.reproduce() # go for it
                        self.ticksSinceLastChild += 1 # reset child age
                    break
            elif self.ecosystem.isEdible(self, org): # try and eat it
                prey = org
                break
       	    if prey != None:
            	food = prey.beEaten()
            	self.hunger -= (food/15000) # decrease hunger
        
        self.hunger += 1 # every tick get 1 more hunger unit

        if self.hunger > 100: # starve, (like normal animals, not like threads)
            self.die('starvation!')
        self.randomDirection()
        self.move()
        self.ticksAlive += 1

    def reproduce(self):
        babyMan = Manatee(self.ecosystem, self.location)
        self.ecosystem.reportBirth(babyMan)

    def checkMaturity(self):
        # Reach maturity at 5 years for females, 9 years for male
        if self.sex == "M":
            maturityAge = 9 * 365 * 24 * 60
            self.isMature = True if self.ticksAlive > maturityAge else False
        else:
            maturityAge = 5 * 365 * 24 * 60
            self.isMature = True if self.ticksAlive > maturityAge else False

    # So there are a lot details to manatee reproduction, I'm going to do a 
    #    simplification that attempts to prevent mana-mania.
    # Can only produce a new baby manatee every 2 years after reached mature.
    def canReproduce(self):
        if self.isMature:
            if self.sex == "F": # Female?
                # How long since last child?
                if self.ticksSinceLastChild > (2 * 365 * 24 * 60): 
                    return True
            else:
                # male, so can always reproduce when mature
                return True
        return False

    def printStatus(self):
        #print "Manatee here"
        return

