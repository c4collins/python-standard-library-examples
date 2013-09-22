# encoding:utf-8
## 12.10 xmlrpclib - Client Library for XML-RPC
# XML-RPC is a lightweight remote procedure call protocol build on top of HTTP and XML.
# The xmlrpclib module lets a Python program communicate with an XML-RPC server written in any language.

import xmlrpclib
import datetime
import pprint
try:
    import cPickle as pickle
except:
    import  pickle as pickle

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )


# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - json", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

## Classes
class MyObj( object ):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __repr__(self):
        return "MyObj(%s, %s)" % ( repr(self.a), repr(self.b) )
        
## Functions

    
## Constants
chapter_sections = [ 
    { 'host':"localhost", 'port':"9000" },  # General use data
    {},
    { 'data_types':[
        ( 'boolean'     , True ), 
        ( 'integer'     , 1 ), 
        ( 'float'       , 2.5 ), 
        ( 'string'      , "some text" ), 
        ( 'datetime'    , datetime.datetime.now() ), 
        ( 'array'       , ['a', 'list'] ), 
        ( 'array'       , ('a', 'tuple') ), 
        ( 'structure'   , {'a':"dictionary"} ), 
        ],
    'data':{
        'boolean': True, 
        'integer': 1, 
        'float'  : 2.5, 
        'string' : "some text", 
        'datetime': datetime.datetime.now(), 
        'array'  : ['a', 'list'], 
        'array'  : ('a', 'tuple'), 
        'structure': {'a':"dictionary"}, 
        }
    },
    {},
    { 'string':"This is a string with control characters" + '\0'},
    {},
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):
    logger = logging.getLogger("12.10 xmlrpclib - Client Library for XML-RPC")   
    logger.info("\n\nAll of these examples use 12.10-xmlrpc_server.py as the server they run off of and it must be running for these examples to work, so, if it fails for that reason, this is your warning.\n")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.10.1 Connecting to a Server")
        ## 12.10.1 Connecting to a Server
        # The simplest way to connect a client to a server is to instantiate a ServerProxy object, giving it the URI of the server.
        # For example, the demo server runs on port 9000 on localhost.
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        logger.info("Ping: %s", server.ping())
        
        # Other options are available, however, to support alternate transport.
        # Both HTTP and HTTPS are supported out of the box, both with basic authentication.
        # To implement a new communication channel, only a new transport class is needed.
        # It could be an interesting exercise, for example, to implement XML-RPC over SMTP
        
        # The verbose option gives debugging information useful for resolving communication errors.
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), verbose=True )
        logger.info("Ping: %s", server.ping())
        
        # The default encoding can be changed from UTF-8 if an alternate system is needed.
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), encoding="ISO-8859-1" )
        logger.info("Ping: %s", server.ping())
        
        # The allow_none option controls whether Python's None value is automatically translated to a nil value or whether it causes an error
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), allow_none=True )
        logger.info("Allowed: %s", server.show_type(None))
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), allow_none=False )
        try:
            logger.info("Not-Allowed: %s", server.show_type(None))
        except TypeError, err:
            logger.error("Not-Allowed: %s", err )
    
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.10.2 Data Types")
        ## 12.10.2 Data Types
        # The XML-RPC protocol recognizes a limited set of common data types.
        # The types can be passed as arguments or return values and combined to create more complex data structures.
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        for t, v in chapter_sections[2]['data_types']:
            as_string, type_name, value = server.show_type(v)
            logger.info("%-12s: %s", t, as_string)
            logger.info("\t\t%s", type_name)
            logger.info("\t\t%s", value)
            
        # The data types can be nested to create values of arbitrary complexity
        arg = []
        for i in xrange(3):
            d = {}
            d.update( chapter_sections[2]['data'] )
            d['integer'] = i
            arg.append(d)
        
        logger.info( "Before:\n%s", arg)
        
        # When the server returns the data, it has been somewhat transformed.
        # Tuples are lists, datetime instances are Datetime objects, otherwise it's the same.
        logger.info( "after:\n%s", server.show_type(arg)[-1] )
        
        # XML-RPC supports dates as a native type, and xmlrpclib can use one of two classes to represent the date values in the outgoing proxy or when they are received from the server.
        # By default, an internal version of DateTime is used, but the use_datetime option turns on support for using the classes in the datetime module.
        
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.10.3 Passing Objects")
        ## 12.10.3 Passing Objects
        # Instances of Python classes are treated as structures and passed as a dictionary, with the attributes of the object as values in the dictionary
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        o = MyObj(1, 'b goes here')
        logger.info("o : %s", o)
        pprint.pprint( server.show_type(o) )
        
        # When a value is sent back to the client from the server, the result is a dictionary on the client
        # Since there is nothing encoded in the values to tell the server (or the client) that it should be instantiated as part of a class
        o2 = MyObj(2, o)
        logger.info("o2: %s", o2)
        pprint.pprint( server.show_type(o2) )
    
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.10.4 Binary Data")
        ## 12.10.4 Binary Data
        # All values passed to the server are encoded and escaped automatically.
        # However, some data types may contain characters hat are not valid XML.
        # For example, binary image data my include byte values in the ASCII control range 0-31.
        # To pass binary data, it is best to use the Binary class to encode it for transport. 
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        s = chapter_sections[4]['string']
        logger.info("Local string: %s", s)
        data = xmlrpclib.Binary( s )
        logger.info("As Binary: %s", server.send_back_binary(data) )
        
        try:
            logger.info("As string: %s", server.show_type(s) )
        except xmlrpclib.Fault, err:
            logger.error( err )
        
        # Binary objects can also be used to sent objects using pickle.
        # The normal security issues related to sending what amounts to executable code over the wire apply here
            # DO NOT do this, IF the communication channel IS NOT secure
            
        o = MyObj( 1, 'b goes here')
        logger.info("Local: %s", id(o))
        logger.info( o )
        logger.info( "As object:" )
        pprint.pprint( server.show_type(o) )
        
        p = pickle.dumps(o)
        b = xmlrpclib.Binary(p)
        r = server.send_back_binary(b)
        
        
        # The data attribute of the Binary instance contains the pickled version of the object, 
        o2 = pickle.loads(r.data)
        # Ss it has to be unpickled before it can be used, resulting in a new id value
        logger.info("\nFrom pickle: %s", id(o2))
        pprint.pprint( o2 )
    
    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("12.10.5 Exception Handling")
        ## 12.10.5 Exception Handling
        # since the XML-RPC server might be written in any language, exception classes cannot be transmitted directly.  
        # Instead, exceptions raised in the server are converted to Fault objects and raised as exceptions locally in the client.
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        try:
            server.raise_exception("The message")
        except Exception, err:
            # The original error message is saved in the faultString attribute, and the faultCode is set to an XML-RPC error number
            logger.info( "Fault code: %s", err.faultCode)
            logger.info( "Message   : %s", err.faultString)
        
    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("12.10.6 Combining Calls into One Message")
        ## 12.10.6 Combining Calls into One Message
        # Multicall is an extension to the XML-RPC protocol that allows more than one call to be sent at the same time, 
        # with the responses collected and returned to the caller.
        # The MultiCall class was added to xmlrpclib in Python 2.4
        server = xmlrpclib.ServerProxy( "http://%s:%s" % ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        # To use a multicall, invoke the methods on it as with a ServerProxy,
        multicall = xmlrpclib.MultiCall(server)
        multicall.ping()
        multicall.show_type(1)
        multicall.show_type('string')
        multicall.show_type("string")
        
        # then call the object with no arguments to actually run the remote functions.
        # The return value is an iterator that yields the results fromm all the calls.
        for i, r in enumerate(multicall()):
            logger.info( "%s : %s", i, r )
            
        # If one of the calls uses Fault, the exception is raised when the result is produced from the iterator and no more results are available.
        multicall.raise_exception("Next to last call stops execution.")
        multicall.show_type(5.5)
        
        try:
            for i, r in enumerate(multicall()):
                logger.info( "%s : %s", i, r )
        except xmlrpclib.Fault, err:
            logger.error( err )
        
        
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)