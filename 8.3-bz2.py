## 8.2 bz2 Compression
# The bz2 module is an interface for the bzip2 library, used to compress data for storage or transmission
# There are three included APIs:
    # "one shot" de/compression functions for operating on a blob of data
    # iterative de/compression functions for working with a stream of data
    # a file-like class that supports reading and writing line an uncompressed file
import bz2, binascii, os, itertools, sys
import logging, SocketServer, socket, threading
from contextlib import closing
try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

## 8.3.1 One-Shot Operations in Memory
# the simplest way to use bz2 is to load all the data into memory and the use de/compress()
original_data = "This is the original text."
fmt = "{:12}: {}"

# Compress the string
print fmt.format( "Original", str(len(original_data)) + " bytes" )
print fmt.format( "", original_data )
print

# Show the hexlified version of the compressed string
# The compressed string length is half the length of the hex_version
compressed = bz2.compress( original_data ) 
hex_version = binascii.hexlify(compressed)
print fmt.format( "Compressed", str(len(hex_version)) + " bytes (hex)" )
print fmt.format( "Compressed", str(len(compressed)) + " bytes (bin)" )
for i in xrange( (len(hex_version) / 40) +1 ):
    print fmt.format( "", hex_version[ i*40 : (i+1)*40 ] )
print

# Decompress the data back to the original string
decompressed = bz2.decompress(compressed)
print fmt.format( "Decompressed", str(len(decompressed)) + " bytes" )
print fmt.format( "", decompressed)
print

# As with gzip, sometimes the compressed version can be longer than the original.
fmt = "{:9}  {:15} {}"
print fmt.format('len(data)', 'len(compressed)', '<')
print fmt.format('-'*9, '-'*15, '-')

for i in xrange(5):
    data = original_data * i
    compressed = bz2.compress(data)
    print fmt.format( len(data), len(compressed), '*' if len(data) < len(compressed) else '' )
print

## 8.3.2 Incremental Compression and Decompression
# Obviously the in-memory approach is impractical for real-world use cases
# The alternative is to use the BZ2Compressor and BZ2Decompressor objects to manipulate data incrementally

compressor = bz2.BZ2Compressor()
compressed = None
data_file = 'data/lorem.txt'
BLOCK_SIZE = 64

with open( data_file , 'r') as input:
    while True:
        block = input.read( BLOCK_SIZE )
        if not block:
            break
        compressed = compressor.compress(block)
        if compressed:
            print "Compressed:", binascii.hexlify(compressed)
        else:
            print "Buffering..."
        
    remaining = compressor.flush()
    print "Flushed: ", binascii.hexlify(remaining)
print
   
## 8.3.3 Mixed Content Streams
# BZ2Decompressor works with mixed streams of compressed and uncompressed data

lorem = open( data_file , 'r' ).read()
compressed = bz2.compress(lorem)
combined = compressed + lorem

decompressor = bz2.BZ2Decompressor()

# Items decompressable are returned
decompressed = decompressor.decompress(combined)
print 'Decompressed matches lorem:', decompressed == lorem
# Items that were not compressed are left in the unused_data attribute
print 'Unused data matches lorem :', decompressor.unused_data == lorem
print

## 8.3.4 Writing Compressed Files
# BZ2File can be used to write to an d read from bz2-compressed files using the usual methods for reading and writing data
read_write_file = 'data/8.3-bz2_read-write.bz2'
with closing( bz2.BZ2File( read_write_file, 'wb') ) as output:
    output.write( original_data )
    
os.system('file data/8.3-bz2_read-write.bz2')
print

# As with gzip, different compression levels from 1-9 can be provided (as compresslevel)
# Lower values do less work, higher values do more work - results may vary

data = open( 'data/lorem.txt', 'r').read()  * 1024
print "Input contains %d bytes." % len(data)

