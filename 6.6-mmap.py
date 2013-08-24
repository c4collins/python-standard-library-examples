## 6.6 mmap - Memory-Map Files
# There are differences in mmap() for Windows vs. *NIX systems
import mmap, contextlib, shutil, re

## 6.6.1 Reading
# mmap( file_descriptor, byte_size[, access] )
# file_descriptor needs to be opened before and closed after mmap()
# byte_size of the portion of the file to map.
    # giving a byte_size larger than the fle will extend the file
    # giving a byte_size of 0 will return either the whole file (*nix) or nothing (Win)
# access is supported by both platforms
    # ACCESS_READ for read-only access
    # ACCESS_WRITE for write-through access (assignments to memory go to file)
    # ACCESS_COPY for copy-on-write (assignments in memory are not written to file)
    
with open('data/lorem.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        b = 10 #bytes
        print 'First %d bytes via read  :' % b, m.read(b)
        print 'First %d bytes via slice :' % b, m[:b]
        print 'Second %d bytes via read :' % b, m.read(b)
print

## 6.6.2 Writing

# copy the data file
shutil.copyfile('data/6.6-lorem.txt', 'data/6.6-lorem.copy.txt')

word = 'novum'
reversed = word[::-1]
print 'Looking for    :', word
print 'Replacing with :', reversed

with open('data/6.6-lorem.copy.txt', 'r+') as f:
    with contextlib.closing(mmap.mmap(f.fileno(),0)) as m:
        # check
        print 'Before:'
        print m.readline().rstrip()
        # rewind
        m.seek(0)
        # replace
        loc = m.find(word)
        m[loc:loc+len(word)] = reversed
        m.flush()
        # rewind
        m.seek(0)
        # recheck
        print 'After :'
        print m.readline().rstrip()
        # rewind
        f.seek(0)
        print 'File  :'
        print f.readline().strip()
print

# using ACCESS_COPY doesn't change the file
word = 'muvon'
reversed = word[::-1]
print 'Looking for    :', word
print 'Replacing with :', reversed
with open('data/6.6-lorem.copy.txt', 'r+') as f:
    with contextlib.closing(mmap.mmap(f.fileno(),0, access=mmap.ACCESS_COPY)) as m:
        # check
        print 'Before:'
        print m.readline().rstrip()
        # rewind
        m.seek(0)
        # replace
        loc = m.find(word)
        m[loc:loc+len(word)] = reversed
        m.flush()
        # rewind
        m.seek(0)
        # recheck
        print 'After :'
        print m.readline().rstrip() 
        # rewind
        f.seek(0)
        print 'File  :'
        print f.readline().strip() 
print

## 6.6.3 Regular Expressions
# since a memory-mapped file can act like a string, it can be used all sorts of crazy ways with other modules that act on strings like re

pattern = re.compile(r'(\.\W+)?([^.]?dolor[^.]*?\.)', 
                re.DOTALL | re.IGNORECASE | re.MULTILINE)
with open('data/6.6-lorem.txt', 'r') as f:
    with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        for match in pattern.findall(m):
            print match[1].replace('\n', ' ')