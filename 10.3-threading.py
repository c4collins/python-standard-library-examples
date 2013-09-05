## 10.3 threading - Manage Concurrent Operations
# Using threads allows a program to run multiple operations concurrently in the same process space
# The threading module builds on low level features of thread to make working with threads easier
import threading
import time
import logging
import random

# The logging mpodule supports embedding the threadname in every log message
# Using the the formatter code %(threadName)s.
# logging is threadsafe.
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(threadName)-10s) %(message)s", datefmt='%H:%M:%S', )

## 10.3.1 Thread Objects
# The simplest way to start a Thread is to instantiate it with a target function and call start()
def worker( sleep_for=0 ):
    """thread worker function"""
    logging.debug( 'Starting' )
    time.sleep( sleep_for )
    logging.debug( 'Ending' )
    return

threads = []
for i in xrange(2):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

# This example passes a number, which the thread then prints


def server ( num, sleep_for=0 ):
    """thread server function"""
    logging.debug( 'Starting' )
    logging.info( 'server-%s' % num )
    time.sleep( sleep_for )
    logging.debug( 'Ending' )
    return

for i in xrange(2):
    t = threading.Thread( target=server, args=(i, ) )
    threads.append(t)
    t.start()

## 10.3.2 Determining the Current Thread
# Using arguments to identify or name the thread is cumbersome and unnecessary.
# Each Thread has a name with a default value that can be changed as the thread is created.
# Naming threads is useful in server process made up of multiple service threads handling different operations

w1 = threading.Thread( name="worker", target=worker, args=( 2, ) )
w2 = threading.Thread( target=worker, args=( 2, ) )
s = threading.Thread( name="server", target=server, args=( "server", 3, ) )

w1.start()
w2.start()

s.start()

## 10.3.3 Daemon vs Non-Daemon Thread
# A Daemon runs without blocking the main program from exiting

def daemon( sleep_for=0 ):
    logging.debug( 'Starting' )
    time.sleep( sleep_for )
    logging.debug( 'Ending' )
    return

d = threading.Thread(name='daemon', target=daemon, args=(20, ) )
d.setDaemon(True)

def non_daemon(  ):
    logging.debug( 'Starting' )
    logging.debug( 'Ending' )
    return

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()
# notice there's no daemon-Ending log in the output because the daemon ends after it dies.

# To wait until a daemon ends, use join()
d2 = threading.Thread(name='daemon2', target=daemon, args=(2, ) )
d2.setDaemon(True)
t2 = threading.Thread(name='non-daemon2', target=non_daemon)

d2.start()
t2.start()

# Join the threads
d2.join()
t2.join()

# It's also possible to set a timeout on the join, in case some jerk set it for 20 seconds
t3 = threading.Thread(name='non-daemon3', target=non_daemon)
t3.start()

d.join(2)
t3.join()

# Since the timeout is less than the amount of time remaining the sleeping daemon thread join returns before the daemon ends

## 10.3.4 Enumerating All Threads
# enumerate() returns a list of all active Thread instances
# The list includes the current Thread which MUST be skipped at risk of deadlock.
def random_worker():
    t = threading.currentThread()
    pause = random.randint(1,5)
    logging.debug('sleeping %s', pause )
    time.sleep(pause)
    logging.debug('ending')
    return

for i in range(3):
    t = threading.Thread(target=random_worker)
    t.setDaemon(True)
    t.start()

main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    logging.debug('joining %s', t.getName())
    t.join(6)

## 10.3.5 Subclassing Thread
# At startup, a Thread does some basic initialization and then calls its run() method
# which calls the target function passed to the construction.
# To create a subclass of Thread, override run() to do whatever is necessary
# To pass arguments to a custom Thread type, redefine the constructor to save the values in an instance attribute visible from the subclass
class MyThread( threading.Thread ):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        logging.debug( 'running with %s and %s', self.args, self.kwargs )
        return

for i in xrange(5):
    t = MyThread( name="MyThread-%s" % i, args=(i, ), kwargs={'a':'A', 'b':'B'} )
    t.start()

# any return value of run is ignored

## 10.3.6 Timer Threads
# one example of a reason to use a subclass thread is provided by threading.Timer
# A Timer starts its work after a delay and can be cancelled at any point in that delay period

def delayed():
    logging.debug('worker running')
    return

t1 = threading.Timer(3, delayed)
t1.setName('t1')
t2 = threading.Timer(3, delayed)
t2.setName('t2')

