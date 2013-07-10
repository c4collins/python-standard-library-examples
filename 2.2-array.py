## Array -  Sequence of Fixed-Type Data
 # It's a list that's restricted to a single datatype
 # which is setup when the array is created
   
 # 'c' -> character
 # 'f' -> float
 # 'i' -> integer
 # 'I' -> long
 # 'u' -> unicode char
 # more options at: http://docs.python.org/2/library/array.html

import array, binascii, tempfile, os

s = "This is the array."
a = array.array('c', s)

print 'As string:', s
print 'As array :', a
print 'As hex   :', binascii.hexlify(a)
 # most of the list functions work on arrays as well
a = array.array('i', xrange(4))
print 'Initial :', a
a.extend(xrange(3))
print 'Extended:', a
print 'Slice   :', a[2:5]
print 'Iterator:'
print list(enumerate(a))
print
 # write/read arrays to/from files
a = array.array('i', xrange(5))
print 'A1:', a

  # write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile(delete=False)
a.tofile(output.file) # must be an actual file
output.flush()

    #read the raw data
with open(output.name, 'rb') as input:
    raw_data = input.read()
    print 'Raw Contents:', binascii.hexlify(raw_data)

    # read the data lines into an array
    input.seek(0)
    a2 = array.array('i')
    a2.fromfile(input, len(a))
    print 'A2:', a2
print
 # Arrays make it easy to change the byte order (I'm big-endian due to being a network guy)
def to_hex(a):
    chars_per_item = a.itemsize * 2 # 2 hex digits
    hex_version = binascii.hexlify(a)
    num_chunks = len(hex_version) / chars_per_item
    for i in xrange(num_chunks):
        start = i*chars_per_item
        end = start + chars_per_item
        yield hex_version[start:end]
a1 = array.array('i', xrange(5))
a2 = array.array('i', xrange(5))
a2.byteswap()
fmt = '%10s %10s %10s %10s'
print fmt % ('A1 hex', 'A1', 'A2 hex', 'A2')
print fmt % (('~' * 10,) * 4)
for values in zip(to_hex(a1), a1, to_hex(a2), a2):
    print fmt % values


