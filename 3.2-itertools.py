## 3.2 itertools - Iterator Functions
# The itertiools module includes a set of functions for working with sequence data sets

import itertools

## 3.2.1 Merging and splitting iterators

# chain() takes several iterators as arguments and returns a single iterator that produces the contents of all of them as though they came from a single iterator.

for i in itertools.chain([1,2,3], ['a', 'b', 'c']):
	print i,
print

# izip() returns an iterator that combines elements of several iterators into tuples
# it's like zip() but returns an iterator instead of a list

for i in itertools.izip([1,2,3],['a','b','c']):
	print i
print

# islice() returns an iterator that returns selected items from the input iterator by index
# it takes the same arguments as slice() - [start,] stop[, step]

print 'Stop at 5:'
for i in itertools.islice(itertools.count(), 5):
	print i,
print '\n'

print 'Start at 5, Stop at 10:'
for i in itertools.islice(itertools.count(), 5, 10):
	print i,
print '\n'

print 'By tens to 100'
for i in itertools.islice(itertools.count(), 0, 100, 10):
	print i,
print '\n'

# tee() returns several (default is 2) independent iterators based on a single original input

r = itertools.islice(itertools.count(), 5)
i1, i2 = itertools.tee(r)

# the new iterators share their input, so the original iterator shouldn't be used once the new ones are created.

print 'r:',
for i in r:
	print i,
	if i > 1:
		break
print

print 'i1:', list(i1)
print 'i2:', list(i2)


## 3.2.2 - Converting Inputs

# imap() returns in iterator that calls a function on the values in the input iterators, and returns the results.
# it's similar to map(), except it stops when an input is exhausted instead of inserting a None value.

print '\nDoubles:'
for i in itertools.imap(lambda x:2*x, xrange(5)):
	print i

print '\nMultiples:'
for i in itertools.imap(lambda x,y: (x,y,x*y), xrange(5), xrange(5,10)):
	print '%d * %d = %d' % i

# starmap() works basically the same way, except instead of using two iterators
# it splits up arguments in a single iterator
print "\nStarmap:"
values = [(0,5), (1,6), (2,7), (3,8), (4,9)]
for i in itertools.starmap(lambda x,y:(x, y, x*y), values):
	print "%d * %d = %d" % i

	## the mapping function to imam is f(i1, i2), where starmap is f(i*)

## 3.2.3 Producing New Values

# count() produces an indefinite number of consecutive integers, and can be given a starting point as a first argument
print "\nCounting:"
for i in itertools.izip(itertools.count(1), ['a', 'b', 'c']):
	print i

# cycle() retunrs an iterator that indefinitely repeats the contents of the arguments given.
# this may take up a lot of memory
print "\nCycling:"
for i, item in itertools.izip(xrange(7), itertools.cycle(['a', 'b', 'c'])):
	print (i, item)

# repeat() returns an iterator that produces the same value every time it is accessed
print "\nRepeating:"
for i in itertools.repeat('over-and-over', 5):
	print i

# this is most useful when combined with izip and imap and you need to include invariant values
print "\nRepeating with izip():"
for i, s in itertools.izip(itertools.count(), itertools.repeat('over-and-over', 10)):
	print i, s

print "\nRepeating with imap():"
for i in itertools.imap(lambda x,y:(x, y, x*y), itertools.repeat(2), xrange(5)):
	print "%d * %d = %d" % i

## 3.2.4 Filtering

# dropwhile() returns an iterator that produces elements of the input iterator
# after a condition becomes false for the first time

def should_drop(x):
	print 'Testing:', x
	return (x<1)

print "\nDropping:"
for i in itertools.dropwhile(should_drop, [ -1, 0, 1, 2, -2 ]):
	print "Yielding:", i

# the opposite of dropwhile() is takewhile()
def should_take(x):
	return should_drop(x)

print "\nTaking:"
for i in itertools.takewhile(should_take, [ -1, 0, 1, 2, -2]):
	print "Yielding:", i

# ifilter() works like filter(), but with iterators instead of lists
def check_item(x):
	return should_drop(x)

print "\nifiltering:"
for i in itertools.ifilter(check_item, [ -1, 0, 1, 2, -2]):
	print "Yielding:", i

print "\nifilterfalseing:"
# ifilterfalse() is the exact opposite
for i in itertools.ifilterfalse(check_item, [ -1, 0, 1, 2, -2]):
	print "Yielding:", i


## 3.2.5 Grouping data

# groupby() returns an iterator that produces a set of valuesorganized by a common key.

import operator, pprint

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __repr__(self):
		return '(%s, %s)' % (self.x, self.y)
	def __cmp__(self, other):
		return cmp((self.x, self.y), (other.x, other.y))

		# create a dataset of Point instances
data = list(itertools.imap( Point,
				itertools.cycle(itertools.islice(itertools.count(), 3)),
				itertools.islice(itertools.count(), 7),
				)
			)

print '\nData:'
pprint.pprint(data, width=69)

	# Try to group the unsorted data
print '\nGrouped, unsorted:'
for k, g in itertools.groupby(data, operator.attrgetter('x')):
	print k, list(g)

	# Sort the data
data.sort()
print "\nSorted:"
pprint.pprint(data, width=69)

	# Group the sorted data based on x
print '\nGrouped, sorted:'
for k, g in itertools.groupby(data, operator.attrgetter('x')):
	print k, list(g)