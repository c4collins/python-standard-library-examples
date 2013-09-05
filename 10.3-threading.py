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
def server(num, sleep_for=0):
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

# The second timer is never run, and the first appears to run after the rest of the main program is done.
# it is joined implicitly when the main thread is done.

