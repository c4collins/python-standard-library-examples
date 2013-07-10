## hashlib
 # hashlib is the core of Python cryptography, and includes many popular encryption algorithms

import hashlib, sys, random

lorem = '''Lorem ipsum dolor sit amet, consectetur adispisicing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit ease cillum dolore eu fugiat nulla
pariatur. Exceptur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.'''


 # MD5 - crete the hash object, add the data, then call digest() or hexdigest()

h = hashlib.md5()
h.update(lorem)
print 'MD5 :', h.hexdigest()

 # SHA1 - crete the hash object, add the data, then call digest() or hexdigest()

h = hashlib.sha1()
h.update(lorem)
print 'SHA1:', h.hexdigest()

 # sometimes it's easier to call the hash by name
try:
    hash_name = sys.argv[1]
except IndexError:
    print "Whoops, you didn't enter a hash type.  I'm gonna choose one for you."
    types = ['sha1', 'sha256', 'sha512', 'md5']
    hash_name = random.choice(types)
finally:
    print "Hash type:", hash_name
    h = hashlib.new(hash_name)
    h.update(lorem)
    all_at_once = h.hexdigest()
    print 'All at once :', all_at_once

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


