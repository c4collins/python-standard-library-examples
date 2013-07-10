## Queue
 # A Queue is a FIFO data structure suitable for multithreaded programming
 # add elements with put() and retrieve elements with get()

import Queue, threading

q = Queue.Queue()

for i in xrange(5):
    q.put(i)

while not q.empty():
    print q.get(),
print
 
 # a LifoQueue uses LIFO ordering (duh)
q = Queue.LifoQueue()

for i in xrange(5):
    q.put(i)

while not q.empty():
    print q.get(),
print

 # Priority Queue
 # Processes items based on priority
class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print 'New job       :', description
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

q = Queue.PriorityQueue()

q.put( Job(3, 'Mid-level job'))
q.put( Job(10, 'Low-level job'))
q.put( Job(1, 'Important job'))

def process_job(q):
    while True:
        next_job = q.get()
        print 'Processing job:', next_job.description
        q.task_done()

workers = [ threading.Thread(target=process_job, args=(q,)),
            threading.Thread(target=process_job, args=(q,)),
            ]

for w in workers:
        w.setDaemon(True)
        w.start()
q.join()
