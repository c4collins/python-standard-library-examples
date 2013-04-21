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

connor = collections.Counter('connor collins')
natalie = collections.Counter('natalie bittcher')
print " c ", connor
print " n ", natalie
print "c+n", connor + natalie
print "c-n", connor - natalie
print "c&n", connor & natalie
print "c|n", connor | natalie
print
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

 # deques can be populated from either end (left or right)
  # create and add to the right
d1 = collections.deque()
d1.extend('abcdefg')
print 'extend    :', d1
d1.append('h')
print 'append    :', d1

  # create and add to the left
d2 = collections.deque()
d2.extendleft(xrange(6))
print 'extendleft:', d2
d2.appendleft(6)
print 'appendleft:', d2
print
 # similarly, deques can be accessed from either end
print 'From the right:'
while True:
    try:
        print d1
        d1.pop()
    except IndexError:
        break
print
print 'From the left:'
d2.reverse()
while True:
    try:
        print d2
        d2.popleft()
    except IndexError:
        break
print
print

 # Deques are threadsafe; the contents can be consumed at differend ends by different threads simultaneously
import threading, time

candle = collections.deque(xrange(5))
def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print '%8s: %s' % (direction, next)
            time.sleep(0.1)
    print '%8s done' % direction
    return

left = threading.Thread(target=burn, args=('Left', candle.popleft))
right = threading.Thread(target=burn, args=('Right', candle.pop))

left.start()
right.start()

left.join()
right.join()

 # Deques are also rotatable, like the numbers on a dial
d = collections.deque(xrange(10))
print 'Normal:', d
d.rotate(2)
print '  +2  :', d
d.rotate(-5)
print '  -5  :', d

## namedtuple
print
print 'Named Tuples!'
 # standard tuples use numerical indexes
bob = ('Bob', 30, 'male')
jane = ('Jane', 29, 'female')
print ' Representation:', bob
print '\n Field by index:', jane[0]
print '\n Fields by index:'
for p in [bob, jane]:
    print '%s is a %d year old %s' % p
print
 # using a namedtuple adds a name to the fields as well as the index
Person = collections.namedtuple('Person', 'name age gender')
print 'Type of Person:', type(Person)
bob = Person(name='Bob', age=30, gender='male')
jane = Person(name='Jane', age=29, gender='female')
print ' Representation:', bob
print '\n Field by name :', jane.name
print '\n Field by index:', jane[2]
print '\n Fields by index:'
for p in [bob, jane]:
    print '%s is a %d year old %s' % p
print
 # field names are invalid if they are repeated or conflict with python keywords
 # you can also set the rename option to True and then rename them on the fly
with_class = collections.namedtuple('Person', 'name class age gender', rename=True)
print with_class._fields
two_ages   = collections.namedtuple('Person', 'name age gender age', rename=True)
print two_ages._fields

## OrderedDict!
 # This is a dict that remembers the ore in which its contens were added
print 'Regular dictionary:'
d = {}
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print k, v

print 'Ordered dictionary:'
d = collections.OrderedDict()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'

for k, v in d.items():
    print k, v
print
 # OrderedDicts take the add-order into account when determining equality
print 'dict       :',
d1 = {}
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'
d2 = {}
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print d1 == d2
print 'OrderedDict:',
d1 = collections.OrderedDict()
d1['a'] = 'A'
d1['b'] = 'B'
d1['c'] = 'C'
d2 = collections.OrderedDict()
d2['c'] = 'C'
d2['b'] = 'B'
d2['a'] = 'A'
print d1 == d2


