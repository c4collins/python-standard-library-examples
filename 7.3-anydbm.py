## 7.3 anydbm
# anydbm is a front-end for DBM-style (non-relational) databases that use simple strings as key values to access records containing strings.
# It uses whichdb to identify databases and opens them with an appropriate module
# It uses dbm in Python3 because whichdb was put into dbm
# It is used as a back-end for shelve, which stores items in a DBM using pickle
import anydbm, whichdb
from contextlib import closing

## 7.3.1 Database Types
# any dmb tries these databases, in this order:

# dbhash
# primary back-end for anydbm
# supports the following flags
    # 'r' - read only **DEFAULT**
    # 'w' - read/write
    # 'c' - read/write, creating if necessary
    # 'n' - always create new db, open for read/write

# gdbm
# updated version of the GNU dbm.
# supports additional flags:
    # 'f' - fast (unsynchronized writes)
    # 's' - synchronized (changes are written to file as they're made, rather than when the db is closed)
    # 'u' - open the db unlocked

# dbm
# Provides an interface to one of several C implementations of the dbm format.

# dumbdbm
# Provides a fallback implementation of the DBM API when no other implementations are available.
# It has no external dependencies, but is the slowest of the lot.

## 7.3.2 Creating a New Database
# the open function takes flags to control how the db file is managed
# using the 'n' flag ensures this db gets reset every time this file is run
db = anydbm.open('data/7.3-dbm_type.db', 'n') 
db['key']    = 'value'
db['today']  = 'Monday'
db['author'] = 'Connor'
db.close()

print 'whichdb?:', whichdb.whichdb('data/7.3-dbm_type.db')
print

## 7.3.3 Opening an Existing Database
# Opening a dbm db is much like opening a file
with closing( anydbm.open('data/7.3-dbm_type.db') ) as db:
    print 'keys():', db.keys()
    for k,v in db.iteritems():
        print 'iterating:', k, v
    print 'db["author"] =', db['author']
print

## 7.3.4 Error Cases
# The keys of the db need to be strings
with closing( anydbm.open('data/7.3-dbm_type.db', 'w') ) as db:
    try:
        db[1] = 'one'
    except TypeError, err:
        print '%s: %s' % (err.__class__.__name__, err)
print

# Values must be string or none
with closing( anydbm.open('data/7.3-dbm_type.db', 'w') ) as db:
    try:
        db['one'] = 1
    except TypeError, err:
        print '%s: %s' % (err.__class__.__name__, err)
print