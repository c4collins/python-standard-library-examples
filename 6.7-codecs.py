# encoding:utf-8
## 6.7 codecs - String Encoding and Decoding
# The codecs module provides stream interfaces and file interfaces for transcoding data.
import codecs, binascii, sys, locale, glob, string, encodings
from cStringIO import StringIO

## 6.7.1 Unicode Primer

def to_hex(t, nbytes):
    """Format text t as a sequence of nbyte long values separated by spaces"""
    chars_per_item = nbytes*2
    hex_version = binascii.hexlify(t)
    return ' '.join(
        hex_version[ start : start + chars_per_item ]
        for start in xrange(0, len(hex_version), chars_per_item)
        )
        
print to_hex('abcdef', 1)
print to_hex('abcdef', 2)

text = u"pi: π"
print 'Raw   :', repr(text)
print 'UTF-8 :', to_hex(text.encode('utf-8'), 1)
print 'UTF-16:', to_hex(text.encode('utf-16'), 2)
print

# Given a sequence of encoded bytes as a str instance
# the decode() method translates them back to unicode
encoded = text.encode('utf-8')
decoded = encoded.decode('utf-8')

print 'Original:', repr(text)
print 'Encoded :', to_hex(encoded, 1), type(encoded)
print 'Decoded :', repr(decoded), type(decoded)
print

## 6.7.2 Working With Files
# the simplest interface provided by codecs is a replacement for open()
try:
    encoding = sys.argv[1]
except IndexError, err:
    encoding = 'utf-8'
filename = 'data/6.7-codecs-' + encoding + '.txt'

print 'Writing to', filename
with codecs.open(filename, mode='wt', encoding=encoding) as f:
    f.write(u'pi: \u03c0')

# Determine the byte grouping to use for to_hex()
nbytes = {  'utf-8' : 1,
            'utf-16': 2,
            'utf-32': 4,
         }.get(encoding, 1)

# Show the raw bytes in the file
print 'File contents:'
with open(filename, mode='r') as f:
    print to_hex(f.read(), nbytes)
print

print 'Reading from', filename
with codecs.open(filename, mode='r', encoding=encoding) as f:
    print repr(f.read())
    
## 6.7.3 Byte Order
# codecs defines constants for byte-order markers to assist with comprehending endianess

for name in [ 'BOM', 'BOM_BE', 'BOM_LE',
              'BOM_UTF8',
              'BOM_UTF16', 'BOM_UTF16_BE', 'BOM_UTF16_LE',
              'BOM_UTF32', 'BOM_UTF32_BE', 'BOM_UTF32_LE',
            ]:
    print '{:12} : {}'.format(name, to_hex(getattr(codecs, name), 2))
print    
# ordering can be specified when encoding, like so:
# pick the non-native version of UTF-16 encoding
if codecs.BOM_UTF16 == codecs.BOM_UTF16_BE:
    bom = codecs.BOM_UTF16_LE
    encoding = 'utf_16_le'
else:
    bom = codecs.BOM_UTF16_BE
    encoding = 'utf_16_be'

print 'Native order  :', to_hex(codecs.BOM_UTF16, 2)
print 'Selected order:', to_hex(bom, 2)
print

# Encode the text
encoded_text = u'pi: \u03c0'.encode(encoding)
print '{:14} : {}'.format(encoding, to_hex(encoded_text, 2))

with open('data/6.7-nonnative-encoding.txt', mode='wb') as f:
    f.write(bom)
    f.write(encoded_text)
print

# Look at the raw data
with open('data/6.7-nonnative-encoding.txt', mode='rb') as f:
    raw_bytes = f.read()
print 'Raw   :', to_hex(raw_bytes, 2)

# reopen the file and let codecs detect the BOM
with codecs.open('data/6.7-nonnative-encoding.txt', 
                mode='rt',
                encoding='utf-16',
) as f:
    decoded_text = f.read()
print 'Decoded:', repr(decoded_text)
print

