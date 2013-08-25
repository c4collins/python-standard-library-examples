## 6.10 dircache - Cache Directory Listings
# dircache reads directory listings form the file system and holds them in memory
import dircache, os, pprint

## 6.10.1 Listing Directory Contents
# dircache.listdir() is a wrapper around os.listdir()
# dircaqche.listdir() will return the same list object, unless the mdate changes
# This list should not be modified in place

path = os.curdir
first = dircache.listdir(path)
second = dircache.listdir(path)

print 'Contents :'
for name in first:
    print '\t', name
print

print 'Identical:', first is second
print 'Equal    :', first == second
print

# if the contents of the directory change it's rescanned
path = '/tmp'
file_to_create = os.path.join(path, '6.10-dircache_temp.txt')

# take a sample
first = dircache.listdir(path)
# create a file to muck with the directory
open(file_to_create, 'w').close()
second = dircache.listdir(path)
# remove the file
os.unlink(file_to_create)

print 'Identical :', first is second
print 'Equal     :', first == second
print 'Difference:', list( set(second) - set(first) )
print

# it's also possible to force a reset of the entire cache.

first = dircache.listdir(os.curdir)
dircache.reset()
second = dircache.listdir(os.curdir)

print 'Identical :', first is second
print 'Equal     :', first == second
print 'Difference:', list( set(second) - set(first) )
print

## 6.10.2 Annotated Listings
# annotate() modifies a list by adding '/' to the ends of directory names
path = os.pardir + os.sep #+ os.pardir + os.sep # '../../'
contents = dircache.listdir(path)
annotated = contents[:]
dircache.annotate(path, annotated)

fmt = '%25s\t%25s'
print fmt % ('ORIGINAL', 'ANNOTATED')
print fmt % (('-' * 25,) * 2)
for o, a in zip(contents, annotated):
    print fmt % (o, a)