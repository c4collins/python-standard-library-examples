## 12.8 uuid - Universally Unique Identifiers
# RFC 4122 defines a system for creating universally unique identifiers for resources in a way that does not require a central registrar.
# UUID values are 128 bits long and as the reference guide says
    # "can guarantee uniqueness across space and time."
# They are useful for generating identifiers for documents, hosts, application clients, and other situations here a unique value is necessary.
# The RFC is specifically focussed on creating a Uniform Resource Name namespace and covers three main algorithms:
    # Using IEEE 802 MAC addresses as a source of uniqueness
    # Using pseudorandom numbers
    # Using well-known strings combined with cryptogtapic hashing
# In all cases the seed value is combined with the system clock and a clock sequence value used to maintain uniqueness in case the clock is set backwards.
import uuid

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 12 - The Internet - uuid", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = argparser.parse_args()

## Functions
def log_uuid( u, logger ):
    logger.info( u )
    logger.info( type(u) )
    logger.info( "bytes     : %s", repr(u.bytes) )
    logger.info( "hex       : %s", u.hex )
    logger.info( "int       : %s", u.int )
    logger.info( "urn       : %s", u.urn )
    logger.info( "variant   : %s", u.variant )
    logger.info( "version   : %s", u.version )
    logger.info( "fields    : %s", u.fields )
    logger.info( "\ttime_low            : %s", u.time_low )
    logger.info( "\ttime_mid            : %s", u.time_mid )
    logger.info( "\ttime_hi_version     : %s", u.time_hi_version )
    logger.info( "\tclock_seq_hi_variant: %s", u.clock_seq_hi_variant )
    logger.info( "\tclock_seq_low       : %s", u.clock_seq_low )
    logger.info( "\tnode                : %s", u.node )
    logger.info( "\ttime                : %s", u.time )
    logger.info( "\tclock_seq           : %s", u.clock_seq )
    return

def show_uuid_list( msg, l, logger):
    logger.info("Message: %s", msg)
    for v in l:
        logger.info("\t: %s", v)

    
## Constants
chapter_sections = [ {}, 
                     { 
                        'hostnames':['192.168.1.160', '192.168.1.160:8001'], 
                        'namespace_types':( n for n in dir(uuid) if n.startswith("NAMESPACE_") ),
                    }, 
                     {}, 
                     { 'input_values': 
                        [ 
                            "urn:uuid:f2f84497-b3bf-493a-bba9-7c68e6def80b",
                            "{417a5ebb-01f7-4ed5-aeac-3d56cd5037b0}",
                            "2115773a-5bf1-11dd-ab48-011ec200d9e0",
                        ]
                     }, 
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.8.1 UUID 1 - IEEE 802 MAC Address")
        ## 12.8.1 UUID 1 - IEEE 802 MAC Address
        # UUID version 1 values are computed using the MAC address of the host.
        # The uuid module uses getnode() to retrieve the MAC value of he current system
        
        logger.info( hex( uuid.getnode() ) )
        # if the host has multiple MAC addresses (multiple NICs) an of them can be returned
        
        # To generate the uuid of a host, identified by MAC address, using uuid1()
        # The node identifier is optional; leave the field blank to used the value ruturned by getnode()
        log_uuid( uuid.uuid1(), logger )
        
        # since the time component is different each time, each call to uuid1() returns a different value
        for i in xrange(5):
            logger.info("UUID : %s", uuid.uuid1() )
            
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.8.2 UUID 3 and 5 - Name-Based Values")
        ## 12.8.2 UUID 3 and 5 - Name-Based Values
        # It is also useful in some contexts to create UUID values form names instead of random or time-based values.
        # Versions 3 and 5 of the UUID specification use cryptographic hash values( MD5 and SHA-1, respectively)
        # to combine namespace-specific seed values with names.
        # There are several well-known namespaces, identified by predefined UUID values
        # for working with DNS, URLs, ISO OIDs, and X.500 Distinguished Names.
        # New application specific namespaces can be defined by generating and saving UUID values.

        # To create a UUID from a DNS name (or simple IP) pass uuid.NAMESPACE_DNS as the namespace argument
        for name in chapter_sections[1]['hostnames']:
            logger.info( name )
            logger.info( "MD5  : %s", uuid.uuid3( uuid.NAMESPACE_DNS, name ) )
            logger.info( "SHA-1: %s", uuid.uuid5( uuid.NAMESPACE_DNS, name ) )
   
        # The UUID for a given name in a namespace is always the same no matter when or where it is calculated
        for namespace_type in sorted( chapter_sections[1]['namespace_types'] ):
            logger.info( "namespace_type : %s", namespace_type )
            namespace_uuid = getattr(uuid, namespace_type)
            logger.info( "\t %s", uuid.uuid3( namespace_uuid, chapter_sections[1]['hostnames'][0] ) )
            logger.info( "\t %s", uuid.uuid3( namespace_uuid, chapter_sections[1]['hostnames'][0] ) )
            
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.8.3 UUID 4 - Random Values")
        ## 12.8.3 UUID 4 - Random Values
        # Sometimes, host-based and namespace-based UUID values are not 'different enough'
        # For example, in case where UUID is intended to be used as a hash key, as more random sequence of values with more differentiation is desireable to avoid collisions in the hash table.
        # Having values with fewer common digis also makes it easier to find them in log files
        # To add greater differentiation in UUIDs, use uuid4() to generate them using random input values
        
        for i in xrange(4):
            logger.info( uuid.uuid4() ) 
            
        # The source of the randomness depends on the available C libraries when uuid is imported
        # If libuuid or uuid.dll can be loadedand contains a function for generating random values it is used
        # otherwise, os.urandom() or the random module are used.
        
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.8.4 Working with UUID Objects")
        ## 12.8.4 Working with UUID Objects
        # In addition to generating new UUID values, it is possible to parse strings in standard formats to create UUID objects, 
        # making it easier to handle comparisons and sorting operations
        show_uuid_list( 'input values      :', chapter_sections[3]['input_values'], logger)
        
        uuids = [ uuid.UUID(s) for s in chapter_sections[3]['input_values'] ]
        show_uuid_list( 'converted to uuids:', uuids, logger)
        
        uuids.sort()
        show_uuid_list( 'Sorted:           :', uuids, logger)
        
        
        
        
        
            
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)