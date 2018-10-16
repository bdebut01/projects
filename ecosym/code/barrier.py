from threading import Semaphore

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

    def decrementN(self) :
        self.n -= 1

    def setN(self, n_) :
        self.n = n_

    # Threads essentially wait twice: for phase1 and phase2.
    def wait(self) :
        self.phase1()
        self.phase2()

