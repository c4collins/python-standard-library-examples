## 12.2 BaseHTTPServer - Base Classes for Implementing Web Servers
# BaseHTTPServer uses classes from SocketServer to create base classes for making HTTP servers.  
# HTTPServer can be used directly, but the BaseHTTPRequestHandler is intended to be extended to handle each protocol method (GET, POST, etc.)
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import urlparse
import cgi
import threading
import time

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
parser = argparse.ArgumentParser( description="Chapter 12 - The Internet - BaseHTTPServer", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = parser.parse_args()



## Classes
    ## 12.2.1
class GetHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        message_parts = [
            "CLIENT VALUES:",
            "client_address=%s (%s)" % ( self.client_address, self.address_string() ),
            "command=%s" % self.command,
            "path=%s" % self.path,
            "real path=%s" % parsed_path.path,
            "request version=%s" % self.request_version,
            '',
            "SERVER VALUES:",
            "server version=%s" % self.server_version,
            "sys version=%s" % self.sys_version,
            "protocol version=%s" % self.protocol_version,
            '',
            "HEADERS RECEIVED:",
        ]
        for name, value in sorted( self.headers.items() ):
            message_parts.append( "%s=%s" % ( name, value.rstrip() ) )
        message_parts.append('')
        message_parts.append("ALL SERVER OBJECT ATTRIBUTES (NO METHODS):")
      
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if not callable( attr ):
                message_parts.append("%s: %s" % (attr_name, attr) )

        message = '\r\n'.join( message_parts )
        # every response requires a response code
        self.send_response(200)
        self.end_headers()
        # wfile is a file handle wrapping the response socket
        self.wfile.write(message)
        return

    ## 12.2.2
class PostHandler( BaseHTTPRequestHandler ):
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers=self.headers,
            environ={ 'REQUEST_METHOD':'POST', 
                      'CONTENT_TYPE':self.headers['Content-Type'],
                    }
        )
        
        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Client: %s\n" % str( self.client_address ))
        self.wfile.write("User Agent: %s\n" % str( self.headers['User-Agent'] ))
        self.wfile.write("Path: %s\n" % str( self.path ))
        self.wfile.write("Form data:\n")
        
        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The filename contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                self.wfile.write("\t Uploaded %s as '%s' (%d bytes)\n" % \
                    (field, field_item.filename, file_len)
                )
            else:
                # Regular form value
                self.wfile.write( "\t%s-%s\n" %( field, form[field].value ) )
         
        return
        
    ## 12.2.3
class ThreadHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message)
        self.wfile.write('\n')
        return

class ThreadedHTTPServer( ThreadingMixIn, HTTPServer ):
    """Handle requests in a separate thread."""
    
    ## 12.2.4
class ErrorHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        self.send_error(404)
        return 
        
    ## 12.2.5
class SetHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        self.send_response(200)
        self.send_header( 'Last-Modified', self.date_time_string(time.time()) )
        self.end_headers()
        self.wfile.write('Response body.\n')
        return

## Constants
chapter_sections = [
    ## 12.2.1 HTTP GET
    { 'name':"HTTP GET", 'version':"12.2.1", 'handler':GetHandler, },
    # To add support for an HTTP method in a request-handler class, implement the method do_METHOD(),
    # relacing METHOD with a valid HTTP method (do_GET(), do_POST(), etc.)
    # These request handler methods take no arguments, all parameters for the request are parsed 
    # by BaseHTTPRequestHandler and stored as instance attributes or the request instance.

    ## 12.2.2 HTTP POST
    { 'name':"HTTP POST", 'version':"12.2.2", 'handler':PostHandler, },
    # Supporting POST requests is more work because the base class dos not parse the data form automatically.
    # The cgi module provides the FieldStorage class, which knows how to parse the form if give the correct inputs.

    # Running from another terminal, you can see this in action with something like:
    #   curl http://192.168.1.150:8002 -F name=server -F face=back -F datafile=@12.1-urlparse.py
    # -F denotes a form field

    ## 12.2.3 Threading and Forking
    { 'name':"Threading and Forking", 'version':"12.2.3", 'handler':ThreadHandler, },
    # HTTPServer does not use multiple threads or processes to handle requests.
    # To add threading or forking, create a new class using the appropriate mix-in from SocketServer

    ## 12.2.4 Handling Errors
    { 'name':"Handling Errors", 'version':"12.2.4", 'handler':ErrorHandler, },
    # Handle errors by calling send_error(), passing the appropriate error code and an optional error message
    # The entire response is generated automatically

    ## 12.2.5 Setting Headers
    { 'name':"Setting Headers", 'version':"12.2.5", 'handler':SetHandler, },
    # The send_header() method adds header data to the HTTP response.
    # It takes two arguments, the name of the header and the value
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    for i, section in enumerate(chapter_sections):
        if results.section == i+1 or results.section == 0:
            print section
            logger = logging.getLogger( "%s %s" % ( section['version'], section['name'] ) )
            logger.info("Showing: %s %s", section['version'], section['name'] )
            server = ThreadedHTTPServer( ('192.168.1.150', (8001 + i) ), section['handler'] )
            ip, port = server.server_address
            logger.info("SERVER RUNNING ON: %s:%s", ip, port )
            logger.info("Starting server, user <Ctrl-C> to stop")
            server.serve_forever()

    
else:
    # If the command isn"t recognized because it wasn"t given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn"t recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)