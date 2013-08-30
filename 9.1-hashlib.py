## 9.1 hashlib - Cryprographic Hashing
 # hashlib is the core of Python cryptography, and includes many popular encryption algorithms

import hashlib, sys, random

## 9.1.1 Sample Data
lorem = open( 'data/lorem.txt', 'r').read()

## 9.1.2 MD5 Example
# MD5 - crete the hash object, add the data, then call digest() or hexdigest()
h = hashlib.md5()
h.update(lorem)
print 'MD5 :', h.hexdigest()

## 9.1.3 SHA1 Example
# SHA1 - crete the hash object, add the data, then call digest() or hexdigest()
h = hashlib.sha1()
h.update(lorem)
print 'SHA1:', h.hexdigest()

## 9.1.4 Creating a Hash by Name
# sometimes it's easier to call the hash by name
try:
    hash_name = sys.argv[1]
except IndexError:
    print "Whoops, you didn't enter a hash type.  I'm gonna choose one for you."
    hash_name = random.choice( hashlib.algorithms )
finally:
    print "Hash type:", hash_name
    h = hashlib.new(hash_name)
    h.update(lorem)
    all_at_once = h.hexdigest()
    print 'All at once :', all_at_once

## 9.1.5 Incremental Updates
# update() can be used to feed in text incrementally
def chunksize(size, text):
    """return parts of the text in size-based increments"""
    start = 0
    while start < len(text):
        chunk = text[start:start+size]
        yield chunk
        start += size
    return

h = hashlib.new(hash_name)
for chunk in chunksize(64, lorem):
    h.update(chunk)
line_by_line = h.hexdigest()

h = hashlib.new(hash_name)
h.update(lorem)
all_at_once = h.hexdigest()

print 'Line by line:', line_by_line
print 'Same        :', (all_at_once == line_by_line)

