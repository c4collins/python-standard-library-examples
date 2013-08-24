## 6.5 Shutil
# The shutil module covers high-level file operations like copying and setting permissions

import shutil, os, sys, time, commands
from glob import glob
from StringIO import StringIO

## 6.5.1 Copying Files
# copyfile() copies the contents of the surce to the destination
# raises IOError if it doesn't have write permissions
print 'BEFORE:', glob('6.5-shutil.*')
shutil.copyfile('6.5-shutil.py', '6.5-shutil.copy.py')
print 'AFTER:', glob('6.5-shutil.*')
print

# Special files (such as UNIX device nodes) aren't copyable with copyfile()
# Because copyfile() opens the input file for reading

# copyfileobject(input, output[, bufferlength]) accepts open file handles instead of filenames
class VerboseStringIO(StringIO):
    def read(self, n=-1):
        next = StringIO.read(self, n)
        print 'read(%d) bytes' % n
        return next

lorem_ipsum = """Lorem ipsum dolor sit amet, novum nemore mel ex, ei eos posse inciderint, docendi tibique sed at. Sumo eruditi eam ut. Prima utamur argumentum duo in, pri cibo erat dolores te. Qui principes intellegat complectitur ea. Delectus percipitur ex est, his malorum epicuri et, tota deserunt vim eu. Sed ea justo saepe vidisse. Cum facer inimicus te, eu vim wisi semper aliquip, aeque numquam ei pro.
Ex nostrud ancillae nominavi nec, duo ea nominati dignissim deterruisset. Ceteros contentiones te his. Has repudiandae dissentiunt cu. Mel eligendi scribentur id, quo oblique mentitum patrioque cu."""

print 'Default:'
input = VerboseStringIO(lorem_ipsum)
output = StringIO()
shutil.copyfileobj(input, output)
print

print 'All at once:'
input = VerboseStringIO(lorem_ipsum)
output = StringIO()
shutil.copyfileobj(input, output, -1)
print

print '256 bytes:'
input = VerboseStringIO(lorem_ipsum)
output = StringIO()
shutil.copyfileobj(input, output, 256)
print

# the copy() function interprets commands the same as UNIX cp
# that is, if you supply the output as a directory, you'll get a file with th same name as input in that directory.
print 'BEFORE:', os.listdir('data')
shutil.copy('6.5-shutil.copy.py', 'data')
print 'AFTER:', os.listdir('data')
print

# copy2() works the same as copy, but copies access and modification times as well.
def show_file_info(filename):
    stat_info = os.stat(filename)
    print '\tMode     :', stat_info.st_mode
    print '\tCreated  :', time.ctime(stat_info.st_ctime)
    print '\tAccessed :', time.ctime(stat_info.st_atime)
    print '\tModified :', time.ctime(stat_info.st_mtime)
    
print 'Source      :'
show_file_info('6.5-shutil.copy.py')
shutil.copy2('6.5-shutil.copy.py', 'data')
print 'Destination :'
show_file_info('data/6.5-shutil.copy.py')
print
    
## 6.5.2 Copying File Metadata
# importing commands... wooooooooooo
# to copy file permissions from one file to another, use copymode()
with open('data/6.5-shutil.copy.py', 'wt') as f:
    f.write('These are the new contents of this file.')
os.chmod('data/6.5-shutil.copy.py', 0444)
print 'BEFORE:'
print commands.getstatus('data/6.5-shutil.copy.py')
shutil.copymode('6.5-shutil.copy.py', 'data/6.5-shutil.copy.py')
print 'AFTER :'
print commands.getstatus('data/6.5-shutil.copy.py')
print

# copying other metadata can be done with copystat()
with open('data/6.5-shutil.copy.py', 'wt') as f:
    f.write('These are the new contents of this file.')
os.chmod('data/6.5-shutil.copy.py', 0444)
print 'BEFORE:'
show_file_info('data/6.5-shutil.copy.py')
shutil.copystat('6.5-shutil.copy.py', 'data/6.5-shutil.copy.py')
print 'AFTER :'
show_file_info('data/6.5-shutil.copy.py')
print

## 6.5.3 Working with Directory Trees
# shutil has 3 functions for working with directory trees

# To copy a directory from one place to another, use copytree()
print 'BEFORE:'
print commands.getoutput('ls -rlast /tmp/data')
shutil.copytree('data/', '/tmp/data')
print 'AFTER :'
print commands.getoutput('ls -rlast /tmp/data')
print

# To move a directory or file from one place to another, use move()
print 'BEFORE:', glob('/tmp/*')
shutil.move('/tmp/data', '/tmp/moved_data')
print 'AFTER :', glob('/tmp/*')
print

# To remove a directory and its contents, use rmtree()
print 'BEFORE:'
print commands.getoutput('ls -rlast /tmp/moved_data')
shutil.rmtree('/tmp/moved_data')
print 'AFTER :'
print commands.getoutput('ls -rlast /tmp/moved_data')
print

# just checking
print '/tmp  :'
print glob('/tmp/*')
print

