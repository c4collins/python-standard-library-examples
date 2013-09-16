# encoding:utf-8
## 12.9 json -JavaScript Object Notation
# The json module provides an API similar ot pickle for converting in-memory Python objects to a serialize representation known as Javascript Object Notation.
# Unlike pickle, JOSN has the benefit of having implementations in many languages.
# It is most widely used forcommunicating between the web server and the client in an AJAX application
# but it is also useful for other inter-application communication needs
import json
try:
    from cStringIO import StringIO
except:
    from  StringIO import StringIO

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
    def __init__(self, s):
        self.s =  s
    def __repr__(self):
        return "<MyObj(%s)>" % self.s
        
class MyEncoder( json.JSONEncoder ):
    logger = logging.getLogger("MyEncoder")
    def default( self, obj ):
        self.logger.info( "default(%s)", repr(obj) )
        return convert_to_builtin_type( obj )

class MyDecoder( json.JSONDecoder ):
    logger = logging.getLogger("MyDecoder")
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)
    def dict_to_object(self, d):
        return dict_to_object(d)
        
## Functions
def convert_to_builtin_type(obj):
    """Converts an unknown type object to a known type object for json.dumps()-ing.
        It doesn't do any encoding, just simply converts one object to another.
    """
    logger = logging.getLogger("convert_to_builtin_type")
    logger.info("default(%s)", repr(obj))
    # convert objects to a dictionary of their representation
    d = { 
        '__class__' :obj.__class__.__name__,
        '__module__':obj.__module__,
    }
    d.update(obj.__dict__)
    return d

def dict_to_object(d):
    """Creates a new object from the information in the dictionary provided (__class__, __module__, and any args)"""
    logger = logging.getLogger("dict_to_object")
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        logger.debug("MODULE: %s", module.__name__)
        class_ = getattr(module, class_name)
        logger.debug(" CLASS: %s", class_ )
        # Since the json module converts string values to unicode objects, 
        # they need to be reencoded as ASCII strings before they can be used as keyword arguments to the class constructor.
        args = dict( (key.encode('ascii'), value) for key, value in d.items() )
        logger.debug("  ARGS: %s", args )
        inst = class_(**args)
    else:
        inst = d
    return inst
    
def get_decoded_and_remainder( input_data ):
    obj, end = decoder.raw_decode( input_data )
    remaining = input_data[end:]
    return (obj, end, remaining)
    
