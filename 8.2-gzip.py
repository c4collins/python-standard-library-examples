## 8.2 gzip - Read and Write GNU Zip Files
# the gzip module provides a file-like interface to GNU zip files, uzing zlib to de/compress
import gzip, os, hashlib, itertools, binascii
from contextlib import closing
try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

## 8.2.1 Writing Compressed Files
outfilename = 'data/8.2-gzip_example.txt.gz'

with closing( gzip.open( outfilename, 'wb') ) as output:
    output.write( 'Contents of the example file go here.\n' )
    
print outfilename, 'contains', os.stat(outfilename).st_size, 'bytes'
os.system('file -b --mime %s' % outfilename)
print

# Different amounts of compression can be used by passing a compresslevel argument
# Valid values range from 1-9, lower values are faster and result in less compression
# Higher values are slower and, in general, compress more
def get_hash(data):
    return hashlib.md5(data).hexdigest()
    
data = open( 'data/lorem.txt', 'r').read() * 1024
cksum = get_hash(data)

fmt = "{:5} {:10} {:35}"
print fmt.format( "Level", "Size", "Checksum" )
print fmt.format( "-"*5, "-"*10, "-"*35 )
print fmt.format( "data", len(data), cksum )

for i in xrange(1, 10):
    filename = 'data/8.2-gzip_compress-level-%s.gz' % i
    with gzip.open( filename, 'wb', compresslevel=i ) as output:
        output.write(data)
    size = os.stat(filename).st_size
    cksum = get_hash( open( filename, 'rb').read() )
    print fmt.format( i, size, cksum )
print

# A GzipFile instance includes a writelines() method that can write a sequence of strings
uncompressed_data = "The same line, over and over.\n"
with gzip.open( 'data/8.2-gzip_example-lines.txt.gz', 'wb', compresslevel=4 ) as output:
        output.writelines(
            itertools.repeat( uncompressed_data, 20 )
        )

## 8.2.2 Reading Compressed Data
# When reading back from compressed datafiles it's important to remember the 'b' binary flag on the file
with closing( gzip.open( 'data/8.2-gzip_example-lines.txt.gz', 'rb') ) as input_file:
    print input_file.read()

# It's also possible to seek and read only part of the data
with closing( gzip.open( 'data/8.2-gzip_example.txt.gz', 'rb') ) as input_file:
    print "Entire file:"
    all_data = input_file.read()
    print all_data
    
    expected = all_data[5:15]
    
    # Rewind to beginning
    input_file.seek(1)
    # Move ahead 5 bytes
    input_file.seek(5)
    print "Starting at position 5 for 10 bytes"
    partial = input_file.read(10)
    print partial
    
    print expected == partial
    print
    
## 8.2.3 Working with Streams
# THe GzipFile class can be used to wrap other types of data streams so they can be compressed as well
# this is useful when the data is being transmitted over a socket or to an existing (already open) file handle
# a StringIO buffer can also be used
uncompressed_data = uncompressed_data * 10
print 'UNCOMPRESSED:', len(uncompressed_data)
print uncompressed_data

buffer = StringIO()
with closing( gzip.GzipFile( mode='wb', fileobj=buffer ) ) as f:
    f.write(uncompressed_data)
    
compressed_data = buffer.getvalue()
print '  COMPRESSED:', len(compressed_data)
print binascii.hexlify( compressed_data )

inbuffer = StringIO(compressed_data)
with closing( gzip.GzipFile( mode='rb', fileobj=inbuffer ) ) as f:
    reread_data = f.read( len(uncompressed_data) )
print

print '     REREAD:', len(reread_data)
print reread_data
