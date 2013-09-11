## 12.6 robotparser - Internet Spider Access Control
# robotparser implements a parser for robots.txt files, 
# including a function that checks if a given user-agent can access a given resource.
# It is intended for use in well-behaves spiders and other  crawler applications that need to be throttled or otherwise restricted
import robotparser
import urlparse
import time

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - robotparser", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

## Classes

      
        
## Constants
chapter_sections = [ {}, 
                     { 'agent_name':"PythonSTL", 
                       'base_url':"http://192.168.1.160/", 
                       'paths':[ "/", "/bandb/", "/admin/", "/static/style.css"],
                     }, 
                     { 'agent_name':"PythonSTL", 
                       'base_url':"http://192.168.1.160/", 
                       'paths':[ "/", "/bandb/", "/admin/", "/static/style.css"],
                     },
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.6.1 robots.txt")
        ## 12.6.1 robots.txt
        # The robots.txt file format is a simple text-based access control system for computer programs that automatically access web resources
        # The file is made up of records that specify the user-agent identifier for the program followed by a list of URLs the agent may not access
        """User-agent: *
        Disallow: /admin/
        Disallow: /downloads/
        Disallow: /media/
        Disallow: /static/
        """
        # It prevents access to parts of the site that are expensive to compute and would overload a server if a search engine tried to index them
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.6.2 Testing Access Permissions")
        ## 12.6.2 Testing Access Permissions
        parser = robotparser.RobotFileParser()
        parser.set_url( urlparse.urljoin( chapter_sections[1]['base_url'], 'robots.txt') )
        parser.read()
        
        for path in chapter_sections[1]['paths']:
            logger.info("%6s : %s", parser.can_fetch( chapter_sections[1]['agent_name'], path ), path )
            url = urlparse.urljoin( chapter_sections[1]['base_url'], path )
            logger.info("%6s : %s", parser.can_fetch( chapter_sections[1]['agent_name'], url ), url )
     
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.6.3 Long Lived Spiders")
        ## 12.6.3 Long Lived Spiders
        # An application that takes a long time to process he resources it downloads or that is throttled to pause between downloads 
        # should check for new robots.txt files periodically, based on the age of the content it has downloaded already.
        # The age is not managed automatically, but there are convenience methods to make tracking it easier
        parser = robotparser.RobotFileParser()
        parser.set_url( urlparse.urljoin( chapter_sections[2]['base_url'], 'robots.txt') )
        parser.read()
        parser.modified()
        
        for path in chapter_sections[2]['paths']:
            age = int( time.time() - parser.mtime() )
            logger.debug( "Age: %s", age )
            
            # This is a bit of an extreme example, wondering if the one-second old robots.txt is out-dated
            if age > 1:
                logger.info('Rereading robots.txt')
                parser.read()
                parser.modified()
            logger.info( "%6s : %s", parser.can_fetch( chapter_sections[2]['agent_name'], path ), path )
            
            # simulate a delay in processing
            time.sleep(1)
        
   
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