## 6.7.4 Error Handling
# codecs uses five error-handling options
    # strict - Raises an exception if data cannot be converted
    # replace - Substitutes a marker for data that cannot be converted
    # ignore - Skips the data that cannot be converted
    # xmlcharrefreplace - XML characted (encoding only)
    # backslashreplace - Escape sequence (encoding only)
    
# The most common error encountered is UnicodeEncodeError when writing Unicode data to an ASCII output stream
error_handling = sys.argv[2]
text =u'pi: \u03c0'

try:
    with codecs.open('data/6.7-encode_error.txt', 'w', encoding='ascii', errors=error_handling) as f:
        f.write(text)
except UnicodeEncodeError, err:
    print 'ERROR:', err
else:
    with open('data/6.7-encode_error.txt', 'rb') as f:
        print 'File contents:', repr(f.read())
        
# It's also possible to get errors while decoding as well
# especially if the encoding was done improperly
print 'Original:', repr(text)

with codecs.open('data/6.7-decode_error.txt', 'w', encoding='utf-16') as f:
    f.write(text)

with open('data/6.7-decode_error.txt', 'rb') as f:
    print 'File contents:', to_hex(f.read(), 1)

with codecs.open('data/6.7-decode_error.txt', 'r', encoding='utf-8', errors=error_handling) as f:
    try:
        data = f.read()
    except UnicodeDecodeError, err:
        print 'ERROR:', err
    else:
        print 'Read  :', repr(data)
print
      
## 6.7.5 Standard Input and Output Streams
# UnicodeEncodeError happens when outputting to console or pipeline 
# when sys.stdout is not configured with an encoding
print 'Default encoding:', sys.stdout.encoding
print 'TTY:', sys.stdout.isatty()
try:
    print text
except UnicodeEncodeError, err:
    print err, "==>: You must explicitly specify the encoding in order to pipe this output"
print
  
# To configure that encoding, use getwriter()
# Wrap sys.stdout with a writer than knows how to handle encoding
wrapped_stdout = codecs.getwriter('UTF-8')(sys.stdout)
wrapped_stdout.write(u'Via write: ' + text + '\n')
# replace stdout with a writer
oldsys = sys.stdout # save for later
sys.stdout = wrapped_stdout
print u'Via print:', text
print

# but why specify the encoding when you could just use locale to figure it out?
# configure locale from the user's environment settings
sys.stdout = oldsys # reset the sys.stdout
locale.setlocale(locale.LC_ALL, '')

# wrap stdout with an encoding-aware writer
lang, encoding = locale.getdefaultlocale()
print 'Locale encoding    :', encoding
sys.stdout = codecs.getwriter(encoding)(sys.stdout)

try:
    print 'With wrapped stdout:', text
except UnicodeDecodeError, err:
    print "Oh, shi-", err
print

# this also needs to be done for sys.stdin
sys.stdout = oldsys # reset the sys.stdout
locale.setlocale(locale.LC_ALL, '')

# wrap stdin with an encoding-aware writer
lang, encoding = locale.getdefaultlocale()
sys.stdin = codecs.getwriter(encoding)(sys.stdin)

print 'From stdin:'
lorem = repr(sys.stdin.read())
print lorem
print

## 6.7.6 Encoding Translation
# Sometimes it's useful to be able to change a file's encoding without holding the data
# EncodedFile() takes an open file handle and wraps it in a class to translate it to another encoding as the I/O occurs

# this is u'pi: \u03c0' from above
data = text

# Manually encode that as utf-8
utf8 = data.encode('utf-8')
print 'Start as UTF-8   :', to_hex(utf8, 1)

# Set up an output buffer, then wrap it with EncodedFile()
output = StringIO()
encoded_file = codecs.EncodedFile( output, 
                                   data_encoding = 'utf-8', 
                                   file_encoding = 'utf-16',
                                   )
encoded_file.write( utf8 )

# Fetch the buffer contents (as utf-16 a encoded string)
utf16 = output.getvalue()
print 'Encoded to UTF-16:', to_hex(utf16, 2)

