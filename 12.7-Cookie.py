## 12.7 Cookie - HTTP Cookies
# The Cookie module implements a parser for cookies that is mostly RFC2109 compliant.
# The implementation is a little less strict than the standard because MSIE 3.0x does not support the entire standard.
import Cookie
import datetime


# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - Cookie", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

## Functions

def show_cookie(c):
    logger = logging.getLogger("show_cookie()")
    logger.info("show_cookie(%s)", c)
    
    for key, morsel in c.iteritems():
        logger.info("Key = %s", morsel.key)
        logger.info("\tvalue       = %s", morsel.value)
        logger.info("\tcoded_value = %s", morsel.coded_value)
        for name in morsel.keys():
            if morsel[name]:
                logger.info( "\t%s = %s", name, morsel[name] )
      
        
## Constants
chapter_sections = [ {}, 
                     {}, 
                     {}, 
                     {}, 
                     {}, 
                     {},
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.7.1 Creating and Setting a Cookie")
        ## 12.7.1 Creating and Setting a Cookie
        # Cookies are used as state management for browser-based applications, ad as such, are usually set by the server to be stored and returend be the client
        # This is the simplest example of creating a cookie.
        c = Cookie.SimpleCookie()
        c['mycookie'] = "cookie_value"
        print c
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.7.2 Morsels")
        ## 12.7.2 Morsels
        # It is also possible to control other aspects of a cookie, such as the expiration, path, and domain.
        # All of the RFC attributes for cookies are manageable through the Morsel object representing the cookie value
        c = Cookie.SimpleCookie()
        
        # A cookie with a value that has to be encoded to fit in the header
        c['encoded_value_cookie'] = '"cookie_value"'
        c['encoded_value_cookie']['comment'] = "Value has escaped quotes"
        
        # A cookie that applies to onl part of a site
        c['restricted_cookie'] = "cookie_value"
        c['restricted_cookie']['path'] = "/sub/path"
        c['restricted_cookie']['domain'] = "PyStL"
        c['restricted_cookie']['secure'] = "True"
        
        # A cookie that expires in 5 minutes
        c['with_max_age'] = 'Expires in 5 minutes.'
        c['with_max_age']['max-age'] = 300 # seconds
                
        # A cookie that expires at a specific time        
        c['expires_at_time'] = "cookie_value"
        time_to_live = datetime.timedelta(hours=1)
        expires = datetime.datetime.now() + time_to_live
        
        expires_at_time = expires.strftime('%s, %d %b %Y %H:%M:%S')
        c['expires_at_time']['expires'] = expires_at_time
        
        show_cookie(c)
    
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.7.3 Encoded Values")
        ## 12.7.3 Encoded Values
        # The cookie header needs values to be be encoded so they can be properly parsed
        c = Cookie.SimpleCookie()
        c['integer'] = 5
        c['string_with_quotes'] = 'He said, "Hello, World!"'
        
        for name in ['integer', 'string_with_quotes']:
            logger.info( c[name].key )
            logger.info( "\t%s", c[name] )
            logger.info( "\tvalue       = %s", c[name].value )
            logger.info( "\tcoded_value = %s", c[name].coded_value )
        
        # Morsel.value is always the decoded version, while Morsel.coded_value is the representation to be used for transmission
        # Both values are always strings.
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.7.4 Receiving and Parsing Headers")
        ## 12.7.4 Receiving and Parsing Headers
        # Once the client receives the Set-Cookie headers, it will return those cookies to the server on subsequent requests using a Cookie header
        # An incoming Cookie header string may contain several string cookie values, separated by semi-colons
            # Cookie: integer=5; string_with_quotes:'"He said, \"Hello, World!\""'
        # Depending on the web server and framework, cookies are available directly from either the headers of theHTTP_COOKIE environment variable
        
        HTTP_COOKIE = '; '.join([ r'integer=5', r'string_with_quotes="He said, \"Hello, World!\""', ])
        
        c = Cookie.SimpleCookie(HTTP_COOKIE)
        logger.info("From constructor:\n%s", c)
        
        c = Cookie.SimpleCookie()
        c.load(HTTP_COOKIE)
        logger.info("From load()     :\n%s", c)
        
    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("12.7.5 Alternative Output Formats")
        ## 12.7.5 Alternative Output Formats
        # Besides using the Set-Cookie header, servers may deliver javaScript that adds cookies to a client.
        # SimpleCookie and Morsel provide JavaScript output via the js_output() method.
        c = Cookie.SimpleCookie()
        c['my_cookie'] = "cookie_value"
        c['another_cookie'] = "second value"
        logger.info( "JS Output: %s", c.js_output() )
    
    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("12.7.6 Deprecated Classes")
        ## 12.7.6 Deprecated Classes
        # All these examples have used Simplecookie.
        # The Cookie module also provides two other classes, SerialCookie and SmartCookie.
            # SerialCookie can handle any values that can be pickled
            # SmartCookie figures out whether a value needs to be unpickled if it it is a simple value.
        # These both use pickle and can therefore be riddled with security holes.
        # It's better to store the state on the server and give the client a session key instead.
   
   
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
