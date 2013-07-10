## heapq!
 # a heap is a tree-like dtat structure where child nodes can have a sort order relationship with the parent
 # I'm hoping that by writing these examples out I'll understand what that means.

import heapq, math, random
from cStringIO import StringIO

o_data = [random.randint(0,100) for r in xrange(15)]
data = o_data[:]

def show_tree(tree, total_width=36, fill=' '):
    """Pretty-print a tree"""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i+1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write('\n')
        columns = 2**row
        col_width = int(math.floor((total_width * 1.0) /  columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print output.getvalue()[1:]
    print '-' * total_width
    return
# Creating a Heap
heap = []
print 'random :', data
print

for n in data:
    print 'heap   :', heap
    print 'add %3d:' % n
    heapq.heappush(heap, n)
    show_tree(heap)
print
 # since the data is already in memory, however, we can just heapify() it
print 'random :', data
heapq.heapify(data)
print 'heap   :', data
print 'heapified :'
show_tree(data)
 # heapq.heappop(heap) removes and returns the element with the lowest value
for i in xrange(len(data)):
    smallest = heapq.heappop(data)
    print 'pop   %3d:' % smallest
    show_tree(data)
 # heapq.heapreplace(heap, n) allows replacement of heap items while maintaining heap size
data = o_data[:]
heapq.heapify(data)
print 'start:'
show_tree(data)
for n in [0,13]:
    smallest = heapq.heapreplace(data, n)
    print 'replace %2d with %2d:' % (smallest, n)
    show_tree(data)
 # there are a few methods for retreiving data, but sometimes list sort is faster
print 'all       :', data
print '3 largest :', heapq.nlargest(3, data)
print 'from sort :', list(reversed(sorted(data)[-3:]))
print '3 smallest:', heapq.nsmallest(3, data)
print 'from sort :', sorted(data)[:3]
