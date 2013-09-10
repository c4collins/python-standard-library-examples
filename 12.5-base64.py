## 12.5 base64 - Encode Binary Data with ASCII
# The Base64, Base32, and Base26 encodings convert 8-bit bytes to values with 6,5, or 4 bits of useful data per byte,
# allowing non-ASCII bytes to be encoded as ASCII characteds for transmission over protocols that require plain ASCII, such as SMTP
# The base values correspond to the length of the alphabet used in each encoding.
# There are also URL-safe variations that use sightly different alphabets
import base64
import textwrap

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG, format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s", datefmt='%H:%M:%S', )

# Argument Parsing
import argparse
parser = argparse.ArgumentParser( description="Chapter 12 - The Internet - base64", add_help=True )
parser.add_argument( '--section','-s', action='store', type=int, dest='section', help="Enter the section number to see the results from that section.  i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.")
results = parser.parse_args()

## Classes

      
        
## Constants
chapter_sections = [ { 'filename' : __file__ }, 
                     { 'original_string' : "This is the data, in the clear." },
                     {}, 
                     { 'original_string' : "This is a string of unencrypted data" }, 
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.5.1 Base64 Encoding")
        ## 12.5.1 Base64 Encoding
        # Load this source file
        with open( chapter_sections[0]['filename'] , 'rt') as input:
            raw = input.read()
        encoded_data = base64.b64encode( raw )
        
        num_initial = len(raw)
        # There will never be more than 2 padding bytes
        padding = 3 - ( num_initial % 3 )
        
        logger.info( "%s bytes before encoding", num_initial )
        logger.info( "Expected %d padding bytes", padding )
        logger.info( "%s bytes after encoding", len(encoded_data) )
        logger.info( "Encoded data:\n%s", encoded_data )
        
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.5.2 Base64 Decoding")
        ## 12.5.2 Base64 Decoding
        # b64decode() converts the four bytes to the original three using a lookup table
        original_string = chapter_sections[1]['original_string']
        logger.info("Original: %s", original_string )
        
        encoded_string = base64.b64encode( original_string)
        logger.info("Encoded : %s", encoded_string )
        
        decoded_string = base64.b64decode( encoded_string )
        logger.info("Decoded : %s", decoded_string )
    
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.5.3 URL-Safe Variations")
        ## 12.5.3 URL-Safe Variations
        # The default Base64 alphabet includes . and /, which would cause problems if included in URLs
        # It's often necessary to use an alternate encoding with substitutes for these characters.
        
        encodes_with_pluses = chr(251) + chr(239)
        encodes_with_slashes = chr(255) * 2
        
        for original in [ encodes_with_pluses, encodes_with_slashes ]:
            logger.info( "Original          : %s", repr(original) )
            logger.info( "Standard Encoding : %s", base64.standard_b64encode( original ) )
            logger.info( "URL-safe Encoding : %s", base64.urlsafe_b64encode( original ) )
            
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.5.4 Other Encodings")
        ## 12.5.4 Other Encodings
        # The module also provides functions for working with Base32 and Base16 (hex) encoded data
        original_string = chapter_sections[3]['original_string']
        logger.info("Original       : %s", original_string )
        
        encoded_string = base64.b32encode( original_string)
        logger.info("Base32 Encoded : %s", encoded_string )
        
        decoded_string = base64.b32decode( encoded_string )
        logger.info("Decoded        : %s", decoded_string )
        
        original_string = chapter_sections[3]['original_string']
        logger.info("Original       : %s", original_string )
        
        encoded_string = base64.b16encode( original_string)
        logger.info("Base32 Encoded : %s", encoded_string )
        
        decoded_string = base64.b16decode( encoded_string )
        logger.info("Decoded        : %s", decoded_string )
   
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
