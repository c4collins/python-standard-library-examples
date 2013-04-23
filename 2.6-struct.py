## struct
 # struct is used to convert between binary and string types
 # there are functions for doing struct things, but generally it's more efficient
 # to make a Struct object and use its methods instead

import struct, binascii, ctypes, array

values = [1, 'ab', 2.7]
s = struct.Struct('I 2s f')
endianess = [
    ('@', 'native, native'),
    ('=', 'native, standard'),
    ('<', 'little-endian'),
    ('>', 'big-endian'),
    ('!', 'network'),
    ]
packed_data = s.pack(*values)

print 'Original values:', values
print 'Format String  :', s.format
print 'Uses           :', s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)
print 'Unpacked Value :', s.unpack(packed_data) 
for code, name in endianess:
    s = struct.Struct(code + ' I 2s f')
    packed_data = s.pack(*values)
    print
    print 'Format String  :', s.format, 'for', name
    print 'Uses           :', s.size, 'bytes'
    print 'Packed Value   :', binascii.hexlify(packed_data)
    print 'Unpacked Values:', s.unpack(packed_data)

# Since most of the reasons to be working with binary packed data coincide with
# good reasons to optimize code, it's best to use the same buffer to minimise overhead


s = struct.Struct('I 2s f')
values = (1, 'ab', 2.7)
print 'Original:', values
print

print 'ctypes string buffer'
b = ctypes.create_string_buffer(s.size)
print 'Before  :', binascii.hexlify(b.raw)
s.pack_into(b, 0, *values)
print 'After   :', binascii.hexlify(b.raw)
print 'Unpacked:', s.unpack_from(b, 0)
print

print 'array'
a = array.array('c', '\0' * s.size)
print 'Before  :', binascii.hexlify(a)
s.pack_into(a, 0, *values)
print 'After   :', binascii.hexlify(a)
print 'Unpacked:', s.unpack_from(a, 0)
