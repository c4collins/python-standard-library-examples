## 3.4 contextlib
## Contextlib ocntains utilities for working with context managers and the with statement
## A context manager is responsible for a resource within a block, like a file, possibly creating
## or opening it when the block is entered and then closing or cleaning up as the block is exited.

## Files support the contecxt manager API to make opening ands closing files easy.
 # with open ('/tmp/temp.txt') as f:
 #	f.write('contents go here')
## In this case the file is automatically closed

## A context manager is enabled with the 'with' statement and then uses __enter__ and __exit__ methods

class Context(object):
	def __init__(self):
		print 'Context.__init__()'
	def __enter__(self):
		print 'Context.__enter__()'
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		print 'Context.__exit__()'
		# __exit__() is always called even if an exception is raised, and so a context can replace a try:finally block

with Context():
	print 'Doing work in the context'

print
# __enter__() can return ANY object that you might want to associate with the name given (using the as keyword).

class WithinContext(object):
	def __init__(self, context):
		print 'WithinContext.__init__(%s)' % context
	def do_something(self):
		print 'WithinContext.do_something()'
	def __del__(self):
		print 'WithinContext.__del__'

class Context(object):
	def __init__(self):
		print 'EnterContext.__init__()'
	def __enter__(self):
		print 'EnterContext.__enter__()'
		return WithinContext(self)
	def __exit__(self, exc_type, exc_val, exc_tb):
		print 'EnterContext.__exit__()'

with Context() as c:
	c.do_something()
print

# __exit__() receives arguments containign details of and exception raised in the with block
# If the error can be properly handled __exit__() should return True so the error will not be propagated
# Returning False causes the exception to be reraised after __exit__() returns.

class Context(object):
	def __init__(self, handle_error):
		print '__init__(%s)' % handle_error
		self.handle_error = handle_error
	def __enter__(self):
		print '__enter__()'
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		print '__exit__()'
		print 'exc_type =', exc_type
		print 'exc_val  =', exc_val
		print 'exc_tb   =', exc_tb
		return self.handle_error

with Context(True):
	raise RuntimeError('error message handled')
print


				## this works but kills the program, which is not exactly helpful
#with Context(False):
#	raise RuntimeError('error message propagated')
#print

## 3.4.2 From Generator to Context Manager
## writing out __init__(), __enter__(), and __exit__() isn't really that hard, but sometimes it can be a lot of overhead for something trivial
## The contextmanager() decorator will convert a generator function into a context manager

import contextlib

@contextlib.contextmanager
def make_context():
	print '  entering'
	try:
		yield()
	except RuntimeError, err:
		print '  ERROR:', err
	finally:
		print '  exiting'

print '\nNormal:'
with make_context() as value:
	print '   inside with statement:', value

print '\nHandled Error:'
with make_context() as value:
	raise RuntimeError('showing example of handling an error')

				## this works but kills the program, which is not exactly helpful
#print '\nUnhandled error:'
#with make_context() as value:
#	raise ValueError('this exception is not handled')
print

## 3.4.3 Nesting Contexts
## You can use nested() instead of nexted with statements, if the outer contexts don't need thiri own seperate block

@contextlib.contextmanager
def make_context(name):
	print 'entering:', name
	yield name
	print 'exiting:', name

with contextlib.nested( make_context('A') , make_context('B') ) as ( A , B ):
	print 'inside with statement:', A, B
print

## this is deprecated in python 2.7 because with supports nesting directly, and fixes some of the edge cases that nested() could not

with make_context('A') as A, make_context('B') as B:
	print 'inside with statement:', A, B

## 3.4.4 Closing Open Handles
# While the file class supports the context manager API, some other objects which represent open handles do not. (i.e. the object returned from urllib.urlopen())
# To ensure that a handle is clodes, use closing() to create a context manager for it.

class Door(object):
	def __init__(self):
		print '__init__()'
	def close(self):
		print 'close()'

print '\nNormal Example:'
with contextlib.closing(Door()) as door:
	print '  inside with statement'

print '\nError handling example:'
try:
	with contextlib.closing(Door()) as door:
		print '  inside with statement'
		raise RuntimeError('error message')
except Exception, err:
	print '  Had an error:', err
