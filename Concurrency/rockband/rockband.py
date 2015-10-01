import pyglet
from pyglet import media
import sys
import threading
from threading import Semaphore

DELIMETER = ' '
REST_NOTE = .3

import time

# Barrier class, based heavily off of Allen's solution for a 
#	'reusable barrier'
class Barrier:
	def __init__(self, n) :
		self.n = n
		self.count = 0
		self.mutex = Semaphore(1)
		self.turnstile = Semaphore(0)
		self.turnstile2 = Semaphore(1)

	def phase1(self) :
		self.mutex.acquire()
		self.count += 1
		if self.count == self.n : #number needed has been reached
			self.turnstile2.acquire() #lock the second
			self.turnstile.release() #unlock the first
		self.mutex.release()
		self.turnstile.acquire() #wait until it is freed
		self.turnstile.release() #release so the next thread can follow
		

	def phase2(self) :
		self.mutex.acquire()
		self.count -= 1
		if self.count == 0 : #all threads have been thru
			self.turnstile.acquire() #lock the first
			self.turnstile2.release() #unlock the second
		self.mutex.release()
		self.turnstile2.acquire() #wait until it is free
		self.turnstile2.release() #release so the next thread can follow

	# Because threads might finish at different times, this method
	#	allows the 'n' expected to finish to decrease when necessary
	def decrementThreads(self) :
		self.n -= 1

	# Threads essentially wait twice: for phase1 and phase2.
	def wait(self) :
		self.phase1()
		self.phase2()


class Instrument(object):
	def __init__(self, src, id_num, notes):
		self.src = src
		self.notes = notes
		self.player = media.Player()
		self.id = id_num

	# The core method of the Instrument class
	#	Parses the note string that it is instantiated with,
	#	skipping |, and only resting on non-numerical characters.
	#	If a digit is found, the pitch and sound is queued, then played.
	#	Digit or not, the loop waits a REST_NOTE before proceeding 
	#	to the barrier. Calling barrier.wait(), the method is not allowed
	#	to proceed until the barrier unlocks.
	def playMusic(self) :
		for c in self.notes :
			if c == '|' : continue #skip the | delimeters
			if c.isdigit() :
				self.player.next_source()
				self.sound = pyglet.media.load(self.src)
				self.player.queue(self.sound)
				self.player.pitch = 2.0 ** (float(c)/12.0)
				print 'Thread ' + str(self.id)
				self.player.play()
			else : print 'Thread ' + str(self.id) + str(c)
			time.sleep(REST_NOTE)
			barrier.wait()

		#Done playing
		print '###Thread ' + str(self.id) + ' is done playing'
		barrier.decrementThreads()


# The thread target function,
#	simply calls the play method within each Instrument.
# 	The playMusic method does all parsing and playing of the note string.
def cueMusician(orchestra, id)  : 
	orchestra[id].playMusic()

# Run the threads
def runThreads(threads) :
	for thread in threads : 
		thread.start()
	for thread in threads :
		thread.join()

	return threads

# Create the thread array, passing the target function: 'cueMusician' 
#	for when the thread needs to begin playing.
def instantiateThreads(orchestra) :
	num_players = len(orchestra)
	return [threading.Thread(target=cueMusician, args = [orchestra, i]) \
		for i in xrange(num_players)]

    
# Parse the lines of the file partitioning on the DELIMETER. 
# Instantiate all instances of instruments, passing them the appropriate 
# 	source location, id number, and note string.
def createInstruments(f) :
	orchestra = []
	count = 0
	for line in f:
		src, x, data = line.partition(DELIMETER)
		orchestra.append(Instrument(src, count, data))
		count += 1

	return orchestra

# Create the barrier that will only allow threads to proceed after all other
#	threads have hit their critical points.
def createBarrier(num_players) : 
    global barrier
    barrier = Barrier(num_players)

def printError(msg) :
    print msg
    exit(1)

def proc_args(args) :
	if len(args) > 2 : printError('Only 1 argument needed')
	if len(args) == 1 : printError('Please provide a text file to read')
	return args[1]


def main(args) :
    filename = proc_args(args)
    f = open(filename, 'r')
    orchestra 	= createInstruments(f)
    threads 	= instantiateThreads(orchestra)
    createBarrier(len(orchestra))
    runThreads(threads)
    print 'Finished!'


if __name__ == '__main__' :     main(sys.argv)