## Constants
chapter_sections = [ { 'data':[{ 'a':"A", 'b':(2,4), 'c':3.0 }], }, 
                     { 'data':[{ 'h':"H", 'b':(1,1,2,3,5,8,13,21,44,65), 'c':3.14159 }], },  
                     { 'data':[{ 'x':"X", 'y':(44,65), 'z':86.911, ('q',):"Q Tuple" }], }, 
                     {},
                     { 'data':[{ 'p':"qrstuv", 'n':(109,174), 'o':19.86, }], }, 
                     { 'data':[{'a':'A','b':[2,4],'c':3.0,}], 'load':'[{"a": "A", "c": 3.0, "b": [2, 4]}]', }, 
                     { 'data':'[{"a": "A", "c": 3.0, "b": [2, 4]}]', }, 
                    
]
        
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):   
    
    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("12.9.1 Encoding and Decoding Simple Data Types")
        ## 12.9.1 Encoding and Decoding Simple Data Types
        # The encoder understands Python's native types by default (string, unicode, int, float, tuple, list, and dict)
        data = chapter_sections[0]['data']
        logger.info( "DATA    : %s", data )
        data_string = json.dumps( data )
        logger.info( "ENCODED : %s", json.dumps( data_string ) )
        decoded = json.loads( data_string )
        logger.info( "DECODED : %s", decoded )
        # But encoding and recoding sometimes will give different types of objects
        # In particular, strings are converted to unicpode objects, and tuples become lists
        logger.info( "ORIGINAL: %s", type(data[0]['b']) )
        logger.info( "DECODED : %s", type(decoded[0]['b']) )
    
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("12.9.2 Human Consumable vs. Compact Output")
        ## 12.9.2 Human Consumable vs. Compact Output
        # Another benefit of JSON over pickle is that the results are human-readable.
        # The dumps() function accepts several arguments to make the code even nicer.
        
        # For example, the sort_keys flag tells the encoder to output the keys of the dictionary in sorted instead of random order.
        data = chapter_sections[1]['data']
        logger.info( "DATA          : %s", data ) 
        unsorted = json.dumps(data)        
        logger.info( "UNSORTED      : %s", unsorted )
        sorted = json.dumps(data, sort_keys=True) 
        logger.info( "  SORTED      : %s", sorted ) 
        
        # Sorting makes it easier to scan by eye, but also easier to compare
        logger.info( "UNSORTED MATCH: %s", unsorted == sorted )
        logger.info( "  SORTED MATCH: %s", sorted == json.dumps(data, sort_keys=True))
        
        # For highly nested data structures, specify a value for indent so the output is formatted nicely as well.
        with_indent = json.dumps(data, sort_keys=True, indent=2)
        logger.info( "WITH INDENT   : %s", with_indent )
        # Of course, a longer output means more data to transmit.
        
        # On the other hand, by adjusting settings for separating data it's possible to make your output more compact than the default
        logger.info( "data length   : %d", len( repr(data) ) )
        logger.info( "dumps length  : %d", len( unsorted ) )
        logger.info( "indent length : %d", len( with_indent ) )
        with_separators = json.dumps(data, separators=(",",":")) # The default is (", ",": ") so this removes whitespace
        logger.info( "data length   : %d", len( with_separators ) )
    
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("12.9.3 Encoding Dictionaries")
        ## 12.9.3 Encoding Dictionaries
        # The JSON format expects the keys to a dictionary to be strings.
        # Trying to encode a dictionary with non-string types as keys produces an exception.
        # One way to work around that limitation is to tell the encoder to skip non-string keys using the skipkeys argument
        data = chapter_sections[2]['data']
        logger.debug( "First Attempt:" )
        try:
            logger.info( json.dumps(data) )
        except (TypeError, ValueError), err:
            logger.error( err )
            
        logger.debug( "Second Attempt:" )
        logger.info( json.dumps(data, skipkeys=True) )
    
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("12.9.4 Working with Custom Types")
        ## 12.9.4 Working with Custom Types
        # All of the examples so far have used Python's built-in types because those are supported by json natively
        # It is common to need to encode custom classes as well, and there are two ways to do so.
        obj = MyObj("This is the instance value.")
        
        logger.debug( "First Attempt:" )
        try:
            logger.info( json.dumps(obj) )
        except (TypeError, ValueError), err:
            logger.error( err )
        
        retyped = json.dumps(obj, default=convert_to_builtin_type)
        logger.debug( "With Default: %s", retyped )
        # This way, the objects are broken down into json.dumps()-able parts with enough information to reconstruct the object
        # ( If access is given to the original Python objects (or compatible others, like a JS object) )
        
        # To decode the results and create a MyObj() instance, use the object_hook argument to loads() to tie in the decoder,
        # so the class can be imported from the module and used to create the instance.
        # The object_hook is called for each dictionary decoded from the incoming data stream, 
        # providing a chance to convert the dictionary to another type of object.
        # The hook function should return the object the calling application should receive instead of the dictionary.
        myobj_instance = json.loads( retyped, object_hook=dict_to_object )
        logger.info( "MyObj Instance: %s", myobj_instance )
        # Similar hooks are available for the built in types:
            # integers               = parse_int
            # floating-point numbers = parse_float
            # constants              = parse_constant
    
    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("12.9.5 Encoder and Decoder Classes")
        ## 12.9.5 Encoder and Decoder Classes
        # The json module provides classes for encoding and decoding.
        # Using the classes directly gives access to extra APIs for customizing their behaviour
        # The JSONEncoder uses an iterable interface for producing chunks of encoded data,
        # making it easier to write to files or network sockets without having to represent an entire data structure in memory.
        encoder = json.JSONEncoder()
        data = chapter_sections[4]['data']
        
        # The output is generated in logical units instead of being based on a size value.
        for part in encoder.iterencode( data ):
            logger.info( "PART: %s", part )
            
        # The encode) mehod is basically equivalent to the value produced by the expression
            # ' '.join( encoder.iterencode() )
        # with some extra error checking up front
        
        # To encode arbitrary objects, override the default() method with an implementation similar to the one used in convert_to_builtin_type()
        obj = MyObj('internal data')
        logger.info( obj )
        encoded = MyEncoder().encode(obj) 
        logger.info( encoded )
        
        # Decoding text, and then converting the dictionary into a n object takes a little more work to set up, but not much
        decoded = MyDecoder().decode( encoded )
        logger.info( decoded )
    
    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("12.9.6 Working with Streams and Files")
        ## 12.9.6 Working with Streams and Files
        # With large data structures, it may be preferable to write encodings directly to a file-like object.
        # The convenience functions load() and dump() accept references to file-like objects to use for reading or writing
        f = StringIO()
        data = chapter_sections[5]['data']
        json.dump( data, f )
        logger.info( f.getvalue() )
        
        # Although not optimized to read only part of the data at a time,
        # the load() function offers the benefit of encapsulating the logic of generating objects from stream input.
        f = StringIO( chapter_sections[5]['load'] ) 
        logger.info( json.load(f) )
    
    if results.section == 7 or results.section == 0:
        logger = logging.getLogger("12.9.7 Mixed Data Streams")
        ## 12.9.7 Mixed Data Streams
        # JSONDecoder includes raw_decode(), a method for decoding a data structure followed by more data,
        # such as JSON data with trailing text.
        # The return value is the object created by decoding the input data and an index into that data indicating where decoding left off
        decoder = json.JSONDecoder()
        encoded_object = chapter_sections[6]['data']
        extra_text = "This text is not part of the JSON."
        
        logger.info( "JSON First:" )
        data = ' '.join( [encoded_object, extra_text] )
        obj, end, remaining = get_decoded_and_remainder(data)
        
        logger.info( "Object             : %s", obj )
        logger.info( "End of parsed input: %s", end )
        logger.info( "Remaining          : %s", remaining )
        
        logger.info( "JSON Embedded:" )
        try:
            data = " ".join([ extra_text, encoded_object, extra_text ])
            obj, end, remaining = get_decoded_and_remainder(data)
        except ValueError, err:
            logger.error( err )
        
        
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)