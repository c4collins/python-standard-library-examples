# encoding:utf-8
## 10.4 multiprocessing - Manage Processes like Threads
# The multiprocessing module includes an API for dividing up work between multiple processes based on the API for threading.
# In some cases, multiprocssing is a drop-in replacement and can be used instead of threading to take advantage of
# multiple CPU cores to avoid computational bottlenecks associated with Python's global interpreter lock.
import multiprocessing
import time
import sys
import random
import collections
import itertools
import operator
import glob
import string

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 10 - Processes and Threads - multiprocessing", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Constants
chapter_sections = [ {},
    {'worker':"Worker",},
    {},
    {'start':'Starting','end':'Exiting',},
    {},{},
    {'start':'Starting','end':'Finished',},
    {},{},{},{},
    {'start':"starting",},
    {},{},{},{},{},{},{},
]

## Functions
def worker( i=0 ):
    """Worker function"""
    logger = logging.getLogger("worker")
    logger.info("%s %d", chapter_sections[1]['worker'], i)

def print_worker():
    """Worker function"""
    print "Print %s" % ( chapter_sections[1]['worker'] )

def fancy_worker(q):
    obj = q.get()
    obj.do_something()

def named_worker( sleep=2 ):
    """Named function"""
    logger = logging.getLogger("named_worker")
    name = multiprocessing.current_process().name
    logger.info("%s %s", name, chapter_sections[3]['start'])
    time.sleep(sleep)
    logger.info("%s %s", name, chapter_sections[3]['end'])

def slow_worker():
    logger = logging.getLogger("slow_worker")
    logger.info("%s slow worker", chapter_sections[6]['start'])
    time.sleep(0.1)
    logger.info("%s slow worker", chapter_sections[6]['end'] )

def exit_error():
    sys.exit(1)

def exit_ok():
    return

def return_value():
    return 1

def raises():
    raise RuntimeError("There was a firefight!")

def terminated():
    time.sleep(3)

def wait_for_event(e):
    """Wait for event to be set before doing anything."""
    logger = logging.getLogger("wait_for_event")
    logger.info('Wait for the event: %s', chapter_sections[11]['start'])
    e.wait()
    logger.info('Wait for the event: e.is_set() -> %s', e.is_set())

def wait_for_event_timeout(e, t):
    """Wait for t seconds and then timeout."""
    logger = logging.getLogger("wait_for_event_timeout")
    logger.info('Wait for the event: %s', chapter_sections[11]['start'])
    e.wait(t)
    logger.info('Wait for the event: e.is_set() -> %s', e.is_set())

def worker_with(lock, stream):
    with lock:
        stream.write("Lock acquired via with\n")

def worker_no_with(lock, stream):
    lock.acquire()
    try:
        stream.write("Lock acquired directly\n")
    except:
        lock.release()

def stage_1(cond):
    """Performs the first stage of work, then notifies stage_2 to continue."""
    logger = logging.getLogger("stage_1")
    name = multiprocessing.current_process().name
    logger.info("Starting: %s", name)
    with cond:
        logger.info( "%s done and ready for stage 2", name )
        cond.notify_all()

def stage_2(cond):
    """wait for the condition telling that stage_1 is done"""
    logger = logging.getLogger("stage_2")
    name = multiprocessing.current_process().name
    logger.info("Starting: %s", name)
    with cond:
        cond.wait()
        logger.info( "%s running", name )

def pool_worker(s, pool):
    logger = logging.getLogger("pool_worker")
    name = multiprocessing.current_process().name
    with s:
        pool.makeActive( name )
        logger.info( "Now running: %s", str(pool) )
        time.sleep( random.random() )
        pool.makeInactive( name )

def key_worker(d, key, value):
    d[key] = value

def producer( ns, event ):
    ns.value = "This is the value."
    ns.my_list.append('This is the fake value')
    event.set()

def consumer( ns, event ):
    logger = logging.getLogger("consumer")
    logger.info("Before event, list: %s", ns.my_list)
    try:
        value = ns.value
    except Exception, err:
        logger.info("Before event, error: %s", err)
    event.wait()
    logger.info("After event: %s", ns.value )
    logger.info("After event, list: %s", ns.my_list)

def start_process():
    logger = logging.getLogger("start_process()")
    logger.info("Starting %s", multiprocessing.current_process().name )

def do_calculation(data):
    return data * 2


