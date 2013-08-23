## 6.3 - linecache
# linecache keeps the lines from a file in memory in a list
import linecache, tempfile, os

## 6.3.1 Test Data

lorem = """Aouda was safe; and Phileas Fogg, who had been in the thickest of the fight, had not received a scratch.  Fix was slightly wounded in the arm.
But Passepartout was not to be found, and tears coursed down Aouda's cheeks. 

All the passengers had got out of the train, the wheels of which were stained with blood.  From the tyres and spokes hung ragged pieces of flesh.  As far as the eye could reach on the white plain behind, red trails were visible.
The last Sioux were disappearing in the south, along the banks of Republican River. Mr. Fogg, with folded arms, remained motionless.  He had a serious decision to make. Aouda, standing near him, looked at him without speaking, and he understood her look.  
If his servant was a prisoner, ought he not to risk everything to rescue him from the Indians?  "I will find him, living or dead," said he quietly to Aouda. "Ah, Mr.&mdash;Mr. Fogg!" cried she, clasping his hands and covering them with tears. "Living," added Mr. Fogg, "if we do not lose a moment." Phileas Fogg, by this resolution, inevitably sacrificed himself; he pronounced his own doom.  
The delay of a single day would make him lose the steamer at New York, and his bet would be certainly lost.  \nBut as he thought, "It is my duty," he did not hesitate. The commanding officer of Fort Kearney was there."""

def make_tempfile():
    fd, temp_file_name = tempfile.mkstemp()
    os.close(fd)
    f = open(temp_file_name, 'wt')
    try:
        f.write(lorem)
    finally:
        f.close()
    return temp_file_name

def cleanup(filename):
    os.unlink(filename)
    
filename = make_tempfile()
    
## 6.3.2 Reading Specific Lines
# linecache line numbers start at 1, while most lists start at 0... just something to keep in mind
## Pick out the same line from source and cache
print 'Source : %r' % lorem.split('\n')[4]
print 
print 'Cache  : %r' % linecache.getline(filename, 5)
print

## 6.3.3 Handling Blank Lines
# The return value always includes the newline at the end, so blank lines are just that

print 'Blank  : %r' % linecache.getline(filename, 3)
print

## 6.3.4 Error Handling
# getline() returns an empty string if the request is for an invalid line number

print 'Invalid: %r'            %      linecache.getline(filename, 500)
print ' Length: %d characters' % len( linecache.getline(filename, 500) )
print

cleanup(filename)

## 6.3.5 Reading Python Source Files
# linecache is used heavily when producing tracebacks

# use the built-in sys.path.search to look at the linecache module
module_line = linecache.getline('linecache.py', 3)
print 'Module :', repr(module_line)
print

# Look at the linecache module source directly.
file_src = linecache.__file__
if file_src.endswith('.pyc'):
    file_src = file_src[:-1]

print 'File:  :',
with open(file_src, 'r') as f:
    file_line = f.readlines()[2]
print repr(file_line)