for i in xrange(1,10):
    filename = 'data/8.3-bzip_compress-level-%s.bz2' % i
    with closing( bz2.BZ2File( filename, 'wb', compresslevel=i) ) as output:
        output.write(data)
    size = os.stat(filename).st_size
    print "For compresslevel %d, the resulting file is %6d bytes" % ( i, size )
    
# A BZ2File instance also has a writelines() method for writing sequences of strings
with closing( bz2.BZ2File( 'data/8.3-bz2_example-lines.bz2', 'wb' ) ) as output:
    output.writelines(
        itertools.repeat( "The same line, over and over.\n", 10 )
    )
print

## 8.3.5 Reading Compressed Files
# When reading back from compressed datafiles it's important to remember the 'b' binary flag on the file
with closing( bz2.BZ2File( 'data/8.3-bz2_example-lines.bz2', 'rb') ) as input_file:
    all_data = input_file.read()
    print all_data
    
# It's also possible to seek and only read portions of a file
    input_file.seek(0)
    
    print 'Expected:', all_data[5:15]
    
    input_file.seek(5)
    sliced_data = input_file.read(10)
    print 'Actual  :', sliced_data
    print all_data[5:15] == sliced_data
print

## 8.3.6 Compressing Network Data
run_server, run_client = False, False

class BZ2RequestHandler( SocketServer.BaseRequestHandler ):
    logger = logging.getLogger('Server')
    
    def handle(self):
        compressor = bz2.BZ2Compressor()
        
        # Find out what the client wants
        filename = self.request.recv(1024)
        self.logger.debug("client asked for '%s'", filename)
        
        # Send chunks of the file as they are compressed
        with open( filename, 'rb') as input:
            while True:
                block = input.read(BLOCK_SIZE)
                if not block:
                    break
                self.logger.debug("RAW '%s'", block)
                compressed = compressor.compress(block)
                if compressed:
                    self.logger.debug("SENDING '%s'", binascii.hexlify(compressed) )
                    s.request.send(compressed)
                else:
                    self.logger.debug("Buffering...")
            
        # Send any data left in the buffer
        remaining = compressor.flush()
        while remaining:
            to_send = remaining[:BLOCK_SIZE]
            remaining = remaining[BLOCK_SIZE:]
            self.logger.debug("FLUSHING '%s'", to_send)
            self.request.send(to_send)
        return

try:
    address = ( sys.argv[1], 0 ) # get host from input line, and let the system provide a port
    run_server = True
except:
    print "No host was given, so the server was not started"
    raise

if run_server:
    logging.basicConfig( level=logging.DEBUG, format="%(name)s: %(message)s" )
    
    # Set up a server, running in its own thread
    server = SocketServer.TCPServer( address, BZ2RequestHandler )
    ip, port = server.server_address
    
    t = threading.Thread( target=server.serve_forever )
    t.setDaemon(True)
    t.start()
    
    # If we've gotten this far without errors, start the client and do the connection thing
    run_client = True

if run_client:
    logger = logging.getLogger('Client')
    
    # Connect to the server
    logger.info('Connecting to the server as %s:%s', ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( (ip, port) )
    
    # Ask for a file
    try:
        requested_file = sys.argv[2]
    except:
        requested_file = data_file
        print "No file specified, defaulting to:", requested_file
    logger.debug("Requesting file: %s", requested_file)
    s.send(requested_file)
    
    # Wait to receive a response
    buffer = StringIO()
    decompressor = bz2.BZ2Decompressor()
    
    while True:
        response = s.recv(BLOCK_SIZE)
        if not response:
            break
        logger.debug( "READ '%s'", binascii.hexlify(response) )
        
        # Include any unconsumed data when feeding the decompressor
        decompressed = decompressor.decompress(response)
        if decompressed:
            logger.debug("DECOMPRESSED '%s'", decompressed)
            buffer.write(decompressed)
        else:
            logger.debug("BUFFERING...")
        
    full_response = buffer.getvalue()
    logger.debug('response matches file contents: %s', lorem == full_response)
        
    # Clean up
    s.close()
    server.shutdown()
    server.socket.close()
