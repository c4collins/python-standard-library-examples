## hmac!
 # The HMAC algorithm is used to verify the integrity of messages passed between
 # applications or stored in potentially vulnerable locations.

import hmac, hashlib, base64, pprint
from StringIO import StringIO

try:
    import cPickle as pickle
except:
    import pickle

digest_maker = hmac.new('secret-shared=key-goes-here')

with open('data/lorem.txt', 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)

digest = digest_maker.hexdigest()
print '          MD5 digest:', digest

 # of course, SHA-1 is preferred over MD5
 # the new() method takes three arguments
     # 1) The secret key
     # 2) An initial message, or very small complete message
     # 3) digest module to use, MD5 is the default

digest_maker = hmac.new('secret-shared-key-goes-here',
                        '',
                        hashlib.sha1)

with open('data/lorem.txt', 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)

digest = digest_maker.hexdigest()
print '         SHA1 digest:', digest

 # sometimes, the base63 encoded binary digest is required, rather than the hexdigest

with open('data/lorem.txt', 'rb') as f:
    body = f.read()

hash = hmac.new('secret-shared-key-goes-here', body, hashlib.sha1)
digest = hash.digest()
print 'Base64 binary digest:', base64.encodestring(digest)

## Applications of Message Signatures

def make_digest(message):
    """Return a digest for the message"""
    hash = hmac.new('secret-shared-key-goes-here',
                    message,
                    hashlib.sha1)
    return hash.hexdigest()

class SimpleObject(object):
    """A very simple class to demonstrate checking digests before unpickling"""
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

 # Simulate a wriatble socket or pipe with StringIO
out_s = StringIO()

 # write a valid object to the stream
     # digest\nlength\npickle
o = SimpleObject('Digest matches')
pickled_data = pickle.dumps(o)
digest = make_digest(pickled_data)
header = '%s %s' % (digest, len(pickled_data))
print '\nWRITING:', header
out_s.write(header + '\n' )
out_s.write(pickled_data)

 # write an invalid object to the stream
o = SimpleObject('digest does not match')
pickled_data = pickle.dumps(o)
digest = make_digest('this is not the pickled data at all')
header = '%s %s' % (digest, len(pickled_data))
print '\nWRITING:', header
out_s.write(header + '\n' )
out_s.write(pickled_data)

out_s.flush()

 # Simulate a readable socket or pipe with StringIO
in_s = StringIO(out_s.getvalue())

# Read the data
while True:
    first_line = in_s.readline()
    if not first_line:
        break
    incoming_digest, incoming_length = first_line.split(' ')
    incoming_length = int(incoming_length)
    print '\nREAD:', incoming_digest, incoming_length

    incoming_pickled_data = in_s.read(incoming_length)
    actual_digest = make_digest(incoming_pickled_data)
    print 'ACTUAL:', actual_digest

    if incoming_digest != actual_digest:
        print 'WARNING: Data corruption'
    else:
        obj = pickle.loads(incoming_pickled_data)
        print 'OK:', obj
        
    
