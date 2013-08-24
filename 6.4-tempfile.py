## 6.4 tempfile - Temporary File System Objects
# tempfile provides several functions for easily creating secure temporary files
import tempfile, os

## 6.4.1 Temporary Files
# TempFile() creates a file and, if possible, unlinks it immediately
# This makes it impossible for another application to find or use
print "Building a filename with PID:"
filename = '/tmp/guess_my_name.%s.txt' % os.getpid()
temp = open(filename, 'w+b')
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
finally:
        temp.close()
        os.remove(filename)

print "\nTemporaryFile:"
temp = tempfile.TemporaryFile() 
try:
    print 'temp:', temp
    print 'temp.name:', temp.name
    print
finally:
    temp.close()

# mode is 'w+b' by default
with tempfile.TemporaryFile() as temp:
    temp.write('Some data:')
    temp.seek(0)
    print temp.read()
    
# mode can be set to 'w+t' for text mode
with tempfile.TemporaryFile() as f:
    f.writelines(['first\n', 'second\n'])
    f.seek(0)
    for line in f:
        print line.rstrip()
        
## 6.4.2 Named Files
# Using a named linked file allows for the file to be shared across processes

print "\nTemporaryFile:"
with tempfile.NamedTemporaryFile() as temp:
    print 'temp:', temp
    print 'temp.name:', temp.name
    print
print 'Exists after close:', os.path.exists(temp.name)
print

## 6.4.3 Temporary Directories
# sometimes it's nice to organize things
directory_name = tempfile.mkdtemp()
print directory_name
os.removedirs(directory_name)

## 6.4.4 Predicting Names
# temp files are made up of dir + prefix + random + suffix; everythign but random can be specified

with tempfile.NamedTemporaryFile(suffix='_suffix', prefix='prefix_', dir='/tmp') as temp:
    print 'temp:', temp
    print 'temp.name:', temp.name
    print 
    
## 6.4.5 Temporary File Location
print 'gettempdir():', tempfile.gettempdir()
print 'gettempprefix():', tempfile.gettempprefix()

tempfile.tempdir = '/i/changed/this/path'
print 'gettempdir():', tempfile.gettempdir()