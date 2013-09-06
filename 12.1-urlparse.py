## 12.1 urlparse - Split URLs into Components
# urlparse provides functions for breaking URLs into their component parts as defined by RFC
import urlparse
import logging
import argparse

# Set up logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
parser = argparse.ArgumentParser( description="Chapter 12 - The Internet", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest="section", help="Enter the section number to see the results from that section.  i.e for 12.1.1, enter 1, for 12.1.10 enter 10.  Entering 0 will run all sections.")

results = parser.parse_args()



## Functions
def log_parsed_url( parsed ):
    """Prints info parsed from a url"""
    logger = logging.getLogger("log_parsed_url")
    parse_list = [  'scheme', 
                    'netloc', 
                    'path', 
                    'params', 
                    'query', 
                    'fragment', 
                    'username', 
                    'password', 
                    'hostname', 
                    'port',
    ]
    for attr in parse_list:
        if hasattr(parsed, attr):
            logger.info( "%-8s: %s", attr, getattr(parsed, attr) )
    return

simple_url = "http://NetLoc/path;param?query=arg#frag"
complex_url = "http://user:pwd@NetLoc:80/p1;param/p2;param?query-arg#frag"

if results.section in [0,1,2]:

    ## 12.1.1 Parsing
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.1.1 Parsing")
        # The return value from urlparse() in an object that acts like a tuple with 6 elements
        logger.debug( "urlparse.urlparse( )" )
        logger.debug( "urlparse.urlparse( %s )", simple_url )
        log_parsed_url( urlparse.urlparse(simple_url) )
        
        # urlsplit() is an alternative to urlparse by keeping parameters with the url
        logger.debug( "urlparse.urlsplit( )" )
        logger.debug( "urlparse.urlsplit( %s )", complex_url )
        log_parsed_url( urlparse.urlsplit( complex_url ) )
     
        # To simply string the gragment identifier from a URL, use urldefrag()
        url, fragment = urlparse.urldefrag(simple_url)
        logger.debug( "urlparse.urldefrag( )" )
        logger.debug( "urlparse.urldefrag( %s )", simple_url )
        logger.debug( "URL     : %s", simple_url )
        logger.debug( "Fragment: %s", fragment )
        
    ## 12.1.2 Unparsing
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.1.2 Unparsing")
        # There are several ways to assemble the parts of a split URL back into a single string.
        # The parsed URL has a geturl() method
        logger.debug( "Original: %s", simple_url )
        logger.debug( "Parsed  : %s", urlparse.urlparse( simple_url ).geturl()  )
    
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it's wrong, show an error.
        logging.warning("Command not recognized: %s", results.section)
        


    
    