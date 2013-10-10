from base64 import b64encode, b64decode

def encode_file( filename, out_filename ):
    with open( filename, 'r') as f:
        with open (out_filename, 'w') as of:
            of.write( b64encode( f.read() ))

def decode_file( filename ):
    with open( filename, 'r') as f:
        return b64decode( f.read() )


#encode_file( 'sample_text.py', 'coded_sample_text.txt' )
print decode_file( 'coded_sample_text.txt' )