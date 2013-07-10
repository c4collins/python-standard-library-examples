## bisect!
 # bisect maintains a sorted list in sorted order without having to redo the sort each time a new item is added to the list
import bisect, random
# use a constant seed to ensure that the same pseudo-random numbers are used on each loop
random.seed(1)

print 'New  Pos  Contents'
print '---  ---  --------'

# use bisect and insort
l = []
for i in xrange(1,15):
    r = random.randint(1,100)    
    position = bisect.bisect(l, r)
    bisect.insort(l, r)
    print '%3d %3d ' % (r, position), l
print
# use bisect_left and insort_left
random.seed(1)
l = []
for i in xrange(1,15):
    r = random.randint(1,100)    
    position = bisect.bisect_left(l, r)
    bisect.insort_left(l, r)
    print '%3d %3d ' % (r, position), l
