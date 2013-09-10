## 12.3 urllib - Network Resource Access
# The urllib module provides a simple interface for network resource access.
# It also includes functions for encoding and quoting arguments to be passed over HTTP to a server
import urllib
import os

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
parser = argparse.ArgumentParser( description="Chapter 12 - The Internet - urllib", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = parser.parse_args()


## Functions
def reporthook( blocks_read, block_size, total_size):
	""" total_size is reported in bytes
	block_size is the amount read each time
	blocks_read is the number of blocks successfully read."""
	logger = logging.getLogger("reporthook")
	logger.debug("reporthook( %s, %s, %s )", blocks_read, block_size, total_size)
	
	if not blocks_read:
		logger.info("Connection opened.")
		return
	if total_size < 0:
		# unknown size
		logger.info("Read %d blocks (%d bytes)", blocks_read, blocks_read * block_size )
	else:
		amount_read = blocks_read * block_size
		logger.info("Read %d blocks (%d bytes)", blocks_read, blocks_read * block_size )
	return
		

## Constants

test_url = 'http://192.168.1.160'
chapter_sections = [
	{ 'file_to_get':test_url, 'reporthook':reporthook }, # Section 1
    [ {'q':"query string", 'foo':"bar", },               # Section 2
      { 'foo':['foo1', 'foo2',] }, 
      { 'url': test_url + ':80/bandb/' }, 
    ],
    ['/a/b/c/', r'\a\b\c', r'C:\a\b\c'],                 # Section 3    
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    if results.section == 1 or results.section == 0:
        ## 12.3.1 Simple Retrieval and Cache
        # urlretrieve() will download data from a URL
        # It takes arguments for the URL, a temp file to hold the data, a function to repoort on download progress, 
        # and data to pass if the URL referes to a form where data should be posted
        # If no folename is given, urlretrieve creates a tempfile.
        # The calling program can delete the file directly or treat it as a cache and use urlcleanup() to remove it
        logger = logging.getLogger("Section 12.3.1 Simple Retrieval and Cache")
        filename, msg = ( urllib.urlretrieve( chapter_sections[0]['file_to_get'], reporthook=chapter_sections[0]['reporthook'] ) )
        logger.info('\tFile: %s', filename)
        logger.info('\tHeaders:\n%s', msg)
        logger.debug('File Exists before cleanup: %s', os.path.exists(filename) )
        urllib.urlcleanup()
        logger.debug('File Exists after cleanup: %s', os.path.exists(filename) )
        
    if results.section == 2 or results.section == 0:
        ## 12.3.2 Encoding Arguments
        # Arguments can be passed to the server by encoding them and appending them to the url
        logger = logging.getLogger("Section 12.3.2 Encoding Arguments")
        query_args = chapter_sections[1]
        encoded_args = urllib.urlencode( query_args[0] )
        logger.debug( "Encoded: %s", encoded_args )
        url = test_url + '/?' + encoded_args
        logger.info( "URL     : %s", urllib.urlopen(url).read()[:100] ) 
        logger.debug( "Stopped after %s characters", '100' )
        
        # Sequences work too, but they need to be encoded with doseq=True
        logger.debug( "Single  :\n%s", urllib.urlencode( query_args[1] ) )
        logger.debug( "Sequence:\n%s", urllib.urlencode( query_args[1], doseq=True ) )
        
        # urllib also include quote() and quote_plus() for escaping characters
        # and unquote and unquote_plus will return them to their previous states
        logger.debug( "urlencode():\n%s", urllib.urlencode( {'url':query_args[2]['url'] } ) )
        quote = urllib.quote( query_args[2]['url'] )
        logger.debug( "quote():\n%s", quote )
        logger.debug( "unquote():\n%s", urllib.unquote( quote ) )
        quote_plus = urllib.quote_plus( query_args[2]['url'] )
        logger.debug( "quote_plus():\n%s", quote_plus )
        logger.debug( "unquote_plus():\n%s", urllib.unquote_plus( quote_plus ) )
        
    if results.section == 3 or results.section == 0:
        ## 12.3.3 Paths vs. URLS
        # Some OSs use different values for separating components of paths in local files than in URLs
        # To make code portable, use the functions pathname2url() or url2pathname() to convert back and forth
        logger = logging.getLogger("Section 12.3.3 Paths vs. URLS")
        for path in chapter_sections[2]:
            logger.info( "Original: %s", path )
            revert_path = urllib.pathname2url( path )
            logger.info( "URL     : %s", revert_path )
            logger.info( "Path    : %s", urllib.url2pathname( revert_path ) )
   
else:
    # If the command isn"t recognized because it wasn"t given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn"t recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)