logging.debug('setting timers')
t1.start()
t2.start()

logging.debug("waiting before cancelling %s", t2.getName())
time.sleep(2)
logging.debug("cancelling %s", t2.getName())
t2.cancel()
logging.debug('done')
print

# The second timer is never run, and the first appears to run after the rest of the main program is done.
# it is joined implicitly when the main thread is done.

## 10.3.7 Signalling between Threads
# Though the point of threading is to have multiple independent operations running concurrently
# there are times when it's important to synchronize the operations in two or more threads
# Event objects are a simple way to communicate between threads safely
# An Event mananges an internal flag that callers can control with the set() and clear() methods
# Other threads can use wait to pause until the flag is set, blocking progress

def  wait_for_event(e):
    """Wait for event to set before doing anything"""
    logging.debug("wait_for_event starting")
    event_is_set = e.wait()
    logging.debug("event set: %s", event_is_set )

def  wait_for_event_timeout(e, t):
    """Wait t seconds before timeout"""
    while not e.isSet():
        logging.debug("wait_for_event_timeout starting")
        event_is_set = e.wait(t)
        logging.debug("event set: %s", event_is_set )
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')

e = threading.Event()
t1 = threading.Thread(name="block", target=wait_for_event, args=(e, ) )
t1.start()
t2 = threading.Thread(name="nonblock", target=wait_for_event_timeout, args=(e, 2 ) )
t2.start()

logging.debug("Waiting before calling Event.set()")
time.sleep(3)
e.set()
logging.debug("Event is set")

# the wait() method takes an argument representing the number of seconds to wait for the event before timing out.
# It returns a Boolean indicating whether or not the event is set, so the caller knows why wait() returned
# The isSet() method can be used separately on the event without fear of blocking
# wait_for_event blocks waiting for the Event to set, but wait_for_event_timeout just checks periodically

## 10.3.8 Controlling Access to Resources
# In addition to synchronizing the operations of threads, it's also important to control access to shared resources
# Python's built-in data structures are thread-safe as a side-effect of having atomic byte codes protecting them
# Other data structures implemented in Python, or simpler types like integers and floats, do not have that protection
# To guard against simultaneous access to an object, us a Lock object.

class Counter( object ):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug("Waiting for lock")
        self.lock.acquire()
        try:
            logging.debug("Acquired lock")
            self.value = self.value+1
        finally:
            self.lock.release()

def lock_worker(c):
    for i in xrange(2):
        pause = random.random()
        logging.debug("Sleeping %0.02f", pause)
        time.sleep(pause)
        # increment the counter instance
        c.increment()
    logging.debug("Done")

counter = Counter()
for i in xrange(3):
    t = threading.Thread( name="lock_worker-%s" % i, target=lock_worker, args=(counter, ) )
    t.start()

logging.debug("Waiting for lock_worker threads")
main_thread = threading.currentThread()

for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug("Counter: %d", counter.value)

# The Counter manages a Lock to prevent two threads from changing its internal state at the same time.
# If the lock was not used, there's a possibility of missing a change to the value attribute

# To find out whether another thread has acquired the lock without holding up the current thread,
# pass False for the blocking argument to acquire()

def lock_holder( lock ):
    logging.debug("Starting")
    while True:
        lock.acquire()
        try:
            logging.debug("Holding")
            time.sleep(0.5)
        finally:
            logging.debug("Not Holding")
            lock.release()
        time.sleep(0.5)
    return

def hold_worker(lock):
    logging.debug("Starting")
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug("Trying to acquire")
        have_it = lock.acquire(0)
        try:
            num_tries += 1
            if have_it:
                logging.debug("Iteration %d: Acquired", num_tries)
                num_acquires += 1
            else:
                logging.debug("Iteration %d: Not Acquired", num_tries)
        finally:
            if have_it:
                lock.release()
    logging.debug("Done after %d iterations", num_tries)

lock = threading.Lock()
holder = threading.Thread( name="LockHolder", target=lock_holder, args=(lock, ) )
holder.setDaemon(True)
holder.start()

worker = threading.Thread( name="HoldWorker", target=hold_worker, args=( lock, ) )
worker.start()

# It takes worker more than three iterations to acquire the lock three separate times

    ## Re-Entrant Locks
