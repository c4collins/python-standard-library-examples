## weakref!
 # Weak references to objects allow the object to be destroyed by garbage collection
 # This allows for circular references and object caches to be dealt with more effectively

 # the most basic weakref is ref()
import weakref

class ExpensiveObject(object):
    def __del__(self):
        print '(Deleting %s)' % self

obj = ExpensiveObject()
r = weakref.ref(obj)

print 'Simple ref:'
print 'obj:', obj
print 'ref:', r
print 'r():', r()
del obj
print 'r():', r()
print

 # the ref constructor takes an optional callback function to invoke when the object is deleted
def callback(reference):
    print 'callback(', reference, ')'
    
obj = ExpensiveObject()
r = weakref.ref(obj, callback)

print 'With a callback:'
print 'obj:', obj
print 'ref:', r
print 'r():', r()
del obj
print 'r():', r()
print

 # sometimes it's more convenient to use a proxy, because they can be used as if they were the original object

class QueryObject(ExpensiveObject):
    def __init__(self, name):
            self.name =  name

obj = QueryObject('My Object')
r = weakref.ref(obj)
p = weakref.proxy(obj)
print 'Proxy:'
print 'via obj:', obj.name
print 'via ref:', r().name
print 'via proxy:', p.name
del obj
try:
    print 'via proxy:', p.name
except ReferenceError: # the prog must go on
    print "sorry, it's gone."
