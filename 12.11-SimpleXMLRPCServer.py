# encoding:utf-8
## 12.11 SimpleXMLRPCServer - An XML-RPC Server
# The SimpleXMLRPCServer module contains classes for creating cross-platform, language-independent servers using the XML-RPC protocol
# Client libraries exist for many other languages besides Python, making XML-RPC an easy choice for building RPC-style services.
from SimpleXMLRPCServer import SimpleXMLRPCServer, list_public_methods
import os
import inspect

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - SimpleXMLRPCServer", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

## Functions
def list_contents( dir_name ):
    logger = logging.getLogger( "Function: list_contents" )
    logger.info( "list_contents( %s )", dir_name )
    return os.listdir(dir_name)
    
def multiply(a, b):
    return a*b
    
def expose(f):
    """Decorator to set exposed flag on a function."""
    f.exposed = True
    return f
    
def is_exposed(f):
    """Test whether another function should be publicly exposed."""
    return getattr(f, 'exposed', False)
    
## Classes

class ServiceRoot( object ):
    pass

class DirectoryService( object ):
    def list( self, dir_name ):
        """list(dir_name) => [<flienames>]
        returns a list containing the contents of the named directory."""
        
        return os.listdir( dir_name ) 
        
    def _listMethods(self):
        """The convenience function list_public_methods() scans an instance to return the names of callable attributes that do not start with an underscore."""
        # redefine _listMethods() to apply whatever rules are desired.
        return list_public_methods(self)
        
    def _methodHelp(self, method):
        """Returns the docstring of the function"""
        f = getattr(self, method)
        return inspect.getdoc(f)

class MyService( object ):
    PREFIX = "prefix"
    
    def _dispatch(self, method, params):
        """This method is invoked when a client tries to access a function that is part of MyService
        It enforces the use of a prefix, and requires the function to have an attribute called exposed with a True value"""
        # remove the prefix from the method name
        if not method.startswith(self.PREFIX + '.'):
            raise Exception( "Method (%s) is not supported" % method )
        method_name = method.partition('.')[2]
        func = getattr( self, method_name )
        if not is_exposed(func):
            raise Exception( "Method (%s) is not supported" % method )
        return func(*params)
        
    # The exposed flag is set on a function using a decorator for convenience
    @expose
    def public(self):
        """This method is marked as exposed to the XML-RPC service"""
        return "This is public"
        
    def private(self):
        """This method is not exposed to the XML-RPC service"""
        return "This is private"
    
## Constants
chapter_sections = [ 
    { 'host':"192.168.1.150", 'port':9000 },
    {},
    {},
    {},
    {},
    {},
    {},
    {},
]
        
## Runtime Configuration
if results.section in xrange( 1, len(chapter_sections) ):
    logger = logging.getLogger("12.11 SimpleXMLRPCServer - An XML-RPC Server")   
    logger.info("\n\nAll of these examples use a client program as well, because these are just servers. So, now that you've started the server, go start the client.\n")

    if results.section == 1:
        logger = logging.getLogger("12.11.1 A Simple Server")
        ## 12.11.1 a Simple Server
        # This simple server exposes a single function that takes the name of a directory and returns the contents.
                
        # The first step is to create the SimpleXMLRPCServer instance and then tell it where to listen for incoming requests
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        # The next step is to define a function to be part of the service and register it so that the server knows how to call it.
        server.register_function( list_contents )
        
        # The final step is to put the server into an infinite loop receiving and responding to requests.
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
        # The server can then be accessed at the URL provided using the client class from xmlrpclib
        # The file 12.11-SimpleXMLRPCServer_client.py is the simplest client that can exist.
        # The arguments are formatted as XML and then sent to the server in a POST message.
        # The server unpacks the XML and determines which function to call based on the method name invoked form the client'
        # The arguments are passed to the function, and the return value is translated back into XML to be returned to the client.
        
    if results.section == 2:
        logger = logging.getLogger("12.11.2 Alternate API Names")
        ## 12.11.2 Alternate API Names
        # Sometimes the function names used inside a module or library are not the names that should be used in the external API
        # Names may change because a platform-specific implementation is loaded, 
        # the service API is built dynamically based on a configuration file,
        # or real functions are to be replaced with stubs for testing.
        
        # To register a function with an alternate name, pass the name as the second argument to register_function()
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ) )
        
        server.register_function( list_contents, 'ls' )
        
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
            
    if results.section == 3:
        logger = logging.getLogger("12.11.3 Dotted API Names")
        ## 12.11.3 Dotted API Names
        # Individual functions can be registered with names that are not normally legal for Python identifiers.
        # For example, a period (.) can be included in names to separate the namespace in the service.
        # The next example extends the directory service to add create and remove calls.
        # All functions are registered using the prefix 'dir.' so that the same server can provide other services using different paths.
        # One other difference in this example is that some of the functions return None, so the server has been told to translate None to a nil value.
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), allow_none=True )
        
        server.register_function( os.listdir, "dir.list")
        server.register_function( os.mkdir, "dir.create")
        server.register_function( os.rmdir, "dir.remove")
        
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
        
    if results.section == 4:
        logger = logging.getLogger("12.11.4 Arbitrary API Names")
        ## 12.11.4 Arbitrary API Names
        # Another interesting feature is the ability to register functions with names that are otherwise invalid Python-object attribute names
        # This example service registers a fucntion with the name "multiply args"
        server.register_function( multiply, "multiply args")
        
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
            
        # But just because you can, doesn't mean you should.  Just that you can.
        # Existing services with arbitrary names need to be compatible with new programs.
    
    if results.section == 5:
        logger = logging.getLogger("12.11.5 Exposing Methods of Objects")
        ## 12.11.5 Exposing Methods of Objects
        # The earlier sections go over techniques for establishing APIs using good naming conventions and namespacing.
        # Another way to incorporate namespacing into an API is to use instances of classes and expose their methods.
        # The first example can be rewritten using an instance with a single method.
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), logRequests=True )
        
        # This allows for dotted names
        root = ServiceRoot()
        root.dir = DirectoryService()
        
        # By registering this server instance with allow_dotted_names, the server has permission to walk the tree of objects
        server.register_instance( root, allow_dotted_names=True )
        
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
            
    if results.section == 6:
        logger = logging.getLogger("12.11.6 Dispatching Calls")
        ## 12.11.6 Dispatching Calls
        # By default, register_instance() finds all callable attributes of the instance with names not starting with an underscore.
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), logRequests=True )
        server.register_instance( MyService() )
        
        # There are other ways to override the dispatching mechanism,
        # such as subclassing directly from SimpleXMLRPCServer
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
    
    if results.section == 7:
        logger = logging.getLogger("12.11.7 Introspection API")
        ## 12.11.7 Introspection API
        # As with many network services, it is possible to query an XML-RPC server to ask it what methods it supports and learn how to use them.
        # SimpleXMLRPCServer includes a set of public methods for performing this introspection.
        # Be default, they are disabled, but can be enabled with register_introspection_functions()
        # Support for system.listmethods() and system.methodHelp() can be added to a service by defining _listMethods() and _methodHelp() on the service class
        server = SimpleXMLRPCServer( ( chapter_sections[0]['host'], chapter_sections[0]['port'] ), logRequests=True )
        server.register_introspection_functions()
        server.register_instance( DirectoryService() )
        
        try:
            logger.info( "Use CTRL-C to exit" )
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info( "Exiting" )
        
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)