# Normal lock objects cannot be acquired more than once
lock = threading.Lock()
logging.debug(" Lock try 1: %s", lock.acquire() )
logging.debug(" Lock try 2: %s", lock.acquire(0) )
lock.release()

# In a situation where Separate code from the same thread needs to reacquire the lock, use an RLock()
lock = threading.RLock()
logging.debug("RLock try 1: %s", lock.acquire() )
logging.debug("RLock try 2: %s", lock.acquire(0) )

    ## Locks as Context Managers
# Locks implement the context manager API, and are compatible with the with statement
def worker_with(lock):
    with lock:
        logging.debug("Lock acquired via with")
        
def worker_no_with(lock):
    lock.acquire()
    try:
        logging.debug("Lock acquired directly")
    finally:
        lock.release()
        
lock = threading.Lock()
w = threading.Thread(name="with_lock", target=worker_with, args=(lock, ) )
nw = threading.Thread(name="no_with_lock", target=worker_no_with, args=(lock, ) )

w.start()
nw.start()
# These two functions are basically the same thing

## 10.3.9 Synchronizing Threads
# In addition to Events, another way of synchronizing threads is through using a Condition object.
# Because the Condition uses a Lock, it can be tied to a shared resource, allowing multiple threads to wait

# In this example, the consumer() threads wait for the Condition to be set before continuing.
# The producer() thread is responsible for setting the condition and notifying the other threads that they can continue

def consumer(cond):
    """Wait for the condition and use the resource"""
    logging.debug("Starting consumer thread")
    t = threading.currentThread()
    with cond:
        cond.wait()
        logging.debug("Resource is available to consumer")

def producer(cond):
    """Set up the resource to be used by the consumer"""
    logging.debug("Starting producer thread")
    with cond:
        logging.debug("Making resource available")
        cond.notifyAll()

condition = threading.Condition()
c1 = threading.Thread( name="c1", target=consumer, args=(condition, ) )
c2 = threading.Thread( name="c2", target=consumer, args=(condition, ) )
p = threading.Thread( name="p", target=producer, args=(condition, ) )

c1.start()
time.sleep(2)
c2.start()
time.sleep(2)
p.start()

## 10.3.10 Limiting Concurrent Access to Resources
# Sometime sit is useful to allow more than one worker access a resource a t a time, while limiting the overall number
# A connection poolmight support a fixed number of simultaneous connectons, or a network application might support a fixed number of concurrent downloads.
# A Semaphore is one way to manage thone connections

class ActivePool( object ):
	def __init__(self):
		super( ActivePool, self).__init__()
		self.active = []
		self.lock = threading.Lock()
	def makeActive(self, name):
		with self.lock:
			self.active.append(name)
			logging.debug('Running: %s', self.active)
	def makeInactive(self, name):
		with self.lock:
			self.active.remove(name)
			logging.debug('Running: %s', self.active)
			
def pool_worker(s, pool):
	logging.debug("Waiting to join the pool")
	with s:
		name = threading.currentThread().getName()
		pool.makeActive(name)
		time.sleep(0.1)
		pool.makeInactive(name)

pool = ActivePool()
s = threading.Semaphore(2)
for i in xrange(4):
	t = threading.Thread( target = pool_worker, name=str(i), args=(s, pool) )
	t.start()
	
## 10.3.11 Thread Specific Data
# While some resources need to be locked so multiple threads can use them, 
# others need to be protected so they are hidden from threads that do not own them
# The local() function creates an object capable of hiding values from views in other threads

def show_value(data):
	try:
		val = data.value
	except AttributeError:
		logging.debug('No value yet')
	else:
		logging.debug('value=%s', val)
		
def value_worker(data):
	show_value(data)
	data.value = random.randint(1,100)
	show_value(data)
	
local_data = threading.local()
show_value(local_data)
local_data.value = 1000
show_value(local_data)

for i in xrange(2):
	t = threading.Thread(name="Value Thread %d" % i, target=value_worker, args=(local_data,) )
	t.start()
	
# local_data.value is not available until it's set in that thread

# To initialize the settings so that all threads start with the same value, \
# use a subclass and save the values in __init__

class MyLocal( threading.local ):
	def __init__(self, value):
		logging.debug('Initializing %r', self)
		self.value=value
		
local_data = MyLocal(1000)
show_value(local_data)

for i in xrange(2):
	t = threading.Thread(name="Local Value %d" % i, target=value_worker, args=(local_data,) )
	t.start()