def file_to_words( filename ):
    """Read a file and return a sequence of (word, occurrence) values."""
    logger = logging.getLogger("file_to_words")
    STOP_WORDS = set([ 'an', 'and', 'are', 'as', 'be', 'by', 'for', 'if', 'in', 'is', 'it', 'of', 'or', 'py',
                       'that', 'the', 'to', 'with', ])
    TR = string.maketrans( string.punctuation, " " * len(string.punctuation))

    logger.info( "%s reading %s", multiprocessing.current_process().name, filename)
    output = []

    with open(filename, mode='r') as f:
        for line in f:
            if line.lstrip().startswith('#'): # Skip comment lines
                continue
            line = line.translate(TR) # Strip punctuation
            for word in line.split():
                word = word.lower()
                if word.isalpha() and word not in STOP_WORDS and len(word) > 1:
                    output.append( (word, 1) )
    return output



def count_words( item ):
    """Convert the partitioned data for a word to a tuple containing the word and the number of occurrences."""
    word, occurrences = item
    return ( word, sum(occurrences) )


## Classes
class Worker( multiprocessing.Process ):
    logger = logging.getLogger("Worker")

    def run(self):
        logger.info('In %s', self.name)
        return

class FancyClass(object):
    logger = logging.getLogger("FancyClass")

    def __init__(self, name):
        self.name = name

    def do_something(self):
        proc_name = multiprocessing.current_process().name
        logger.info("Doing something fancy in %s for %s!", proc_name, self.name)

class Consumer( multiprocessing.Process ):
    logger = logging.getLogger("Consumer")

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill
                self.logger.info("%s : Exiting", proc_name)
                self.task_queue.task_done()
                break
            self.logger.info("%s : %s", proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

class Task( object ):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __call__(self):
        time.sleep(0.1) # do some work (or pretend to)
        return "%s * %s = %s" % (self.a, self.b, self.a*self.b)
    def __str__(self):
        return "%s * %s" % (self.a, self.b)

class ActivePool( object ):
    logger = logging.getLogger("ActivePool")
    def __init__(self):
        super( ActivePool, self ).__init__()
        self.mgr = multiprocessing.Manager()
        self.active = self.mgr.list()
        self.lock = multiprocessing.Lock()
    def makeActive(self, name ):
        with self.lock:
            self.active.append(name)
    def makeInactive(self, name ):
        with self.lock:
            self.active.remove(name)
    def __str__(self):
        with self.lock:
            return str( self.active )

class SimpleMapReduce( object ):
    logger = logging.getLogger("SimpleMapReduce")
    def __init__( self, map_func, reduce_func, num_workers=None):
        """
        map_func
        Function to map inputs to intermediate data.
        Takes as argument one input value and returns a tuple with the key and a value to be reduced.

        reduce_func
        Function to reduce partitioned version of intermediate data to final output.
        Takes as argument a key as produced by mp_func and a sequence of the values associated with that key

        num_workers
        The number of workers to create in the pool.
        Defaults to the number of CPUs available on the current host.
        """

        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)

    def partition(self, mapped_values):
        """Organize the mapped values by their key.
        Returns an unsorted sequence of tuples with a key and sequence of values.
        """
        partitioned_data = collections.defaultdict( list )
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__( self, inputs, chunksize=1):
        """ Process the inputs through the map and reduce functions given.

        inputs
        An iterable containing the input data to be processed

        chunksize
        The portion of the input data to hand to each worker.
        This can be used to turn performance during the mapping phase.
        """
        print inputs
        map_responses = self.pool.map( self.map_func, inputs, chunksize=chunksize)
        partitioned_data = self.partition( itertools.chain( *map_responses ) )
        reduced_values = self.pool.map( self.reduce_func, partitioned_data )
        return reduced_values

## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections) ):
    logger = logging.getLogger("10.4 multiprocessing - Manage Processes like Threads")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("10.4.1 Multiprocessing Basics")
        # The simplest way to spawn a second process is to instantiate a Process object with a target function
        # and call start() to let it begin working
        for i in xrange(5):
            p = multiprocessing.Process(
                target=worker,
                kwargs={'i':i,}
            )
            p.start()
        # When passing arguments to a Process, the args have to be serializable by pickle.

    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("10.4.2 Importable Target Functions")
        # Because multiprocessing child processes import the script, care must be taken to ensure that the scxript does
        # not start running recursively, by wrapping the application in a check for  __main__ (which isn't used here,
        # but is used on some of the earlier scripts before I started using argparse.
        # Another approach is to import a worker function
        from multiprocessing_import_main import import_worker
        for i in xrange(5):
            p = multiprocessing.Process(
                target=import_worker,
                kwargs={ 'i':i,}
            )
            p.start()

    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("10.4.3 Determining the Current Process")
        # Passing arguments to identify or name the process is cumbersome and unnecessary.
        # Each process has a name with a default value that can be changed as the process is created.
        # Naming processes is useful for keeping track of them,
        # especially in applications with multiple types of processes running simultaneously.
        service = multiprocessing.Process( name="my_service", target=named_worker, args=(4,) )
        worker_0 = multiprocessing.Process( target=named_worker ) # Default Name
        worker_1 = multiprocessing.Process( name="worker 1", target=named_worker )
        worker_2 = multiprocessing.Process( name="worker 2", target=named_worker )

        worker_0.start()
        worker_1.start()
        worker_2.start()
        service.start()

    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("10.4.4 Daemon Processes")
        # By default, the main program will not exit until all children have exited.  This is useful, but there are
        # times when starting a background process that runs without blocking the main program from exiting is useful,
        # Ssuch as in services where there may not be an easy way to interrupt the worker, or where letting it die in
        # the middle of its work does not lose or corrupt data.
        # to mark a process as a daemon, set it's daemon attribute to True <<YDS!>>.  The default is False.
        d = multiprocessing.Process(target=named_worker, kwargs={'sleep':10})
        d.daemon = True
        n = multiprocessing.Process(target=worker)

        d.start()
        time.sleep(1)
        n.start()
        # The daemon function terminates automatically before the main program exits to avoid orphan processes.

    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("10.4.5 Waiting for Processes")
        # To wait until a process has completed its work and exited, use the join() method
        d1 = multiprocessing.Process(target=named_worker, kwargs={'sleep':3})
        d1.daemon = True
        d2 = multiprocessing.Process(target=named_worker, kwargs={'sleep':10})
        d1.daemon = True

        n1 = multiprocessing.Process(target=worker)
        n2 = multiprocessing.Process(target=worker)

        d1.start()
        time.sleep(1)
        n1.start()

        d1.join()
        n1.join()
        # The main process waits for the daemon to exit before terminating because d keeps n open via join()

        # By default, join blocks indefinitely, but it's also possible to pass a timeout argument (float) representing
        # the seconds to wait.  If the process does not complete within that period, join(0)returns anyway.
        d2.start()
        n2.start()

        d2.join(2)
        logger.debug("d2.is_alive(): %s", d2.is_alive())
        n2.join()

        # Since d2 is still active after the timeout, the process is still alive after join() returns.

    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("10.4.6 Terminating Processes")
        # Although it is better to use the 'poison pill' method of signalling a process, if a process appears to be hung
        # or deadlocked, it can be useful to be able to kill it forcefully.
        # Calling terminate() on a process kills the child process.
        p = multiprocessing.Process(target=slow_worker)
        logger.info("BEFORE: %s %s", p, p.is_alive())
        p.start()
        logger.info("DURING: %s %s", p, p.is_alive())
        p.terminate()
        logger.info("TERMINATED: %s %s", p, p.is_alive())
        # It's important to always join after terminating in order to update the process management code
        p.join()
        logger.info("JOINED: %s %s", p, p.is_alive())

    if results.section == 7 or results.section == 0:
        logger = logging.getLogger("10.4.7 Process Exit Status")
        # The status code produced when the process exits can be accessed via the exitcode attribute.
        # The ranges allowed are:
            # == 0  No error was produced
            #  > 0  The process had an error and exited with that code
            #  < 0  The process was killed with a signal of -1 * exitcode
        jobs = []
        for f in [exit_error, exit_ok, return_value, raises, terminated]:
            logger.info("Starting process for %s", f.func_name )
            j = multiprocessing.Process( target=f, name=f.func_name )
            jobs.append(j)
            j.start()

        jobs[-1].terminate()

        for j in jobs:
            j.join()
            logger.info("%15s.exitcode = %s", j.name, j.exitcode)

    if results.section == 8 or results.section == 0:
        logger = logging.getLogger("10.4.8 Logging")
        # When debugging concurrency issues, it can be useful to have access to the internals of the objects provided
        # by multiprocessing.  There is a convenient module-level function to enable logging called log_to_stderr().
        # It sets up a logger object using logging and adds a handler so that log messages are sent to the standard
        # error channel.

        # By default the logging level is set to NOTSET so no messages are produced.
        # Passing in a different level to initialize the logger to the level of detail required.
        multiprocessing.log_to_stderr(logging.DEBUG)

        p = multiprocessing.Process( target=print_worker )
        p.start()
        p.join()

        time.sleep(2)

        # To manipulate the logger directly, use get_logger()
        multiprocessing.log_to_stderr(logging.DEBUG)
        logger = multiprocessing.get_logger()
        logger.setLevel(logging.INFO)
        p = multiprocessing.Process( target=print_worker )
        p.start()
        p.join()

    if results.section == 9 or results.section == 0:
        logger = logging.getLogger("10.4.9 Subclassing Process")
        # Although the simplest way to start a job in a separate process is to use Process and pass a target function,
        # It's also possible to use a custom subclass
        jobs = []
        for i in xrange(5):
            p = Worker()
            jobs.append(p)
            p.start()
        for j in jobs:
            j.join()

    if results.section == 10 or results.section == 0:
        logger = logging.getLogger("10.4.10 Passing Messages to Processes")
        # As with threads, a commonly used pattern for multiple processes is to divide a job up among several workers
        # to run in parallel.  Effective use of multiple processes usually requires some communication between them,
        # so that work can be divided and results can be aggregated.  A simple way to communicate between processes
        # with multiprocessing is to use a Queue to pass messages back and forth.  Any object that can be serialized
        # with pickle can pass through a Queue
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(target=fancy_worker, args=(queue, ))
        p.start()

        queue.put(FancyClass("Fancy Dan"))

        # wait for the worker to finish
        queue.close()
        queue.join_thread()
        p.join()

        # Of course, it's not that impressive when it's just one, is it?
        # This more complex example shows how to manage several worker processes consuming data from a JoinableQueue
        # and passing it back to the parent process.  The poison piss technique is used to stop the workers.
        # After setting up the real tasks, the main program adds one stop value per worker to the job queue.
        # when a worker encounters the special value it breaks out of its processing loop.
        # THe main process beings to use the task queue's join() method to wait for all the tasks to finish before
        # processing the results.

        # Establish queues
        tasks = multiprocessing.JoinableQueue()
        answers = multiprocessing.Queue()

        # Start consumers
        num_consumers = multiprocessing.cpu_count() * 2
        logger.info("Creating %d consumers", num_consumers)
        consumers = [ Consumer(tasks, answers) for i in xrange(num_consumers) ]
        for w in consumers:
            w.start()

        # Enqueue jobs
        num_jobs = 10
        for i in xrange(num_jobs):
            tasks.put( Task(i, i) )

        # Add a poison pill for each consumer
        for i in xrange(num_consumers):
            tasks.put(None)

        # Wait for all the tasks to finish
        tasks.join()

        # Show the results
        while num_jobs:
            result = answers.get()
            logger.info( "Result: %s", result )
            num_jobs -= 1


    if results.section == 11 or results.section == 0:
        logger = logging.getLogger("10.4.11 Signalling Between Processes")
        # The Event class is a simple way to communicate state information between processes.
        # An event can be toggled between set and unset states.
        # users of the event object can wait for it to change from unset to set , using an optional timeout value
        e = multiprocessing.Event()
        w1 = multiprocessing.Process( name="block", target=wait_for_event, args=(e, ), )
        w1.start()
        w2 = multiprocessing.Process( name="nonblock", target=wait_for_event_timeout, args=(e, 2, ), )
        w2.start()

        logger.info("Main waiting before calling Event.set()")
        time.sleep(3)
        e.set()
        logger.info("Main event is set")

        # When wait() times out it returns with an error.
        # The caller is responsible for checking the state with is_set().

    if results.section == 12 or results.section == 0:
        logger = logging.getLogger("10.4.12 Controlling Access to Resources")
        # In situations when a single resource needs to be shared between multiple processes, a Lock can be used to
        # avoid conflicting accesses.

        lock = multiprocessing.Lock()
        w = multiprocessing.Process(target=worker_with, args=(lock, sys.stdout))
        nw = multiprocessing.Process(target=worker_no_with, args=(lock, sys.stdout))

        w.start()
        nw.start()

        w.join()
        nw.join()

    if results.section == 13 or results.section == 0:
        logger = logging.getLogger("10.4.13 Synchronizing Operations")
        # Condition objects can be used to synchronize parts of a workflow so that some run in parallel but others
        # run sequentially, even if they are in separate processes.

        condition = multiprocessing.Condition()
        s1 = multiprocessing.Process(name='s1', target=stage_1, args=(condition,))
        s2_clients = [ multiprocessing.Process(name='s2[%d]' % i, target=stage_2, args=(condition,))
               for i in xrange(1,3)
        ]

        for c in s2_clients:
            c.start()
            time.sleep(1)

        s1.start()
        s1.join()

        for c in s2_clients:
            c.join()

    if results.section == 14 or results.section == 0:
        logger = logging.getLogger("10.4.14 Controlling Concurrent Access to Resources")
        # It may also be useful to allow more than one worker to access a resource at a time, while still limiting
        # the overall number.  For example, a connection pool might support a fixed number of simultaneous connections,
        # or a network application might support a fixed number of concurrent downloads.  A Semaphore is one way to
        # manage those connections.
        pool = ActivePool()
        s = multiprocessing.Semaphore(3)
        jobs = [ multiprocessing.Process( target=pool_worker, name="PW %d" % i, args=( s, pool, ) ) for i in xrange(10)]

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
            logger.info("Now running: %s", str(pool))
        # In this example, the ActivePool class simply serves as a convenient way to track which processes are running.
        # a real resource pool would probably allocate a connection or some other value to the newly active processes
        # and retrieve the value when the task is done.  Here the pool just holds the names of the active processes
        # to show that only 3 are running concurrently

    if results.section == 15 or results.section == 0:
        logger = logging.getLogger("10.4.15 Managing Shared State")
        # In the previous example, the list of active processes is maintained centrally in the ActivePool instance via
        # a special type of list object created by a Manager.  The manager is responsible for coordinating shared
        # information state between all of its users.
        mgr = multiprocessing.Manager()
        d = mgr.dict()
        jobs = [ multiprocessing.Process( target=key_worker, args=(d, i, i*2)) for i in xrange(10) ]

        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

        # by creating the dict/list through the manager, it is shared and updates are seen in all processes.
        logger.info("Results: %s", d)


    if results.section == 16 or results.section == 0:
        logger = logging.getLogger("10.4.16 Shared Namespaces")
        # In addition to dictionaries and lists, Managers can create a shared Namespace.
        mgr = multiprocessing.Manager()
        namespace = mgr.Namespace()
        namespace.my_list = []
        event = multiprocessing.Event()

        p = multiprocessing.Process( target=producer, args=(namespace, event))
        c = multiprocessing.Process( target=consumer, args=(namespace, event))

        c.start()
        p.start()

        c.join()
        p.join()

        # Any names value added to the Namespace is visible to all clients that received the Namespace instance.
        # But updates to mutable values in the namespace are not propagated automatically.

    if results.section == 17 or results.section == 0:
        logger = logging.getLogger("10.4.17 Process Pools")
        # The Pool class can be used to manage a fixed number of workers for simple cases, where the work to be done
        # can be broken up and distributed between workers independently.  The return values from the jobs are collected
        # and returned as a list.  the pool arguments include the number of processes
        # and a function to run when starting the task process ( invoked once per child ).
        inputs = list( xrange(100) )
        logger.info("Inputs  : %s", inputs)

        builtin_outputs = map( do_calculation, inputs )
        logger.info("Built-In: %s", builtin_outputs)

        pool_size = multiprocessing.cpu_count() * 2
        # By default, Pool creates a fixed number of workers and passes jobs to them until there are no more jobs.
        # Setting the maxtasksperchild parameter instructs the Pool to restart a worker after it has finished
        # a number of tasks, preventing long-running workers form consuming ever more system resources.
        pool = multiprocessing.Pool( processes=pool_size, initializer=start_process, maxtasksperchild=2 )
        # Pool.map() functions the same way as map() except the functions run in parallel
        pool_outputs = pool.map( do_calculation, inputs )
        # Since they're running in parallel, close() and join() must be used to sync the main process and ensure
        # proper cleanup.
        pool.close() # no more tasks
        pool.join()  # wrap up current tasks

        logger.info("Pool   : %s", pool_outputs )

    if results.section == 18 or results.section == 0:
        logger = logging.getLogger("10.4.18 Implementing MapReduce")
        # The Pool class can be used to create a simple sinlge-server MapReduce implementation.
        # Although it does not give the full benefits of distributed processing, it does illustrate how easy it is
        # to break down some problems into distributable units of work.
        # In a MapReduce-based system, input data is broken down into chunks for processing by different worker
        # instances.  Each chunk of input data is mapped to an intermediate state using a simple transformation.
        # The intermediate data is then collected together and partitioned based on a key value so that all related
        # values are together.  Finally the partitioned data is reduced to result set.
        # The following example uses SimpleMapReduce to count the "words" in this project, ignoring some common bits
        input_files = glob.glob('*.py')

        mapper = SimpleMapReduce( file_to_words, count_words )
        word_counts = mapper(input_files)
        word_counts.sort( key=operator.itemgetter(1) )
        word_counts.reverse()

        logger.info('\nTOP 20 WORDS BY FREQUENCY\n')
        top20 = word_counts[:20]
        longest = max( len(word) for word, count in top20 )
        for word, count in top20:
            print '%-*s: %5s' % (longest+1, word, count)
        print

else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        argparser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
