## 8.5 zipfile - ZIP Archive Access
# The zipfile module can be used to manipulate ZIP archive files
import zipfile, time, datetime, itertools, binascii, sys
from contextlib import closing
try:
    import zlib
    zip_compression = zipfile.ZIP_DEFLATED
except:
    zip_compression = zipfile.ZIP_STORED

## 8.5.1 Testing ZIP Files
# Use is_zipfile() to return a Boolean indicating if it is or not
filenames = [ 
    'data/lorem.txt', 
    'data/8.5-zipfile_example.zip',
    'data/8.5-zipfile_bad-example.zip',
    'data/8.5-zipfile_does-not-exist',
]

for filename in filenames:
    print '%35s %s' % ( filename, zipfile.is_zipfile( filename ) )
print

## 8.5.2 Reading Metadata from an Archive
# use the ZipFile class to work directly on a ZIP file
# namelist() returns the names of the files in the archive
with closing( zipfile.ZipFile( filenames[1] , 'r') ) as zf:
    print zf.namelist()
print
    
# to access the rest of the metadata, use infolist() or getinfo()
def print_info(archive_name):
    fmt = "\t{:12} : {}"
    with closing( zipfile.ZipFile( archive_name ) ) as zf:
        for info in zf.infolist():
            if info.create_system == 0:
                system = 'Windows'
            elif info.create_system == 3:
                system = 'Unix'
            else:
                system = 'UNKNOWN'
        
            print info.filename
            print fmt.format( "Comment", info.comment )
            print fmt.format( "Modified", datetime.datetime(*info.date_time) )
            print fmt.format( "System", system )
            print fmt.format( "ZIP version", info.create_version )
            print fmt.format( "Compressed", info.compress_size ), "bytes"
            print fmt.format( "Uncompressed", info.file_size ), "bytes"
            print
        
print_info( filenames[1] )

# If the name of the archive member is known in advance, it can be selected directly.
with closing( zipfile.ZipFile( filenames[1], 'r' ) ) as zf:
    archive_filenames = list( itertools.chain( 
        [info.filename for info in zf.infolist()[ :len(zf.infolist()) /2 ]],
        ['data/8.3-bzip_compress-level-10.bz2',]
    ))
    for filename in archive_filenames:
        try:
            info = zf.getinfo( filename )
        except KeyError:
            print "ERROR: Did not find %s in zip file" % filename
        else:
            print '%s is %d bytes' % ( info.filename, info.file_size )
    print

## 8.5.3 Extracting Archived Files from an Archive
# To access the data from an archive member, use the read() method, passing the name
    for filename in archive_filenames:
        try:
            data = zf.read( filename )
        except KeyError:
            print "ERROR: Did not find %s in zip file" % filename
        else:
            print filename, ': (sample)'
            print binascii.hexlify(data)[:79]
    print
    
## 8.5.4 Creating New Archives
# Creating a new archive is as simple as opening a file with mode='w'

print "Creating archive:"
with closing( zipfile.ZipFile( archive_filenames[0], mode='w' ) ) as zf:
    print "adding data/lorem.txt"
    zf.write( 'data/lorem.txt' )
    
print 
print_info( archive_filenames[0] )

# To add compression, the zlib module is required
# if zlib is available, the sompression mode for a file or the archive can be set with
# zipfile.ZIP_DEFLATED
# The default compression mode is zipfile.ZIP_STORED, which doesn't compress archived data
modes = { 
    zipfile.ZIP_DEFLATED: 'deflated',
    zipfile.ZIP_STORED  : 'stored',
}

print "Creating archive:"
with closing( zipfile.ZipFile( archive_filenames[0], mode='w' ) ) as zf:
    mode = modes[zip_compression]
    print "adding 'data/lorem.txt' with compression mode", mode
    
## 8.5.5 Using Alternative Archive Member Names
    # add an arcname= value to write() to change the name of the file stored
    zf.write( 'data/lorem.txt', arcname='ipsum.txt', compress_type=zip_compression )
print
print_info( archive_filenames[0] )
print

## 8.5.6 Writing Data from Source Other than Files
# Rather than writing data to file and then adding that file to the ZIP archive
# Insert the data directly into the archive from memory with writestr()
msg = "This data did not exist in a file"
with closing( zipfile.ZipFile( filenames[1], mode='w', compression=zip_compression ) ) as zf:
    zf.writestr('from-string10.txt', msg * 10)
    zf.writestr('from-string100.txt', msg * 100)
    zf.writestr('from-string1000.txt', msg * 1000)
print_info( filenames[1] )

with closing( zipfile.ZipFile( filenames[1], 'r' ) ) as zf:
    print zf.read( 'from-string10.txt' )
print

## 8.5.7 Writing with a ZipInfo Instance
# Normally the modification date is computed when the file or string is added to the archive
# A ZipInfo instance can be passed to writestr() to define the modification date and other metadata
## 8.5.8 Appending to Files
# using the mode='a' flag adds to the file instead of truncating it
with closing( zipfile.ZipFile( filenames[1], mode='a') ) as zf:
    info = zipfile.ZipInfo( 'lorem.txt', date_time = time.localtime( (time.time() ) )[:6] )
    info.compress_type = zip_compression
    info.comment = "Remarks go here."
    info.create_system=0
    zf.writestr(info, msg)
print_info( filenames[1] )

## 8.5.9 Python ZIP Archives
# Python can import modules from inside aip archives using zipimport, if those archives appear in sys.path
# The PyZipFile class can be used to construct a module suitable for use this way.
# The extra method writepy() tells PyZipFile to scan a directory for .py files and add the corresponding .po or .pyc to the archive
# If neither compiled form exists, a .pyc is created and added.

with closing( zipfile.PyZipFile( 'data/8.5-zipfile_pyzipfile.zip', mode='w' ) ) as zf:
    zf.debug = 3
    print "Adding python files"
    zf.writepy('.')
    for name in zf.namelist():
        print name
        
    print
    sys.path.insert(0, 'data/8.5-zipfile_pyzipfile.zip')
    
import zipfile_print_info
print 'Imported from:', zipfile_print_info.__file__
print

#zipfile_print_info.print_info('data/8.5-zipfile_pyzipfile.zip')

## 8.5.10 Limitations
# zipfile will not work on ZIP files with appended comments, or multidisk archives
# It also does not support files >4GB that use the ZIP64 extension