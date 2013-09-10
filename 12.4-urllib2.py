## 12.3 urllib2 - Network Resource Access
# The urllib2 module provides an updated API for network resources identified by URLs.
# It is designed to be extended by individual applications to support new protocols,
# Or add variations to existing protocols (such as handling HTTP basic authentication)
import urllib2
import urllib
import itertools
import mimetypes, mimetools
import os
import tempfile

try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
parser = argparse.ArgumentParser( description="Chapter 12 - The Internet - urllib2", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = parser.parse_args()

## Classes

# for 12.4.6
class MultiPartForm( object ):
    """ Accumulate the data to be used when postign a form."""
    
    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        
    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary
        
    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append( (name, value) )
        return
        
    def add_file( self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded"""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = ( mimetypes.guess_type( filename )[0] or 'application/octet-stream' )
        self.files.append( ( fieldname, filename, mimetype, body) )
        return
        
    def __str__(self):
        """Return a string representing the form data, including attached files"""
        # Build a list of lists, each containing "lines" of the request.
        # Each part is separated by a boundary string.
        # Once the list is built, return a string where wach line is separated by '\r\n'
        parts = []
        part_boundary = '--' + self.boundary
        
        # Add the form fields
        parts.extend( 
            [ part_boundary, 
                'Content-Disposition: file; name="%s"; fieldname="%s' % ( fieldname, filename),
                'Content-Type: %s' % content_type,
                '',
                body,
            ] for fieldname, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker, and the return CR+LF separated data
        flattened = list( itertools.chain( *parts ) )
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join( flattened )

# for 12.4.7
class NFSFile(file):
    def __init__(self, tempdir, filename):
        self.tempdir = tempdir
        self.logger = logging.getLogger("NFSFile")
        file.__init__(self, filename, 'rb')
    def  close(self):
        self.logger.info("NFSFile:")
        self.logger.info("\tunmounting %s", os.path.basename( self.tempdir ) )
        self.logger.info("\twhen %s is closed", os.path.basename( self.name ) )
        return file.close(self)

# for 12.4.7
class FauxNFSHandler( urllib2.BaseHandler ):
    def __init__(self, tempdir):
        self.logger = logging.getLogger("FauxNFSHandler")
        self.tempdir = tempdir
        
    def nfs_open(self, req):
        url = req.get_selector()
        directory_name, file_name = os.path.split(url)
        server_name = req.get_host()
        self.logger.info("FauxNFSHandler simulating mount:")
        self.logger.info("\tRemote path: %s", directory_name )
        self.logger.info("\terver      : %s", server_name )
        self.logger.info("\tLocal path : %s", os.path.basename(tempdir) )
        self.logger.info("\tFilename   : %s", file_name )
        local_file = os.path.join( tempdir, file_name )
        fp = NFSFile( tempdir, local_file )
        content_type = ( mimetypes.guess_type( file_name )[0] or 'application/octet-stream' )
        stats = os.stat(local_file)
        size = stats.st_size
        headers = { 'Content-type'   : content_type,
                    'Content-length' : size,
        }
        return urllib.addinfourl( fp, headers, req.get_full_url() )
        
        
## Constants

test_url = 'http://192.168.1.150'
chapter_sections = [ {}, 
                     { 'q':"query string", 'foo':"bar", }, 
                     { 'first':"First Name", 'last':"Last Name", }, 
                     {},
                     { 'first_name':"Charlie", 'last_name':"and the Chocolate Factory", },
                     {},
                     {},
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    ## NOTE: This is a client for the HTTP GET server from 12.2-BaseHTTPServer.py
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.4.1 HTTP GET")
        ## 12.4.1 HTTP GET
        # as with urllib, urllib2's HTTP GET is really simple
        port = '8001'
        logger.info("Opening %s:%s", test_url, port )
        response = urllib2.urlopen( test_url + ':' + port )
        logger.debug('RESPONSE : %s', response )
        logger.debug('URL      : %s', response.geturl() )
        headers = response.info()
        logger.debug('DATE     : %s', headers['date'] )
        logger.debug('HEADERS  :' )
        for header in headers:
            logger.debug('%-9s: %s', header, headers[header] )
        data = response.read()
        logger.debug('LENGTH   : %s', len(data) )
        logger.debug('DATA     :\n%s', data )
        logger.debug('RESPONSE :\n' )
        response = urllib2.urlopen( test_url + ':' + port )
        for line in response:
            logger.debug('  %s', line.rstrip() )
    
    ## NOTE: This is a client for the HTTP GET server from 12.2-BaseHTTPServer.py
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.4.2 Encoding Arguments")
        ## 12.4.2 Encoding Arguments
        # Arguments can be passed to the server by encoding them with urllib2.urlencode() and appending them to the url
        port = '8001'
        encoded_args = urllib.urlencode( chapter_sections[1] )
        logger.info( "Encoded: %s", encoded_args )
        url_with_args = test_url + ':' + port + '/?' +encoded_args
        logger.debug( "URL    : %s", url_with_args )
        logger.debug( "DATA   :\n%s", urllib2.urlopen( url_with_args ).read() )

    ## NOTE: This is a client for the HTTP POST server from 12.2-BaseHTTPServer.py
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.4.3 HTTP POST")
        ## 12.4.3 HTTP POST
        # to send form-encoded data to the remote server using POST instead of GET, pass the encoded query arguments as data to urlopen()
        port = '8002'
        encoded_args = urllib.urlencode( chapter_sections[2] )
        logger.info( urllib2.urlopen( test_url + ':' + port, encoded_args).read() )
        
    ## NOTE: This is a client for the HTTP GET server from 12.2-BaseHTTPServer.py
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.4.4 Adding Outgoing Headers" )
        ## 12.4.4 Adding Outgoing Headers
        # urlopen() is a convenience function that hides some details of how the request is made and handled
        # More precise control is possible by using a Request to instance directly.
        # For example, custom headers can be added to the outgoing request to:
            # control the format of the data returned,
            # specify the version of a document cached locally, and
            # tell the remote server the name of the software client communicating with it.
        # As the output from the earlir examples shows, the default User-agent header value is made up of the constant Python-urllib, 
        # followed by the Python interpreter version.
        # When creating an application that will access web resourcesowned by someone else, 
        # it is courteous to include real user-agent information in the requests, so the can identify the source of the hits more easily
        # Using a custom agent also allows them to control crawlers using a robots.txt file (see robotparser)
        port = '8001'
        request = urllib2.Request( test_url + ':' + port )
        request.add_header( 'User-agent', "12.4-urllib2.py - Subsection 12.4.4 Adding Outgoing Headers" )
        logger.debug( "DATA   :\n%s", urllib2.urlopen( request ).read() )
        
    ## NOTE: This is a client for the HTTP POST server from 12.2-BaseHTTPServer.py
    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("12.4.5 Posting Form Data from a Request" )
        ## 12.4.5 Posting Form Data from a Request
        # The outgoing form data can be added to the request to have it posted to the server
        port = '8002'
        request = urllib2.Request( test_url + ':' + port )
        logger.info( "Request method before adding data: %s", request.get_method() )
        # Careful, add_data() works like mode='w', not mode='a'
        request.add_data( urllib.urlencode( chapter_sections[4] ) )
        logger.info( "Request method after adding data : %s", request.get_method() )
        request.add_header( 'User-agent', "12.4-urllib2.py - Subsection 12.4.5 Posting Form Data from a Request" )
        logger.debug( "OUTGOING DATA  :\n%s", request.get_data() )
        logger.debug( "SERVER RESPONSE:\n%s", urllib2.urlopen( request ).read() )
     
    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("12.4.6 Uploading Files" )
        ## 12.4.6 Uploading Files
        # Encoding files for upload requires a little more work than simple forms
        # A complete MIME message needs to be constructed in the body of the request 
        # so that the server can distinguish incoming form fields from uploaded files.
        port = "8002"
        # Create a form with simple fields
        form = MultiPartForm()
        form.add_field('first_name', 'Abe')
        form.add_field('last_name', 'Froman')
        
        # Add a fake file
        form.add_file( 'fake', 'data/fake.txt', fileHandle=StringIO( 'Sausage King of Chicago' ) )
        
        # Build the request
        request = urllib2.Request( test_url + ':' + port )
        request.add_header( 'User-agent', "12.4-urllib2.py - Subsection 12.4.6 Uploading Files" )
        body = str(form)
        request.add_header( 'Content-type', form.get_content_type() )
        request.add_header( 'content-length', len(body) )
        request.add_data( body )
        
        logger.debug( "OUTGOING DATA  :\n%s", request.get_data() )
        logger.debug( "SERVER RESPONSE:\n%s", urllib2.urlopen( request ).read() )
        
        
        
    if results.section == 7 or results.section == 0:
        logger = logging.getLogger("12.4.7 Creating Custom Protocol Handlers" )
        ## 12.4.7 Creating Custom Protocol Handlers
        # urllib2 has built -in support for HTTP(S), FTP, and local file access.
        # To add support for other URL types, register another protocol handler.
        # For example, to support URLs pointing to arbitrary files on remote NFS servers,
        # create a class derived from BaseHandler and with a method nfs_open().
        # The protocol-specific open() method is given a single argument, the Request instance,
        # and should return an object with a read() method that can be used to read the data,
        # an info() method to return the response headers
        # and geturl() to return the actual URL of the file being read.
        # A simple way to achieve that result is to create an instance of urllib.addurlinfo,
        # passing the headers, URL, and open file handle into the constructor
        tempdir = tempfile.mkdtemp()
        try:
            # Populate the temp file for the simulation
            with open( os.path.join( tempdir, 'file.txt' ), 'wt' ) as f:
                f.write("Contents of file.txt")
                
            # Construct an opener with our NFS handler and register it as the default opener
            opener = urllib2.build_opener( FauxNFSHandler( tempdir ) )
            urllib2.install_opener(opener)
            
            # Open the file through a URL
            response = urllib2.urlopen( 'nfs://remote_server/path/to/the/file.txt' )
            logger.info( "READ CONTENTS: %s", response.read() )
            logger.info( "URL          : %s", response.geturl() )
            logger.info( "HEADERS      :" )
            for name, value in sorted( response.info().items() ):
                logger.debug("\t%-15s = %s", name, value)
            response.close()
        finally:
            os.remove( os.path.join( tempdir, 'file.txt' ) )
            os.removedirs( tempdir )
        
   
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
