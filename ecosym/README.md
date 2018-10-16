# ECOSYM

By: Reema Al-Marzoog, Ben deButts, Nathan Stocking

Date: December 11, 2015


## Project Description


We created a simulation of a marine ecosystem. The ecosystem contains marine 
organisms and simulates the relationships between these organisms. We also 
simulate a couple of natural processes that occur in such ecosystems.

The project primarily uses object polymorphism and separate threads to represent
organisms or groups thereof. There is a central ecosystem class which contains 
the shared state of the ocean and stores data and functions allowing organisms 
to read and affect changes to the ocean.


## How To Run Code


In order to run the project, you will need python installed and the Pillow image
library.
To start, type 
    `python main.py`
at a terminal. You have the option to include command-line parameters to specify
the way in which the graphics will be implemented, as follows:
1. If no parameters are provided, the graphics are disabled.
2. If you use the command line flag `-g` with no extra arguments, the default 
    graphics behavior (output only to file) will be enabled.
3. If you would like other graphics parameters, you can specify an argument to 
    the `-g` flag, which can contain any of the following characters:
    1. `f` - enables output to image files in the current directory
    2. `s` - automatically opens the default image viewer with the current frame
    3. `d` - debug output of the last frame to a csv file (not really intended for
        use)

Examples:
To launch the simulation with graphics output to file, enter

`python main.py -g`

To launch a simulation with automatic graphics output and files, enter

`python main.py -g fs`

Once you have launched the simulation, you must answer some questions about the 
specific simulation parameters you would like to use. The program will prompt 
you for input and provide examples. Follow all instructions to launch the 
simulation.

Note:
The prompts will ask you to choose how many minutes of marine life you'd like to
simulate. This is because we consider each tick of time to approximate one 
minute's worth of an organism's actions. In real time, each tick will last for
about a second (so, a real world second approximates a minute of simulated 
marine life).


## Directory & Files explanation


main.py
-- contains the main function, which prompts the user for input, retrieves it, 
    instantiates an Ecosystem with the appropriate parameters, and starts the 
    simulation
-- imports ecosystem and all of the organisms (used for allowing the user to 
    decide how many of each organism to populate the ocean with)

ecosystem.py
-- contains the definition of the Ecosystem class
-- This class is the centralized mechanism that does most of the work of 
    launching, running, and displaying the simulation.
-- imports all of the organisms, seablock, location, foodchain, as well as Lock,
    Barrier, and with_lock (a helper function) for synchronization.

seablock.py
-- contains the definition for the SeaBlock class
-- This class stores data about various locations in the ocean, and is used by 
    organisms to see their surrounding environment.
-- imports Set, with_lock, and Lock

foodchain.py
-- contains the definition for the Foodchain class
-- This class is used to store predator-prey relationships between different 
    types of organism.

location.py
-- contains the definition for the Location class
-- This class represents a location in the ocean, used to locate the creature 
    geographically.

organism.py
-- contains the definition for the Organism class
-- This class is the parent for all organisms in the ocean, and implements 
    general functions to facilitate the operation of various types of organisms.
-- imports threading, random, location, and helper_functions

fish.py
-- contains the definition for the Fish class
-- This class inherits from organism, and represents a general type of creature 
    which is mobile, does not inherently operate in groups, and reproduces 
    sexually.
-- imports random and organism

barrier.py
-- contains the definition for the Barrier class
-- This class is used to synchronize the simulation such that no deadlock or 
    time confusion occurs.

graphic_output.py
-- contains the definition for the graphicsOutput() function, which can be used 
    to create an image of each tick of the simulation

helper_functions.py
-- contains definitions for two helper functions, with_lock and random_pick
-- with_lock was taken from the class notes
-- random_pick was taken from Python Cookbook, 2nd Edition:http://bit.ly/1QfSwDs

Files that contain class definitions for our organisms. All of them eventually 
inherit from Organism, and some also inherit from Fish:
-- coccolithophores.py
-- grouper.py
-- herring.py
-- manatee.py
-- shark.py
-- shrimp.py
-- starfish.py
-- tuna.py