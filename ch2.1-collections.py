## Collections!
import collections
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
 # most_common(n) returns a sequence of the n most frequently encountered value and their count
c = collections.Counter()
with open('data/6of12.txt', 'rt') as f:
    for line in f:
        c.update(line.rstrip().lower())
print 'Most common:'
for letter, count in c.most_common():
    print ' %s: %d' % (letter, count)
