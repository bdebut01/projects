# graphic_output module
# Handles printing of graphics from the ecosystem
# Part of the EcoSym Project
# Mostly written by Nathan Stocking (contact for questions)
#   with contributions from Reema Al-Marzoog and Ben DeButts
# Employs the Pillow module. If an import error results, use
#   sudo pip install Pillow

# import each organism type for printing
from coccolithophores import Coccolithophores
from shrimp import Shrimp
from tuna import Tuna
from shark import Shark
from manatee import Manatee
from starfish import Starfish
from grouper import Grouper
from herring import Herring
from PIL import Image
from location import Location
import random

# Colors for each organism are specified here.
# If an organism is not mentioned, it may have a more sophisticated mechanism.
# Shapes are not specified, as more complex calculations are performed.
shrimpColor = (236, 69, 240)
tunaColor = (255, 251, 10)
sharkColor = (235, 23, 17)
manateeColor = (103, 242, 232)
seastarColor = (238,128,21)
grouperColor = (196,188,169)
herringColor = (138, 215, 110)

# These variables store which types of graphics output are enabled
gOutputToFile = False
gOutputToDefault = False
gOutputToDebug = False

# This function takes a string provided via command line argument
#   and sets various parameters of the graphics system
def graphics_init(params):
    global gOutputToFile
    global gOutputToDefault
    global gOutputToDebug
    for c in list(params):
        if c == 'f':
            gOutputToFile = True
        if c == 's':
            gOutputToDefault = True
        if c == 'd':
            gOutputToDebug = True


# Call this function with a list of organisms, a width and height in blocks and 
#   a graphic will result
def graphicsOutput(orgsList, filename, rows, cols):
    # check if graphics are desired at all
    if not(gOutputToFile or gOutputToDefault or gOutputToDebug): return

    # set up a blank image (all black)
    vdim = 51 * rows
    hdim = 51 * cols
    picture = Image.new("RGB", (hdim, vdim))
    pix_map = picture.load()

    # draw white line barriers between blocks
    for i in range(hdim):
        if i % 51 == 0 and i != 0:
            for j in range(vdim): pix_map[i,j] = (255, 255, 255)
        for j in range(vdim):
            if j % 51 == 0 and j != 0: pix_map[i,j] = (255, 255, 255)

    # now handle printing of each organism in turn
    for org in orgsList:
        if type(org) == Coccolithophores: 
            # coccolithophores manifest as green dots
            # the greater the population, the greener they are
        
            loc = org.location
            cornerH, cornerV, width, height = graphics_location_block(loc)
            for i in range(cornerH, (cornerH + height)):
                for j in range(cornerV, (cornerV + width)):
                    printpixel = random.uniform(0,1)
                    if printpixel > 0.9:
                        r, g, b = pix_map[i,j]
                        g = g + ((255 - g) * ((2000000)/(255 - g + 1)))
                        pix_map[i,j] = (r, g, b)

        # most other organisms print either as squares/rectangles or by 
        #   pre-defined shapes
        if type(org) == Shrimp:
            loc = org.location
            x, y = graphics_location(loc)

            # the greater the population, the bigger the square
            squaresize = 1
            if org.population > 20: squaresize = 2
            if org.population > 50: squaresize = 3
            if org.population > 80: squaresize = 4
            if org.population > 120: squaresize = 5
            if org.population > 160: squaresize = 6
            if org.population > 200: squaresize = 7

            for i in range(x - squaresize, x + squaresize + 1):
                if i < 0: continue
                if i >= vdim: continue
                for j in range(y - squaresize, y + squaresize + 1):
                    if j < 0: continue
                    if j >= hdim: break
                    pix_map[i,j] = shrimpColor

        if type(org) == Shark:
            loc = org.location
            x, y = graphics_location(loc)
            pixels = printFishShape(x, y, hdim, vdim)
            for i in pixels:
                pix_map[i] = sharkColor

        if type(org) == Tuna:
            printStandardOrg(org, pix_map, hdim, vdim, 2, 3, 4, 5, tunaColor)
        if type(org) == Manatee:
            printStandardOrg(org, pix_map, hdim, vdim, 4, 5, 4, 5, manateeColor)
        if type(org) == Starfish:
            printStandardOrg(org, pix_map, hdim, vdim, 2, 3, 2, 3, seastarColor)
        if type(org) == Grouper:
            printStandardOrg(org, pix_map, hdim, vdim, 4, 5, 2, 3, grouperColor)
        if type(org) == Herring:
            printStandardOrg(org, pix_map, hdim, vdim, 1, 2, 4, 5, herringColor)

    if gOutputToFile: picture.save(filename)
    if gOutputToDefault: picture.show()
    if gOutputToDebug: write_picture(pix_map, "test.csv", hdim, vdim)

# Prints an organism in a rectangle shape
# leftX: number of pixels from center to the left edge of the rectangle
# rightX: number of pixels from center to the right edge of the rectangle
# topY: number of pixels from center to the top edge of the rectangle
# bottomY: number of pixels from center to the bottom edge of the rectangle
# color: color the rectangle should be
def printStandardOrg(org, pix_map, hdim, vdim, leftX, rightX, topY, 
        bottomY, color):
    loc = org.location
    x, y = graphics_location(loc)
    for i in range(x - leftX, x + rightX):
        if i < 0: continue
        if i >= vdim: break
        for j in range(y - topY, y + bottomY):
            if j < 0: continue
            if j >= hdim: break
            pix_map[i,j] = color

# Return the pixel coordinates of the block in which the given location can be 
#   found
# Used to print something globally to the block
# e.g. coccolithophores print dots over the entire block, not just in one area
def graphics_location_block(loc):
    return (int(loc.row) * 51, int(loc.col) * 51, 50, 50)

# Return the pixel best located for the given location
# Used to print an organism with more specific location data
# Used in this simulation for all mobile organisms
def graphics_location(loc):
    return (int(loc.row * 51), int(loc.col * 51))

# Function to print a vaguely fish-like shape
# Used for shark because there are only so many rectangles
def printFishShape(x, y, hdim, vdim):
    pixels = []
    colLengths = [1, 1, 1, 2, 2, 3, 3, 2, 2, 1, 1, 0, 0]
    #start 7 columns back, 3 for the tail
    for i in range(x - 7, x + 6):
        if i < 0: continue
        if i >= hdim: break
        for j in range(y-colLengths[(i+7-x)], y+colLengths[(i+7-x)]+1):
            if j < 0: continue
            if j >= hdim: break
            pixels.append((i,j))
    return pixels

# A debug function
# Takes a pixel map and dumps data to a csv file, which can be opened as a 
#   spreadsheet
# This is not intended to be run
# It was included because one of the original writers is blind and used it as a 
#   testing module
def write_picture(picture, filename, hdim, vdim):
    csv = open(filename, "w")
    for i in range(hdim):
        for j in range(vdim):
            r, g, b = picture[i,j]
            csv.write("" + str(r) + " " +str(g) + " " + str(b) + ",")
        csv.write("\n")