# Set up another buffer with the utf-16 data for reading,
# and wrap that in another EncodedFile()
buffer = StringIO(utf16)
encoded_file = codecs.EncodedFile( buffer, 
                                   data_encoding='utf-8', 
                                   file_encoding='utf-16',
                                   )

# read the utf-8 encoded version of the data
recoded = encoded_file.read()
print 'Back to UTF-8    :', to_hex( recoded, 1 )
print

## 6.7.7. Non-Unicode Encodings
# codecs can also work with base-64, bzip2, ROT-13, ZIP, and other formats
buffer = StringIO()
stream = codecs.getwriter('rot_13')(buffer)

text = 'abcdefghijklmnopqrstuvwxyz'

stream.write(text)
stream.flush()

print 'Original:', text
print 'ROT-13  :', buffer.getvalue()
print

# Using codecs is easier than working directly with zlib
buffer = StringIO()
stream = codecs.getwriter('zlib')(buffer)

text = (text + '\n')
repetitions = 50

stream.write(text * repetitions)
stream.flush()

print 'Original length  :', len(text * repetitions)
compressed_data = buffer.getvalue()
print 'ZIP compressed   :', len(compressed_data)

buffer = StringIO(compressed_data)
stream = codecs.getreader('zlib')(buffer)

first_line = stream.readline()
print 'Read first line  :', repr(first_line)

uncompressed_data = first_line + stream.read()
print 'Uncompressed     :', len(uncompressed_data)
print 'Are they the same:', text * repetitions == uncompressed_data
print

## 6.7.8 Incremental Encoding
# For large data sets, it's better to use incremental changes,
# especially when the length of the data is dramatically changed,
# such as with zlib and bz2
# codecs includes IncrementalEncoder and IncrementalDecoder for this purpose

print 'Text length :', len(text)
print 'Repetitions :', repetitions
print 'Expected len:', len(text) * repetitions
print

# Encode the text several times to build up a large amount of data
encoder = codecs.getincrementalencoder('bz2')()
encoded = []
print 'Encoding:',
for i in xrange( repetitions ):
    en_c = encoder.encode( text, final=( i == repetitions - 1 ) )
    if en_c:
        print '\nEncoded : {} bytes'.format( len( en_c ) )
        encoded.append(en_c)
    else:
        sys.stdout.write('.')
print

bytes = ''.join(encoded)
print 'Total encoded length:', len(bytes)
print

# Decode the byte string one byte at a time
decoder = codecs.getincrementaldecoder('bz2')()
decoded = []

print 'Decoding:',
for i, b in enumerate(bytes):
    # final will be set to true when the last bit of data is passed in
    # and the codec then knows to flush any remaining buffered data.
    final= ( i + 1) == len(text)
    c = decoder.decode(b, final)
    if c:
        print '\nDecoded : {} characters'.format( len( c ) )
        print 'Decoding:',
        decoded.append(c)
    else:
        sys.stdout.write('.')
print

restored = u''.join(decoded)
print

print 'Total uncompressed length:', len(restored)
print

## 6.7.9 Unicode data and Network Communication
print 'See', glob.glob('6.7.9-*.py')[0], 'for 6.7.9 Unicode Data and Network Communication'
print

## 6.7.10 Defining a Custom Encoding
# This will probably not ever be necessary because of all the encodings that come with Python
# but it might be fun to do sometime.
def invertcaps(text):
    """return a new string with all the case of the letters swapped"""
    return ''.join( 
        c.upper() 
            if c in string.ascii_lowercase
        else c.lower() 
            if c in string.ascii_uppercase
        else c
        for c in text
        )
        

print invertcaps( repr( lorem ) )
print invertcaps( repr( lorem ) )
print invertcaps('ABC.def')
print invertcaps('abc.DEF')
print
    
# but that is inefficient.
# codecs allows for the creation of decoding and encoding character maps

# Map every character to itself
decoding_map = codecs.make_identity_dict( xrange(256) )

# Make a list of pairs of ordinal values for all lcase and ucase letters
pairs = zip( [ord(c) for c in string.ascii_lowercase],
             [ord(c) for c in string.ascii_uppercase] )

