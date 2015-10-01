# Ben deButts
# 09/27/15
# Comp 50cp: Concurrent Programming
# Program: This program, assuming it is passed a normal JPG image, can do 
#   three basic things to an image: switch its r and b values, boost the red 
#   in the image, or turn the image black and white. The program also 
#   utilizes threads to process separate regions of the image, depending on 
#   the row and column limits one calls the program with. 
#
# Synchronization required: I would argue there is little to no 
#   synchronization required. Threads are each given their own, non-overlapping
#   region to operate on, and that's it. Concurrent programming is always 
#   concerned with shared resources, and in this case the shared resource is
#   the pixel map, but threads are not sharing regions of the map. Because there
#   isn't any potential for messing with shared values, no synchronization is
#   needed.

import sys
import threading
from PIL import Image

MAX_THREADS = 150
ROW_DEFAULT = 2
COL_DEFAULT = 2

# Switches the r and b values.
def switch_rb(tuple_rgb) :
    return (tuple_rgb[2], tuple_rgb[1], tuple_rgb[0])

# Somewhat basic, but it adds 100 to the r value, boosting the 
#   image's red amounts.
def boost_red(tuple_rgb) :
    return (tuple_rgb[0] + 100, tuple_rgb[1], tuple_rgb[2])

# Not sure what the actual math for turning an image black and white is,
#   but averaging the three rgb values and returning this value 
#   for each r g and b seems to operate similarly.
def b_w(tuple_rgb) :
    rgb_sum = tuple_rgb[0] + tuple_rgb[1] + tuple_rgb[2]
    new_value = rgb_sum / 3
    return (new_value, new_value, new_value)

dict_acts = {'switch-r-b': switch_rb, 'boost-red': boost_red, 'bw': b_w}

# The thread function which does the actual manipulations of 
#   an image's rgb values. It is passed the pixel map to manipulate,
#   whichever transfer function value is occurring, and then the limits
#   of the region the particular thread is responsible for.
def thread_func(pix_map, tran_func, row_min, row_max, col_min, col_max) :
    for col in xrange(col_min, col_max) :
        for row in xrange(row_min, row_max) :
            r, g, b = pix_map[col, row]
            pix_map[col, row] = tran_func((r, g, b))

# Using the passed width, height, row count, and column count
#   values, the calculator returns what is essentially the interval
#   size [row/col_add] and the leftover number of pixels that might
#   exist [row/col_final]. It returns these calculations to the 
#   thread launching function.
def matrix_calculator(w, h, rc, cc) :
    row_add = col_add = row_final = col_final = 0
    row_final = -1 if h % rc == 0 and rc != 1 else ((h % rc)) # - 1) 
    row_add = h / rc
    col_final = -1 if w % cc == 0 and cc != 1 else ((w % cc))  # - 1)
    col_add = w / cc
    return (row_add, col_add, row_final, col_final)

# Launch threads is the hub of thread launching: it calls the needed
#   calculator functions, and has the central double for loop that 
#   assigns threads to whichever regions of the image. Upon completion
#   of the for loops, it starts the threads running and joins them to
#   wait for all threads to complete.
#
# str_act transformation request, pix_map the pixel map, w width, h height, 
#   rc row count, cc col count
def launch_threads(str_act, pix_map, w, h, rc, cc) :
    # Set incrementor and leftover pixels amounts
    row_add, col_add, row_final, col_final = matrix_calculator(w, h, rc, cc)
    r_min = r_max = c_min = c_max = 0
    threads = [] # will contain the list of all threads
    for x in xrange(rc) :
        r_min = x * row_add
        r_max = r_min + row_add if x != rc-1 else r_min + row_add + row_final
        for y in xrange(cc) : 
            c_min = y * col_add
            c_max = c_min + col_add if y != cc-1 else c_min + col_add +col_final
            threads.append(threading.Thread(target = thread_func, \
                args = [pix_map, dict_acts[str_act], r_min, r_max, \
                c_min, c_max]))
    # Start threads
    for thread in threads :
        thread.start()
    for thread in threads :
        thread.join()

# This function organizes the transformation that will occur on the image.
#   If the supplied row/col count is greater than the number of actual pixels
#   in the image, it brings the count down to the image width/height.
#   If there isn't a supplied row/col count it defaults to the DEFAULT constant.
#   Finally, it opens the image, accesses width and height, then calls the 
#   launch_threads function passing it all the requisite variables.
#   Once launch_threads has returned, the function writes to the name supplied 
#   in the argument list.
def transform_hub(inputs) :
    # Set row and col counts, depending on argument list size
    row_count = ROW_DEFAULT if len(inputs) == 3 else int(inputs[3])
    col_count = COL_DEFAULT if len(inputs) == 3 else int(inputs[4])
    # Open image and access width, height values
    in_img = Image.open(inputs[0])
    pix_map = in_img.load()
    width, height = in_img.size
    # Check for more threads than pixels, setting counts back accordingly 
    if row_count > height : row_count = height
    if col_count > width : col_count = width
    # Launch threads
    launch_threads(inputs[2], pix_map, width, height,
            row_count, col_count)
    # Save and write new file
    in_img.save(inputs[1])


def printError(msg) :
    print msg
    exit(1)

# Error checking function, checks for unknown transformation requests,
#   non-numerical values for the row/col counts, and row/col counts that
#   would exceed the MAX_THREADS constant.
def errorCheck(inputs) :
    # Check for unknown transformation requests
    if inputs[2] not in dict_acts :
        printError('Unknown transform: ' + inputs[2])
   
    # Don't do the following checks if the extra row/col inputs weren't there
    if len(inputs) < 4 : return

    ## Check for last 2 arguments to be integers
    if not inputs[3].isdigit() or not inputs[4].isdigit() :
        printError('Please provide numerical values for arguments 4 and 5')
    
    # Check for too many threads
    if len(inputs) == 5 and (int(inputs[3]) * int(inputs[4])) \
            > MAX_THREADS :
        printError('Row/col exceeded MAX_THREAD count, please pick smaller ' + \
                'numbers')

# Processes the command line arguments, checking for proper number of arguments
#   only.
def proc_args(args) :
    if len(args) < 4 : printError('Please provide at least 3 arguments') 
    elif len(args) == 4 :
        filename, outname, action = args[1:4]
        return (filename, outname, action)
    elif len(args) == 6 :
        filename, outname, action, num_rows, num_cols = args[1:6]
        return (filename, outname, action, num_rows, num_cols)
    else : printError('Please provide either 3 or 5 arguments')

def main(args) :
    inputs = proc_args(args)
    errorCheck(inputs) 
    transform_hub(inputs)

if __name__ == '__main__' :     main(sys.argv)


