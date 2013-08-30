## 8.4 tarfile
# The tarfile module provide read/write access to UNIX tar archives, including compressed files
import tarfile, time, os, shutil
from contextlib import closing
try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

## 8.4.1 Testing Tar Files
# is_tarfile() returns a Boolean indicating whether or not the argument represents a valid tarfile
filenames = [ 
    'data/lorem.txt', 
    'data/8.4-tarfile_example.tar',
    'data/8.4-tarfile_bad-example.tar',
    'data/8.4-tarfile_does-not-exist',
]
for filename in filenames:
    try:
        print '%35s %s' % ( filename, tarfile.is_tarfile( filename ) )
    except IOError, err:
        print '%35s %s' % ( filename, err )
print

## 8.4.2 Reading Metadata from an Archive
# Use the TarFile class to work directly on a tar archive.
# It supports reading data about files, as well as modifying archives
# use getnames() to read the names of the files in the archive

with closing( tarfile.open( filenames[1], 'r' ) ) as tf:
    for index, name in enumerate(tf.getnames()):
        print 'File%3s:' % index, name
        
    # In addition to names, metadata is available as instances of TarInfo objects
    fmt = "\t{:8}:\t{}"
    for member_info in tf.getmembers():
        print member_info.name
        print fmt.format( "Modified", time.ctime( member_info.mtime ) )
        print fmt.format( "Mode", oct( member_info.mode ) )
        print fmt.format( "Type", member_info.type )
        print fmt.format( "Size", member_info.size ), "bytes"
        print
        
    # Or, if the name is known in advance, it can be asked for directly
    print "Single lookup:"
    for filename in filenames:
        try:
            member_info = tf.getmember( filename )
            print member_info.name
            print fmt.format( "Modified", time.ctime( member_info.mtime ) )
            print fmt.format( "Mode", oct( member_info.mode ) )
            print fmt.format( "Type", member_info.type )
            print fmt.format( "Size", member_info.size ), "bytes"
            print
        except KeyError, err:
            print "File Not Found:", err
    print

## 8.4.3 Extracting Files from an Archive
    # Use extractfile() to access the data from an archived file, passing in the filename
    for filename in filenames:
        if not filename.endswith('.tar'):
            try:
                # this returns a file-like object that contains the archived file's contents
                f = tf.extractfile( filename )
            except KeyError, err:
                print "File not found:", err
            else:
                print "Extracting contents of %s: (first 200 chars)" % filename
                print  f.read(200)
                print
    print

    # To unpack the archive and write the files to the file system use extract() or extractall() instead
    outdir = 'data/8.4-tarfile'
    # Delete the folder and recreate it so it's clean each time
    shutil.rmtree( outdir )
    if not os.path.exists( outdir ):
        os.mkdir( outdir )
    tf.extract( filenames[0], 'data/8.4-tarfile' )
    print "After extract():"
    print os.listdir( outdir )
    print
    
    # extractall() is safer, and should be used whenever possible over extract()
    # the first arguement is the directory everything should be extracted into.
    tf.extractall( outdir )
    print "After extractall():"
    print os.listdir( outdir )
    print
    
    # It is possible to extract specific files with extractall()
    # just pass the name or TarInfo metadata container to it
    shutil.rmtree( outdir )
    if not os.path.exists( outdir ):
        os.mkdir( outdir )
    
    tf.extractall( outdir, members=[ tf.getmember( 'data/lorem.txt' ) ] )
    print "After extractall('data/lorem.txt'):"
    print os.listdir( outdir  )
    print
    
## 8.4.4 Creating New Archives
# To create a new archive, open the TarFile with a mode of 'w' (like every other file-like)
print "Creating archive"
with closing( tarfile.open( filenames[1], 'w') ) as out:
    print "Adding data/"
    for file in os.listdir( 'data/' ):
## 8.4.5 Using Alternative Archive Member Names        
        # you can change the filename to something more useful by passing in an archive name (as arcname)
        # Might be hard to notice: the input is 'data/filename' and the arcname is 'filename'
        out.add( 'data/' + file, arcname=file )

## 8.4.6 Writing Data from Sources Other than Files
# Sometimes it's nice to not have to write files to add them to tar archives
# for this, there is addfile() to add date from a file-like handle.
data = "This is the data to write to the archive."

with closing( tarfile.open( 'data/8.4-tarfile_addfile-string.tar', 'w' ) )as out:
    info = tarfile.TarInfo( 'made-up-file.txt' )
    info.size = len( data )
    out.addfile( info, StringIO(data) )
    
## 8.4.7 Appending to Archives
# Use the 'a' flag when opening the archive to append to, rather than truncate, it
with closing( tarfile.open( 'data/8.4-tarfile_addfile-string.tar', 'a' ) )as out:
    info = tarfile.TarInfo( 'other-made-up-file.txt' )
    info.size = len( data )
    out.add( 'data/lorem.txt' )
print

print 'Contents:'
with closing( tarfile.open( 'data/8.4-tarfile_addfile-string.tar', 'r' ) ) as tf:
    for member_info in tf.getmembers():
        print member_info.name
        f = tf.extractfile(member_info)
        print f.read()
        print
        
## 8.4.8 Working with Compressed Archives
# Besides regular tar files, tarfile can work with compressed gzip or bz2 files
# To open a compressed archive, add :gz or :bz2 to the mode string passed when opening the file
fmt = "{:5}  {:38}  {:10}"
fmt_filler = "{:-^5}  {:-^38s}  {:-^10s}"
print fmt.format( 'MODE', 'FILENAME', 'SIZE' )
print fmt_filler.format("", "", "")

for filename, write_mode in [
    ('data/8.4-tarfile_compression.tar', 'w'),
    ('data/8.4-tarfile_compression.tar.bz', 'w:gz'),
    ('data/8.4-tarfile_compression.tar.gz', 'w:bz2'),    
    ('data/8.4-tarfile_compression.tar', 'a'),
    ('data/8.4-tarfile_compression.tar.bz', 'a:gz'),
    ('data/8.4-tarfile_compression.tar.gz', 'a:bz2'),
]:
    err_bool = False
    try:
        out = tarfile.open(filename, mode=write_mode)
    except ValueError, err:
        print fmt.format( write_mode, filename, err)
        print err
        continue
        
    try:
        out.add('data/lorem.txt')
    finally:
        out.close()
   
    print fmt.format( write_mode, filename, os.stat(filename).st_size),
    print [m.name for m in tarfile.open( filename, 'r:*').getmembers() ]
    # only for reading files: using mode='r:*' tarfile will determine the compression method automatically
