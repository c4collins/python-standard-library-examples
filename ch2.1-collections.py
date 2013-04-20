## collections!
import collections
## Counters!
 # Counters can be used to count how many times equivalent items are added
 # and they can be created a bunch of ways
print collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
print collections.Counter({'a':2, 'b': 3, 'c': 1})
print collections.Counter(a=2,b=3, c=1)
 # sometimes it's easier to start empty and add items
c = collections.Counter()
print ' Initial :', c
c.update('abcdaab')
print ' Sequence:', c
c.update({'a':1, 'd':5})
print ' Dict    :', c
print
 # Counter values can be called similarly to a dict and returns 0 for unknown items
for letter in 'abcde':
    print '%s : %d' % (letter, c[letter])
 # elements() returns an iterator that produces all known items
c = collections.Counter('extremely')
c['z']=0
print c
print list(c.elements())
 # most_common([n]) returns a sequence of (all | [the n]) most frequently encountered value and their count
c = collections.Counter()
with open('data/6of12.txt', 'rt') as f:
    for line in f:
        c.update(line.rstrip().lower())
print 'Most common:'
for letter, count in c.most_common(5):
    print ' %s: %d' % (letter, count)
 # Counters also support arithmetic and set operations
c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('alphabet')
print 'Arithmetic and Set Operations'
print '  C1:', c1
print '  C2:', c2
print '\n Combined counts:'
print '  ', c1+c2
print '\n Subtraction:'
print '  ', c1-c2
print '\n Intersection (taking positive minimums):'
print '  ', c1&c2
print '\n Union (taking maximums):'
print '  ', c1 | c2
print
print

connor = collections.Counter('connor collins')
natalie = collections.Counter('natalie bittcher')
print " c ", connor
print " n ", natalie
print "c+n", connor + natalie
print "c-n", connor - natalie
print "c&n", connor & natalie
print "c|n", connor | natalie

## defaultdict!
 # the standard dict uses setdefault() to set a default value,
 # default dict lets you specify the default up front
def default_factory():
    return 'default value'
d = collections.defaultdict(default_factory, foo='bar')
print 'd:', d
print ' foo =>', d['foo']
print ' bar =>', d['bar']

## deque!
 # deque supports adding and removing elements from both ends

d = collections.deque('abcdefg')
print 'Deque     :', d
print '    Length:', len(d)
print '  Left end:', d[0]
print ' Right end:', d[-1]

d.remove('c')
print 'remove(c):', d
