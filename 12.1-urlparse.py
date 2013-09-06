## 12.1 urlparse - Split URLs into Components
# urlparse provides functions for breaking URLs into their component parts as defined by RFC
from urlparse import urlparse
import logging
import argparse

# Set up logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(threadName)-10s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
parser = argparse.ArgumentParser( description="Chapter 12", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest="section", help="Enter the section number to see the results from that section.  i.e for 12.1.1, enter 1, for 12.1.10 enter 10 ")

results = parser.parse_args()



## Functions
def log_parsed_url( parsed ):
    """Prints info parsed from a url"""
    logger = logging.getLogger("log_parsed_url")
    logger.info( "scheme  : %s", parsed.scheme )
    logger.info( "netloc  : %s", parsed.netloc )
    logger.info( "path    : %s", parsed.path )
    logger.info( "params  : %s", parsed.params )
    logger.info( "query   : %s", parsed.query )
    logger.info( "fragment: %s", parsed.fragment )
    logger.info( "username: %s", parsed.username )
    logger.info( "password: %s", parsed.password )
    logger.info( "hostname: %s", parsed.hostname )
    logger.info( "port    : %s", parsed.port )
    return



## 12.1.1 Parsing
if results.section == 1:
    logger = logging.getLogger("12.1.1 Parsing")
    # The return value from urlpase() in an object that acts like a tuple with 6 elements
    url = "http://bittchinsdesign.ca/path;param?query=arg#frag"
    parsed = urlparse(url)
    logger.info( parsed )
    log_parsed_url( parsed )
    
 
    
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        results = parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it's wrong, show an error.
        logging.warning("Command not recognized: %s", results.section)
        


    
    