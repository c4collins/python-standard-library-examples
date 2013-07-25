## 3.3 Operator
## Programmingin python, especially when using iterators, sometimes calls for the creation of one-off functions
## i.e. lambdas, our nameless single-serving friends, but operator defines some functions that correspond to
## arithmetic and comparison.

from operator import *

a = -1
b = 5.0
c = 2
d = 6

print 'a=', a
print 'b=', b
print 'c=', c
print 'd=', d

## 3.3.1 Logical Operations
print '\nnot_(a)     :', not_(a)
print 'truth(a)    :', truth(a)
print 'is_(a. b)   :', is_(a,b)
print 'is_not(a, b):', is_not(a,b)

## 3.3.2 Comparison Operators
for func in (lt, le, eq, ne, ge, gt):
	print '%s(a, b):' % func.__name__, func(a,b)

## 3.3.3 Arithmetic Operators
print '\nPositive/Negative'
print 'abs(a):', abs(a)
print 'neg(a):', neg(a)
print 'neg(b):', neg(b)
print 'pos(a):', pos(a)
print 'pos(b):', pos(b)

print '\nArithmetic:'
print 'add(a,b)     :', add(a,b)
print 'div(a,b)     :', div(a,b)
print 'div(d,c)     :', div(d,c)
print 'floordiv(a,b):', floordiv(a,b)
print 'floordiv(d,c):', floordiv(d,c)
print 'mod(a, b)    :', mod(a,b)
print 'mul(a, b)    :', mul(a,b)
print 'pow(c, d)    :', pow(c,d)
print 'sub(b, a)    :', sub(b,a)
print 'truediv(a, b):', truediv(a,b)
print 'truediv(d,c) :', truediv(d,c)

# floordiv() is integer division, and truediv() is float division

print '\nBitwise:'
print 'and_(c,d)   :', and_(c,d)
print 'invert(c)   :', invert(c)
print 'lshift(c,d) :', lshift(c,d)
print 'or_(c,d)    :', or_(c,d)
print 'rshift(d, c):', rshift(d,c)
print 'xor(c,d)    :', xor(c,d)

e = [ 1, 2, 3 ]
f = [ 'a', 'b', 'c']

print "e =", e
print "f =", f

## 3.3.4 Sequence Operators
print '\nConstructive:'
print 'concat(e, f):', concat(e,f)
print 'repeat(e, 3):', repeat(e,3)

print '\nSearching:'
print 'contains(e, 1 ):', contains(e,1)
print 'contains(f, "d"):', contains(f,"d")
print 'countOf(e, 1):', countOf(e,1)
print 'countOf(f,"d"):', countOf(f,"d")
print 'indexOf(e, 1):', indexOf(e,1)

print '\nAccess Items:'
print 'getitem(f, 1):', getitem(f, 1)
print 'getslice(e, 1, 3):', getslice(e, 1, 3)
print 'setitem(f, 1, "d"):', setitem(f, 1, 'd'),
print ', after f =:', f
print 'setslice(e, 1, 3, [4, 5]):', setslice(e, 1, 3, [4, 5]),
print ', after e =', e

print '\nDestructive:'
print 'delitem(f, 1):', delitem(f, 1), ", after f =", f
print 'delslice(e, 1, 3):', delslice(e, 1, 3), ', after e = ', e

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

print '\nReset'
print 'a=', a
print 'b=', b
print 'c=', c
print 'd=', d

## 3.3.5 In Place Oerators
print '\nIn-place Operators'
a = iadd(a,b)
print 'a = iadd(a,b) =>', a
c = iconcat(c,d)
print 'c = iconcat(c,d) =>', c
# There are lots more
print

## 3.3.6 Attribute and Item Getters
## Getters are callable objects constructed at runtime which allow for the retreival of
## object attributes or contents from sequences.  They are intended to be more efficient than lambdas

class MyObj(object):
	"""attrgetter example class"""
	def __init__(self, arg):
		super(MyObj, self).__init__()
		self.arg = arg
		self.val = arg
	def __repr__(self):
		return 'MyObj(%s)' % self.arg
	# The rest of this applies to 3.3.7
	def __str__(self):
		return 'MyObj(%s)' % self.val
	def __lt__(self, other):
		"""Compare for less-than"""
		print 'Testing %s < %s' % (self, other)
		return self.val < other.val
	def __add__(self, other):
		"""add values"""
		print 'Adding %s + %s' % (self, other)
		return MyObj(self.val + other.val)


l = [ MyObj(i) for i in xrange(5)]
print 'objects   :', l

# Get each object's arg attribute
# Attribute getters work like lambda x, n='attrname': getattr(x, n)
g = attrgetter('arg')
vals = [g(i) for i in l]
print 'arg values:', vals

# Sort using the arg value
l.reverse()
print 'reversed  :', l
print 'sorted    :', sorted(l, key=g)

# Item getters work like lambda x, y=5: x[y]
l = [ dict(val=-1*i) for i in xrange(4)]
print '\nDictionaries:', l
g = itemgetter('val')
vals = [g(i) for i in l]
print 'values      :', vals
print 'sorted      :', sorted(l, key=g)
l = [ (i, i*-2) for i in xrange(4)]
print '\nTuples:', l
g = itemgetter(1)
vals = [g(i) for i in l]
print 'values:', vals
print 'sorted:', sorted(l, key=g)

## 3.3.7 Combining Operators and Custom Classes
## Since operator works via the standard Python interfaces, it works with user-defind classes too

a = MyObj(1)
b = MyObj(2)

print '\nComparison:'
print lt(a, b)

print '\nArithmetic:'
print add(a,b)
print

## 3.3.8 Type Checking

class NoType(object):
	"""Supports none of the type APIs"""

class MultiType(object):
	"""Supports multiple type APIs"""
	def __len__(self):
		return 0
	def __getitem__(self, name):
		return 'mapping'
	def __int__(self):
		return 0

o = NoType()
t = MultiType()

for func in (isMappingType, isNumberType, isSequenceType):
	print '%s(o)' % func.__name__, func(o)
	print '%s(t)' % func.__name__, func(t)