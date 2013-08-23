## 6.2 glob - Filename Pattern Matching
# pattern rules for glob are not the same as re, instead they follow UNIX path rules
import glob, os.path, os, logging, time
# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


## 6.2.1 Example Data
# create directories for testing glob
if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('data/6.2'):
    os.mkdir('data/6.2')
if not os.path.exists('data/6.2/subdir'):
    os.mkdir('data/6.2/subdir')
    
# create files for testing glob
os.chdir('data/6.2/')
logger.debug( "Current directory is now: %r" % os.path.abspath(os.curdir) )

with open('file1.txt', 'wt') as f:
    f.write("File 1")
with open('file2.txt', 'wt') as f:
    f.write("This is File 2")
with open('filea.txt', 'wt') as f:
    f.write("File A is Here")
with open('fileb.txt', 'wt') as f:
    f.write("Nothing quite like File B")
with open('subdir/subfile.txt', 'wt') as f:
    f.write("This file is a submarine sandwich.")

os.chdir('../../') # change back to main dir

logger.debug( "Current directory is now: %r" % os.path.abspath(os.curdir) )

## 6.2.2 Wildcards
# * matches 0 or more characters in a name segment
print "\nEverything:"
for name in glob.glob('data/6.2/*'):
    print name
   
print "\nNamed Explicitly:"
for name in glob.glob('data/6.2/subdir/*'):
    print name
 
print "\nUsing Wildcard:"
for name in glob.glob('data/6.2/*/*'):
    print name
    
## 6.2.3 Single Character Wildcard
# ? matches any single character
print "\nQuestion Mark:"
for name in glob.glob('data/6.2/file?.txt'):
    print name
    
## 6.2.4 Character Ranges
# [a-z] instead of a question mark will match one of several characters
print "\nDigits Before Extension:"
for name in glob.glob('data/6.2/*[0-9].txt'):
    print name
    
print "\nLetters Before Extension:"
for name in glob.glob('data/6.2/*[a-z].txt'):
    print name
    
print "\n1 or a Before Extension:"
for name in glob.glob('data/6.2/*[a1].txt'):
    print name