## 6.8 StringIO
# StringIO provides access to the file API (read(), write(), etc)
# There are two versions
    #  StringIO is written in Python for portability
    # cStringIO is written in C      for speed

# find the best implementation for the current platform
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
# writing to a buffer
output = StringIO()
output.write("This goes into the buffer. ")
print >>output, "And so does this"

# Retrieve the value written
print output.getvalue()

# discard buffer memory
output.close()

# Initialize a read buffer
input = StringIO('Initial value for read buffer')

# Read from the buffer
print input.read() # readline() and readlines() are also usable

# rewind a bit
input.seek(-11, 1) # f.seek(pos[, mode=0]) 
# mode 0 is absolute, 1 is from current position, and 2 is from EOF
print input.read()