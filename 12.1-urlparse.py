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

## Constants
simple_url = "http://NetLoc/path;param?query=arg#frag"
complex_url = "http://user:pwd@NetLoc:80/p1;param/p2;param?query-arg#frag"
extra_url = "http://NetLoc/path;?#"
base_url = "http://www.example.com/path/file.html"

if results.section in [0,1,2,3]:

    ## 12.1.1 Parsing
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.1.1 Parsing")
        logger.info("Showing: 12.1.1 Parsing")
       
       # The return value from urlparse() in an object that acts like a tuple with 6 elements
        logger.debug( "urlparse.urlparse( )" )
        logger.debug( "urlparse.urlparse( %s )", simple_url )
        log_parsed_url( urlparse.urlparse(simple_url) )
        
        # urlsplit() is an alternative to urlparse by keeping parameters with the url
        logger.debug( "urlparse.urlsplit( )" )
        logger.debug( "urlparse.urlsplit( %s )", complex_url )
        log_parsed_url( urlparse.urlsplit( complex_url ) )
        # urlsplit() returns an object that acts like a tuple with 5 elements, as there are no params
     
        # To simply string the gragment identifier from a URL, use urldefrag()
        url, fragment = urlparse.urldefrag(simple_url)
        logger.debug( "urlparse.urldefrag( )" )
        logger.debug( "urlparse.urldefrag( %s )", simple_url )
        logger.debug( "URL     : %s", simple_url )
        logger.debug( "Fragment: %s", fragment )
        
    ## 12.1.2 Unparsing
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.1.2 Unparsing")
        logger.info("Showing: 12.1.2 Unparsing")
        
        # There are several ways to assemble the parts of a split URL back into a single string.
        # The parsed URL has a geturl() method
        logger.debug( "Original: %s", simple_url )
        logger.debug( "Parsed  : %s", urlparse.urlparse( simple_url ).geturl()  )
        # geturl() only works on an object returned by urlparse() or urlsplit()
        
        # A regular tuple containing strings can be combined into a URL with urlunparse()
        logger.debug( "Original: %s", simple_url )
        parsed = urlparse.urlparse( simple_url )
        logger.debug( "Parsed  : %s [%s]", parsed, type(parsed) )
        t = parsed[:]
        logger.debug( "Tuple   : %s [%s]", t, type( t ) )
        logger.debug( "Built   : %s", urlparse.urlunparse( t ) )
        
        # If the input URL has superfluous parts, they may be dropped when reconstructed
        logger.debug( "Original: %s", extra_url )
        parsed = urlparse.urlparse( extra_url )
        logger.debug( "Parsed  : %s [%s]", parsed, type(parsed) )
        t = parsed[:]
        logger.debug( "Tuple   : %s [%s]", t, type( t ) )
        logger.debug( "Built   : %s", urlparse.urlunparse( t ) )
        
    ## 12.1.3 Joining
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.1.3 Joining")
        logger.info("Showing: 12.1.3 Joining")
        
        # In addition to parsing URLs, urljoin() will construct absolute URLs from relative fragments
        logger.debug( "Base URL: %s", base_url )
        logger.debug( "Add File: %s", urlparse.urljoin( base_url, "anotherfile.html" )  )
        logger.debug( "Another : %s", urlparse.urljoin( base_url, "../anotherfile.html" )  )
        # Note that urljoin() respects and interprets '../' correctly
        logger.debug( "With /  : %s", urlparse.urljoin( base_url, "/subpath/thirdfile.html" )  )
        logger.debug( "Without : %s", urlparse.urljoin( base_url, "subpath/fourthfile.html" )  )
    
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it's wrong, show an error.
        logging.warning("Command not recognized: %s", results.section)
        


    
    