# modify the mapping to convert upper to lower and lower to upper
decoding_map.update( dict( (upper, lower) for (lower, upper) in pairs ) )
decoding_map.update( dict( (lower, upper) for (lower, upper) in pairs ) )

# Create a separate encoding map
encoding_map = codecs.make_encoding_map( decoding_map )

print (codecs.charmap_encode('abc.DEF', error_handling, encoding_map)) 
print (codecs.charmap_decode('abc.DEF', error_handling, decoding_map)) 
print encoding_map == decoding_map
print

# by default, char map encoders and decoders support the standard error methods
# since this charmap only includes [a-zA-Z], the u"pi: π" from earlier fails    
for error in ['ignore', 'replace', 'strict']:
    try:
        encoded = codecs.charmap_encode(data, error, encoding_map)
    except UnicodeEncodeError, err:
        encoded = str(err)
    print '{:7} {}'.format(error, encoded)
print

# After defining a en/decoding maps, a few additonal classes have to be set up
# and the encoding should be registered so codecs can locate it.
# The search function should take a string of the name of the encoding and return either the CodecInfo object or None
def search1(encoding):
    print 'search1: Searching for', encoding
    return None
    
def search2(encoding):
    print 'search2: Searching for', encoding
    return None
    
codecs.register(search1)
codecs.register(search2)

utf8 = codecs.lookup('utf-8')

try:
    unknown = codecs.lookup('no-such-encoding')
except LookupError, error:
    print 'ERROR:', error
print  
# multiple search functions can be registered, and they'll all run in order until a match is found

# The CodecInfo instance returned by the search function tells the codec what to do.
# There are a number of required classes that codecs provided the bases for

# Stateless encoder / decoder
class InvertCapsCodec(codecs.Codec):
    def encode(self, input, errors=error_handling):
        return codecs.charmap_encode(input, errors, encoding_map)
    
    def decode(self, input, errors=error_handling):
        return codecs.charmap_decode(input, errors, decoding_map)
        
# Incremental forms
class InvertCapsIncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        data, nbytes = codecs.charmap_encode(input, self.errors, encoding_map)
        return data
class InvertCapsIncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        data, nbytes = codecs.charmap_decode(input, self.errors, decoding_map)
        return data
        
# Stream reader & writer
class InvertCapsStreamReader(InvertCapsCodec, codecs.StreamReader):
    pass
class InvertCapsStreamWriter(InvertCapsCodec, codecs.StreamWriter):
    pass

# Register the search function
def find_invertcaps(encoding):
    """return the codec for 'invertcaps'"""
    if encoding == 'invertcaps':
        return codecs.CodecInfo(
            name = 'invertcaps',
            encode = InvertCapsCodec().encode,
            decode = InvertCapsCodec().decode,
            incrementalencoder = InvertCapsIncrementalEncoder,
            incrementaldecoder = InvertCapsIncrementalDecoder,
            streamreader = InvertCapsStreamReader,
            streamwriter = InvertCapsStreamWriter,
            )
    return None
    
codecs.register(find_invertcaps)

# Stateless encoder/decoder
text = 'abc.DEF'
encoder = codecs.getencoder('invertcaps')
encoded_text, consumed = encoder(text)
print "Encoded '{}' to '{}', consuming {} characters".format(text, encoded_text, consumed)

# Stream writer
writer = codecs.getwriter('invertcaps')(sys.stdout)
print 'StreamWriter for stdout: ', writer.write(text)

# Incremental decoder
decoder_factory = codecs.getincrementaldecoder('invertcaps')
decoder = decoder_factory()
decoded_text_parts = []
for c in encoded_text:
    decoded_text_parts.append( decoder.decode( c, final=False ) )
decoded_text_parts.append( decoder.decode( '', final=True ) )
decoded_text = ''.join( decoded_text_parts )
print "IncrementalDecoder converted '{}' to '{}'".format(encoded_text, decoded_text)
print
