## functools!
# allows for adapting or extending fucntions and other callable objects, without completely rewriting them
# primarily through use of the `partial` class, which acts as a wrapper for the original functions and can be used in the same way

import functools

def myfunc(a, b=2):
	"""Docstring for myfunc"""
	print ' called myfunc with:', (a, b)
	return

def show_details(name, f, is_partial=False):
	"""Show details of callable object"""
	print '%s' % name
	print ' object:', f
	if not is_partial:
		print ' __name__:', f.__name__
	if is_partial:
		print ' func:', f.func
		print ' args:', f.args
		print '  keywords:', f.keywords
	return

show_details('myfunc', myfunc)
myfunc('a', 3)
print

# Set a differnt default value for 'b', but require the caller to set 'a'
p1 = functools.partial(myfunc, b=4)
show_details('partial with named default', p1, True)
p1('passing p')
p1('override b', b=5)
print

# Set default values for bot 'a' and 'b'
p2 = functools.partial(myfunc, 'default a', b=99)
show_details('partial with defaults', p2, True)
p2()
p2(b='override b')
print

#print 'Insufficient arguments:'
#p1()

# The partial object does not have __name__ or __doc__ attributes by default
# the update_wrapper() function copies or adds attributes from the original function to the partial object.

def show_details(name, f):
	"""Show details of callable object"""
	print '%s' % name
	print ' object:', f
	print ' __name__:',
	try:
		print f.__name__
	except AttributeError:
		print '(no __name__)'
	print ' __doc__:', repr(f.__doc__)
	print
	return

show_details('myfunc',myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print 'Updating wrapper:'
print '  assign:', functools.WRAPPER_ASSIGNMENTS
print '  update:', functools.WRAPPER_UPDATES
print

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)

# Partials work with any callable objecty, not just with stand-alone functions
class MyClass(object):
	"""Demo class for functools"""

	def method1(self, a, b=2):
		"""Docstring for method1"""
		print '  called method1 with:', (self, a, b)
		return

	def method2(self, c, d=5):
		"""Docstring for method2"""
		print '  called method2 with:', (self, c, d)
		return

	wrapped_method2 = functools.partial(method2, 'wrapped c')
	functools.update_wrapper(wrapped_method2, method2)

	def __call__(self, e, f=6):
		"""docstring for MyClass.__call__"""
		print '   called object with:', (self, e, f)
		return

o = MyClass()

show_details('method1 straight', o.method1)
o.method1('no default for a', b=3)
print

p1 = functools.partial(o.method1, b=4)
functools.update_wrapper(p1, o.method1)
show_details('method1 wrapper', p1)
p1('a goes here')
print

show_details('method2', o.method2)
o.method2('no default for c', d=6)
print

show_details('wrapped method2', o.wrapped_method2)
o.wrapped_method2('no default for c', d=6)
print

show_details('instance', o)
o('no default for e')
print

p2 = functools.partial(o, f=7)
show_details('instance wrapper', p2)
p2('e goes here')


# Updating the properties of a wrapped callable is a good technique when using decorators
# as the new function ends up with all the properties of the undecorated function

def simple_decorator(f):
	@functools.wraps(f)
	def decorated(a='decorated defaults', b=1):
		print '   decorated:', (a, b)
		print '   ', f(a, b=b)
		return
	return decorated

def myfunc(a, b=2):
	"""myfunc() is not complicated"""
	print '  myfunc:', (a,b)
	return

 # the raw function
show_details('myfunc', myfunc)
myfunc('unwrapped, default b')
myfunc('unwrapped, passing b', 3)
print

 # wrap explicitly
wrapped_myfunc = simple_decorator(myfunc)
show_details('wrapped_myfunc', wrapped_myfunc)
wrapped_myfunc()
wrapped_myfunc('args to wrapped', 4)
print

 # wrap with decorator syntax
@simple_decorator
def decorated_myfunc(a,b):
	myfunc(a,b)
	return

show_details('decorated_myfunc', decorated_myfunc)
decorated_myfunc()
decorated_myfunc('args to decorated', 4)