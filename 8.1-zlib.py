## 8.1 zlib - GNU zlib Compression
# the zlib module provides a low-level interface to many of the functions 
# in the zlib compression library from GNU
import zlib, binascii, sys
import logging, SocketServer, socket, threading
try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

## 8.1.1 Working on Data in Memory
original_data = "This is the original text."
print 'Original    :', len(original_data), original_data

compressed_data = zlib.compress(original_data)
print 'Compressed  :', len(compressed_data), binascii.hexlify(compressed_data)

decompressed_data = zlib.decompress(compressed_data)
print 'Decompressed:', len(decompressed_data), decompressed_data
print
# Sometimes compressed data is longer than decompressed data
fmt = "%15s %15s"
print fmt % ( 'len(data)', 'len(compressed)' )
print fmt % ( '-' * 15, '-' * 15 )

for i in xrange(5):
    data = original_data*i
    compressed = zlib.compress(data)
    highlight = "*" if len(data) < len(compressed) else " "
    print fmt % ( len(data), len(compressed) ), highlight
print

## 8.1.2 Incremental Compression and decompression
# The in-memory approach is impractical for many real-world applications, 
# moreso as the size of the data files grows
# Compress and Decompress objects can manipulate data incrementally 
# so the entire data set does not have to fit into memory twice
BLOCK_SIZE = 64
DATA_FILE = 'data/lorem.txt'
compressor = zlib.compressobj(1)

with open( DATA_FILE, 'r' ) as input:
    while True:
        # read in small amounts of data from file
        block = input.read( BLOCK_SIZE )
        if not block:
            break
        # Give those bits to the compressor object and see if it has anything to print
        compressed = compressor.compress(block)
        if compressed:
            print 'Compressed: %s' % binascii.hexlify(compressed)
        else:
            print 'Buffering...'
    # When we run out of data to process, flush out the buffer o close out the final block
    remaining = compressor.flush()
    print 'Flushed: %s' % binascii.hexlify(remaining)
print
   
## 8.1.3 Mixed Content Streams
# The Decompress class returned by decompressobj() can also be used in situations 
# where compressed and uncompressed data are mixed

lorem = open( 'data/lorem.txt', 'r' ).read()
compressed = zlib.compress(lorem)
combined = compressed + lorem

decompressor = zlib.decompressobj()

# Items decompressable are returned
decompressed = decompressor.decompress(combined)
print 'Decompressed matches lorem:', decompressed == lorem
# Items that were not compressed are left in the unused_data attribute
print 'Unused data matches lorem :', decompressor.unused_data == lorem
print

## 8.1.4 Checksums
# zlib contains two functions for computing checksums of data: adler32() and crc32()
# neither is cryptographically secure and should only be used for data-integrity verification
# both functions take a string of data and an optional value to be used as a starting point for the checksum
    # zlib.adler32( data_string[, checksum_startpoint] ) / zlib.crc32( data_string[, checksum_startpoint] )
# They return a 32-bit signed integer value that can be passed back in subsequent calls as a new starting point
# this will produce a running checksum
cksum = zlib.adler32(lorem)
print 'Adler32: %12d' % cksum
print '       : %12d' % zlib.adler32(lorem, cksum)

cksum = zlib.crc32(lorem)
print 'CRC-32 : %12d' % cksum
print '       : %12d' % zlib.crc32(lorem, cksum)
print

## 9.1.5 Compressing Network Data
# This server uses the stream compressor to respond to requests of filenames
# by writing a compressed version of the file to the socket used to communicate with the client
# Some chunking has been artificially added
class ZlibRequestHandler( SocketServer.BaseRequestHandler ):
    logger = logging.getLogger('Server')
    
    def handle(self):
        compressor = zlib.compressobj(1)
        
        # Find out what file the client wants
        filename = self.request.recv(1024) # check port 1024 for requests
        self.logger.debug( "client asked for: '%s'", filename)

        
      
        # Send chunks of the file as they are compressed
        with open( filename, 'rb' ) as input:
            while True:
                block = input.read( BLOCK_SIZE )
                if not block:
                    break
                self.logger.debug("RAW '%s'", block)
                compressed = compressor.compress( block )
                if compressed:
                    self.logger.debug("SENDING '%s'", binascii.hexlify(compressed) )
                    self.request.send(compressed)
                else:
                    self.logger.debug("BUFFERING")
                
        # Send any data being buffered by the compressor
        remaining = compressor.flush()
        while remaining:
            to_send = remaining[:BLOCK_SIZE]
            remaining = remaining[BLOCK_SIZE:]
            self.logger.debug("FLUSHING '%s'", binascii.hexlify(to_send))
            self.request.send(to_send)
        return


run_server, run_client = False, False
try:
    address = ( 'localhost', 0) # the ports must flow
    run_server = True
except:
    print "The server was not started as a host was not specified."

if run_server:
    logging.basicConfig( level=logging.DEBUG, format='%(name)s: %(message)s', )
    clientLogger = logging.getLogger('Client')
    
    # Set up server, running in a separate thread
    server = SocketServer.TCPServer( address , ZlibRequestHandler )
    ip, port = server.server_address
    print ip, port
    
    t = threading.Thread( target=server.serve_forever )
    t.setDaemon(True)
    t.start()
    
    run_client= True

if run_client:
    # Connect to the server as a client
    clientLogger.info('Contacting server on %s:%s', ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( (ip, port) )
    
    # Ask for a file
    requested_file = DATA_FILE
    clientLogger.debug("sending filename: '%s'", requested_file)
    s.send(requested_file)
    
    # Wait to receive a response
    buffer = StringIO()
    decompressor = zlib.decompressobj()
    
    while True:
        response = s.recv(BLOCK_SIZE)
        if not response:
            break
        clientLogger.debug( "READ '%s'", binascii.hexlify(response) )
        
        # Include any unconsumed data when feeding the decompressor
        to_decompress = decompressor.unconsumed_tail + response
        while to_decompress:
            decompressed = decompressor.decompress(to_decompress)
            if decompressed:
                clientLogger.debug("DECOMPRESSED '%s'", decompressed)
                buffer.write(decompressed)
                # look for unconsumed data due to buffer overflow
                to_decompress = decompressor.unconsumed_tail
            else:
                clientLogger.debug("BUFFERING")
                to_decompress = None
        
    # Deal with data remaining inside the decompressor buffer
    remainder = decompressor.flush()
    if remainder:
        clientLogger.debug("FLUSHED '%s'", remainder)
        buffer.write(remainder)
    
    full_response = buffer.getvalue()
    clientLogger.debug('response matches file contents: %s', lorem == full_response)
        
    # Clean up
    s.close()
    server.socket.close()
            
print

