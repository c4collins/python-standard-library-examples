## 6.9 fnmatch - UNIX-Style Glob Pattern Matching
# fnmatch compares filenames to glob-style patterns
import fnmatch, os, pprint

## 6.9.1 Simple matching
# fnmatch compares a filename to a pattern and returns a Boolean indicating if they match
patterns = ['6.?-*.py', '6.?.*-*.py', '*.*.*-*.py', '*io.py', '*IO.py']
files = os.listdir(os.curdir)

for pattern in patterns:
    print ' Pattern:', pattern
    for name in files:
        if fnmatch.fnmatch(name, pattern):
            print 'No Case Filename: %-25s' % name
                
    # case-sensitive comparisons can be forced with fnmatchcase()
    # [not that Linux cares if I tell it to be case-sensitive]
    for name in files:
        if fnmatch.fnmatchcase(name, pattern):
            print '   Case Filename: %-25s' % name
    print
    
## 6.9.2 Filtering
# to test a sequence of filenames, use filter() which returns a list
print 'Pattern :', patterns[0]
print 'Files   :'
pprint.pprint(files)
print 'Matches :'
pprint.pprint( fnmatch.filter( files, patterns[0]) )
print

## 6.9.3 Translating Patterns
# fnmatch converts the glob pattern to regex and uses the re module to compare the name and apttern
# the translate) function is the public API to do so
for pattern in patterns:
    print 'Pattern:', pattern
    print 'Regex  :', fnmatch.translate(pattern)