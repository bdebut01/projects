# EcoSym main file
# Part of the EcoSym Project

import sys
from ecosystem import Ecosystem
from coccolithophores import Coccolithophores
from shark import Shark
from manatee import Manatee
from tuna import Tuna
from grouper import Grouper
from shrimp import Shrimp
from starfish import Starfish
from seablock import SeaBlock
from location import Location
from herring import Herring
import graphic_output

""" Three global dictionaries used for user input """
global creatures
global num_and_what_creatures
global creature_funcs

# ADD YOUR ORGANISM HERE, for recognition purposes
def presetCreatures():
    global creatures
    global creature_funcs
    global num_and_what_creatures
    creatures = dict()
    num_and_what_creatures = dict() # key is creature_id, value is quantity
    creature_funcs = dict()

    # List off creature pairings, add your organism HERE
    creatures[0] = "Coccolithophores"
    creature_funcs[0] = Coccolithophores
    creatures[1] = "Shrimp"
    creature_funcs[1] = Shrimp
    creatures[2] = "Shark"
    creature_funcs[2] = Shark
    creatures[3] = "Tuna"
    creature_funcs[3] = Tuna
    creatures[2] = "Shark"
    creature_funcs[2] = Shark
    creatures[3] = "Tuna"
    creature_funcs[3] = Tuna
    creatures[4] = "Manatee"
    creature_funcs[4] = Manatee
    creatures[5] = "Starfish"
    creature_funcs[5] = Starfish
    creatures[6] = "Grouper"
    creature_funcs[6] = Grouper
    creatures[7] = "Herring"
    creature_funcs[7] = Herring

def userDeclareOceanSize():
    print "--Input Ocean size--"
    print "--------------------"
    print "Example input: '10 10'"
    while True:
        user_input = raw_input()
        # Ignore inputs with anything but 2 values
        if len(user_input.split(' ')) != 2:
            prompt = "Please input a valid ocean size, minimum 1 x 1, "
            prompt += "maximum block^2 is 900"
            print prompt
            continue
        else:
            width, height = user_input.split(' ')
            print "Height: " + str(height) + " Width: " + str(width)
            if not width.isdigit() or not height.isdigit() or int(width) < 1 \
               or int(height) < 1  or int(width) * int(height) > 900:
                prompt = "Minimum height and width is 1, max block^2 is 900, "
                prompt += "try again"
                print prompt
            else:
                confirmation = "OK, ocean width: " + str(width)
                confirmation += " ocean height: " + str(height)
                print confirmation
                print '\n' 
                return (int(width), int(height))

# This function gets input for organisms and places those organisms in the 
#   simulation
# Loop in stdin/stdout receiving organism IDs and quantities
# Stop when 'q' is read in
def inputLoop():
    while True:
        user_input = raw_input()
        if user_input == 'q':
            break
        # Ignore inputs with anything but 2 values
        if len(user_input.split(' ')) != 2:
            continue
        else:
            key, value = user_input.split(' ')
            if not key.isdigit() or not value.isdigit():
                    print 'Input not recognized. Please give a digit.'
                    continue
        if int(key) not in creatures:
            print "That key not found, ignoring"
        else:
            # [0] is key, [1] is quantity
            value = int(value)
            if int(key) in num_and_what_creatures: 
                # already added so we're going to just increment
                res = int(num_and_what_creatures[int(key)])
                value += res

            num_and_what_creatures[int(key)] = value
            if creatures[int(key)][-1] == 'r' or creatures[int(key)][-1] == 'k'\
                or creatures[int(key)][-1] == 'e':
                print str(value) + " " + creatures[int(key)] + "s added"        
            else:
                print str(value) + " " + creatures[int(key)] + " added"

def getSimulationLengthFromUser():
    print "-------------------------------------------------------------------"
    print "---Input number of minutes of marine life you'd like to simulate---"
    print "-------------------------------------------------------------------"
    print "Example input: 60"
    while True:
        user_input = raw_input()
        if not user_input.isdigit():
            print "Please input an integer"
        else:
            print "OK, " + user_input + " simulation minutes"
            return int(user_input)

def inputCreatures():
    # User input simulation duration in ticks
    simMins = getSimulationLengthFromUser()

    # Have user input ocean size
    width, height = userDeclareOceanSize()

    # Load data structures with preset data
    print "---Input Creatures---"
    print "---------------------"
    presetCreatures()

    # Redeclare because we are modifying them in this function
    global creatures
    global num_and_what_creatures

    # Rattle off the dictionary of known creature-name pairings
    print "Known creatures:"
    for c in creatures:
            print (str(c) + ": " + creatures[c])
    print ''
    prompt = "Input desired creatures ids & quantity separated by newline,"
    prompt += " enter 'q' to stop input"
    print prompt
    print "Example input for 10 coccolithophores: "
    print "0 10"
    print ''
    inputLoop()
    return simMins, width, height

def main(argv):
    for i in range(len(argv)):
        if argv[i] == "-g":
            if len(argv)-i == 1: # last argument
                graphic_output.graphics_init("f")
            else:
                graphic_output.graphics_init(argv[i+1])
    
    simMins, width, height = inputCreatures()
    ecosystem = Ecosystem(simMins, width, height)
    ecosystem.loadCreatures(num_and_what_creatures, creature_funcs, creatures)

    ecosystem.startSimulation()

if __name__ == '__main__':
    main(sys.argv)

