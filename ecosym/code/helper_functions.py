import threading
import random

# Function taken from Mark Sheldon's COMP 50 class notes 
def with_lock(lock, function):
    lock.acquire()
    try:
        value = function()
    finally:
        lock.release()

    return value

# Chooses an option from some_list based on the probability from
# probabilities that has the same index.
#       
# Written by Kevin Park and Peter Cogolo, as seen in Python
# Cookbook, 2nd Editions: http://bit.ly/1QfSwDs
# 
# Args:
# some_list -- a list of items
# probabilities -- a list of probabilities as integers or floats. Should be of 
#       the same length as some_list. If not, the shorter list will be truncated
#       to match the length of the longer list
# Returns: the option from some_list chosen
def random_pick(some_list, probabilities):

    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

