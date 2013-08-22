## Chapter 6, the file system
# compose filename and paths using os.path
# list directory contents with listdir(), or glob
# filename pattern matching can be used by fnmatch
# dircache pscans and processes contents of file directories
# os.stat() provides file characteristics
# linecache allows for random (by line number) access to file contents
# tempfile manages temporary files
# shutil provides common shell file utilities (cp, chmod, etc.)
# filecmp compares files and directories at a byte-level
# file class is used to read and write files on the local system,
# using mmap() rather than read() or write() can bypass a few steps in copying file objects
# the codecs module handles encoding and decoding of non-ASCII files so they can be used without modification
# StringIO provides an in-memory stream object that behaves like a file, but doesn't reside on disk

## 6.1 os.path
# os.path allows for reliable filename parsing across platforms
import os, os.path, time, pprint

## 6.1.1 Parsing Paths
print 'os.sep               :', os.sep
print 'os.extsep            :', os.extsep
print 'os.pardir            :', os.pardir
print 'os.curdir            :', os.curdir

TEST_PATHS = [ '/one/two/three',
               '/one/two/three/',
               '/',
               '.',
               '',
             ]
               
for path in TEST_PATHS:
    print '%15s split: %s' % ( path, os.path.split(path) )
    print '%15s  base: %s' % ( path, os.path.basename(path) )
    print '%15s   dir: %s' % ( path, os.path.dirname(path) )

TEST_FILES = [ 'filename.txt',
               'filename',
               '/path/to/filename.txt',
               '/',
               '.',
               'my-archive.tar.gz',
               'no-extension.',
             ]
for path in TEST_FILES:
    print '%21s:' % path, os.path.splitext(path)
print
    
MATCH_PATHS = [ '/one/two/three/four',
                '/one/two/threefold',
                '/one/two/three/',
              ]
for path in MATCH_PATHS:
    print 'PATH  :', path
print 'PREFIX:', os.path.commonprefix(MATCH_PATHS)
print

## 6.1.2 Building Paths
for parts in [ 
    ('one', 'two', 'three'),
    ('/', 'one', 'two', 'three'),
    ('/one', '/two', '/three'),
]:
    print parts, ':', os.path.join(*parts)
print

# expanduser() will find the user's folder if available
for user in [ '', 'connor', 'server', 'bittchinsdb', 'postgresql' ]:
    lookup = '~' + user
    print '%12s : %s' % ( lookup, os.path.expanduser(lookup) )
print
# expandvars() is more general and will expand any environment variables
os.environ['MYVAR'] = 'my/path'
print os.path.expandvars('/path/to/$MYVAR')
print

## 6.1.3 Normalizing Paths
# normpath() cleans up artifacts left from join()
# segments composed of os.pardir and os.curdir are evaluated and collapsed
for path in [
    'one//two//three',
    'one/./two/./three',
    'one/../alt/two/three',
]:
    print '%20s : %s' % (path, os.path.normpath(path))
print

# abspath() convers a relative path to an absolute filename
for path in [
    '.',
    '..',
    './one/two/three',
    '../one/two/three',
]:
    print '%17s : %s' % ( path, os.path.abspath(path) )
print

## 6.1.4 File Times
print 'File         :', __file__
print 'Access time  :', time.ctime(os.path.getatime(__file__))
print 'Modified time:', time.ctime(os.path.getmtime(__file__))
print 'Change time  :', time.ctime(os.path.getctime(__file__))
print 'Size         :', os.path.getsize(__file__), 'bytes'
print

## 6.1.5 Testing Files
# all of these tests return Boolean values
FILENAMES = [
    __file__,
    os.path.dirname(__file__),
    '/',
    './broken_link',
    '/srv/samba/media',
    '/srv/samba/development',
    ]
for file in FILENAMES:
    print '{:^6}:'.format( 'File' ), file
    print '{:-^19}'.format( '' )
    print '{:12}:'.format( 'Absolute' ), os.path.isabs(file)
    print '{:12}:'.format( 'Is File?' ), os.path.isfile(file)
    print '{:12}:'.format( 'Is Dir?' ), os.path.isdir(file)
    print '{:12}:'.format( 'Is Link?' ), os.path.islink(file)
    print '{:12}:'.format( 'Mountpoint?' ), os.path.ismount(file)
    print '{:12}:'.format( 'Exists?' ), os.path.exists(file)
    print '{:12}:'.format( 'Link Exists?' ), os.path.lexists(file)
    print

## 6.1.6 Traversing a Directory Tree
# using os.path.walk()
def visit(arg, dirname, names):
    print dirname, arg
    for name in names:
        subname = os.path.join(dirname, name)
        if os.path.isdir(subname):
            print '  %s/' %name
        else:
            print '  %s' % name
    print

if not os.path.exists('data'):
    os.mkdir('data')
if not os.path.exists('data/6.1.6'):
    os.mkdir('data/6.1.6')

with open('data/6.1.6/file.txt', 'wt') as f:
    f.write('contents')
with open('data/6.1.6.txt', 'wt') as f:
    f.write('contents')
    
os.path.walk('data', visit, '(User data)')
