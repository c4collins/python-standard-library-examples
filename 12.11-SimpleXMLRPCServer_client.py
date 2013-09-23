import xmlrpclib
import logging

# Setup logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)03d (%(name)s) %(message)s", datefmt='%H:%M:%S', )
logger = logging.getLogger( "RPC Client" )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - SimpleXMLRPCServer", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to use the client for that exercise.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

# The ServerProxy is connected to the server suing its base URL, and then methods are called directly on the proxy.
# Each method invoked on the proxy is translated into a request on the server.
proxy = xmlrpclib.ServerProxy('http://192.168.1.150:9000')


if results.section == 1:
    logger.info( "Command: %s : %s", 'proxy.list_contents("/srv")', proxy.list_contents('/srv') )

if results.section == 2:
    logger.info( "Command: %s : %s",  'proxy.ls("/srv")',  proxy.ls('/srv') )
          
if results.section == 3:
    # To call dotted service functions in the client, you just call the dotted name.
    fmt = "%-12s : %s"
    logger.info( fmt, "BEFORE", 'EXAMPLE' in proxy.dir.list('/tmp') )
    logger.info( fmt, "CREATE", proxy.dir.create('/tmp/EXAMPLE') )
    logger.info( fmt, "SHOULD EXIST", 'EXAMPLE' in proxy.dir.list('/tmp') )
    logger.info( fmt, "REMOVE", proxy.dir.remove('/tmp/EXAMPLE') )
    logger.info( fmt, "AFTER", 'EXAMPLE' in proxy.dir.list('/tmp') )
    
if results.section == 4:
    logger.info( getattr( proxy, 'multiply args')(5, 5) )
    logger.info( getattr( proxy, 'multiply args')(5, 10) )
    logger.info( getattr( proxy, 'multiply args')(2, 256) )
    
if results.section == 5:
    #logger.info( "Command: %s : %s",  'proxy.list("/srv")',  proxy.list('/srv') )
    logger.info( "Command: %s : %s",  'proxy.dir.list("/srv/samba")',  proxy.dir.list('/srv/samba') )
    
if results.section == 6:
    logger.info( "private(): %s", proxy.prefix.public() )
    try:
        logger.info( "private(): %s", proxy.prefix.private() )
    except Exception, err:
        logger.error( err )
    try:
        logger.info( "public without prefix(): %s", proxy.public() )
    except Exception, err:
        logger.error( err )
        
        
if results.section == 7:
    for method_name in proxy.system.listMethods():
        logger.info( "=" * 60 )
        logger.info( method_name )
        logger.info( "=" * 60 )
        logger.info( proxy.system.methodHelp( method_name ) )