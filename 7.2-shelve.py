## 7.2 shelve - Persistent Storage of Objects
# the shelve module is a simple storage option when a rdb is not needed
# the shelf is accessed with keys, like a dictionary
# the values are pickled and written to a database created and managed by anydbm
import shelve, contextlib

## 7.2.1 Creating a New Shelf
# use the DbfilenameShelf class directly, or use shelve.open()
with contextlib.closing( shelve.open( 'data/7.2-test_shelf.db') ) as s:
    s['key1'] = { 'int':10, 'float':9.5, 'string':"sample data" }
    
# then you can open the shelf and access the data like it was a dictionary
# flag='r' forces readonly mode, it isn't necessary, but it's a good idea
with contextlib.closing( shelve.open( 'data/7.2-test_shelf.db', flag='r') ) as s:
    existing = s['key1']

for key in existing:
    print key, ':', existing[key]
print
    
## 7.2.2 Writeback
# Objects are not automatically updated on the shelf when their state is changed
# unless writeback is set to True
print 'Without writeback=True:'
with contextlib.closing( shelve.open(  'data/7.2-test_shelf.db') ) as s:
    original = s['key1'].copy()
    print 'ORIGINAL   :', original
    print 'adding new item...'
    s['key1']['new_value'] = 'this was not here before'
    print 'MODIFIED   :', s['key1']
with contextlib.closing( shelve.open(  'data/7.2-test_shelf.db') ) as s:
    print 'NEW        :', s['key1']
    print 'WRITEBACK  :', original != s['key1']
print

print 'With writeback=True:'
with contextlib.closing( shelve.open(  'data/7.2-test_shelf.db', writeback=True) ) as s:
    original = s['key1'].copy()
    print 'ORIGINAL   :', original
    print 'adding new item...'
    s['key1']['new_value'] = 'this was not here before'
    print 'MODIFIED   :', s['key1']
with contextlib.closing( shelve.open(  'data/7.1-test_shelf.db') ) as s:
    print 'NEW        :', s['key1']
    print 'WRITEBACK  :', original != s['key1']
print
# obviously, writeback is a nice feature, but it also creates extra memory overhead.

## 7.2.3 Specific Shelf Types
# Using shelve.open() uses a database selected automatically, 
# but when the db format is important, it's possible to use
# DbfilenameShelf and BsdDbShelf directly, or subclass Shelf itself for a custom solution.