## Using difflib to computer and work with differences between sequences
text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu rementum euismod. Donec
pulvinar porttitor tellus.  Aliquam ventatis. Donec facilisis
pharetra tortor.  In nec mauris eget magna consequat
convallis. Nam sed sem vitae odio pellentesque interdum.
Sed consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhocus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem is nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
tristitque enim. Donec quis lectus a justo imperdiet tempus."""
text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu rementum euismod. Donec
pulvinar, porttitor tellus.  Aliquam ventatis. Donec facilisis
pharetra tortor. In nec mauris eget magna consequat
convallis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhocus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem is nisl porta
adipiscing. Duis vulputate tristitque enim. Donec quis lectus a
justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text1_lines = text1.splitlines()
text2_lines = text2.splitlines()

import difflib

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print '\n'.join(diff)

 # Differ relies on SequenceMatcher to detect noise in the input
 # The default for ndiff() is to ignore space and tab characters

from difflib import SequenceMatcher

def show_results(s):
    # SequenceMatcher.find_longest_match(self, alo, ahi, blo, bhi)
    # In this case, it's A[0:5] and B[0:9], which are their full lengths
    # and it checks for the longest (maximal) matches, and returns the earliest
    # locations in each string in an output of (Astart, Bstart, length)
    i, j, k = s.find_longest_match(0,5,0,9)
    print ' i = %d' % i
    print ' j = %d' % j
    print ' k = %d' % k
    print ' A[i:i+k] = %r' % A[i:i+k]
    print ' B[j:j+k] = %r' % B[j:j+k]

A = " abcd"
B = "abcd abcd"

print ' A = %r' % A
print ' B = %r' % B

print '\n Without junk detection:'
show_results(SequenceMatcher(None, A, B))
print '\n Treat spaces as junk:'
show_results( SequenceMatcher( lambda x: x == " ", A, B ))

 # SequenceMatcher works on any two sequences of any hashable type 
import random
s1 = [x for x in range(0, 101)] # [ 1, 2, 3, 5, 6, 4 ]
s2 = s1[:]
random.shuffle(s1)
        

print '\nInitial data:'
print ' s1 =', s1
print ' s2 =', s2
print ' s1 == s2:', s1==s2
print

matcher = difflib.SequenceMatcher(None, s1, s2)
 # get_opcodes() returns the instructions for converting the original list into the new version
 # these changes are applied in reverse so the indexes stayed consistent
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
    if tag == 'delete':
        print 'Remove %s from positions [%d:%d].' % (s1[i1:i2], i1, i2)
        del s1[i1:i2]
    elif tag == 'equal':
        print 's1[%d:%d] and s2[%d:%d] are equal.' % (i1, i2, j1, j2)
    elif tag == 'insert':
        print 'Insert %s from s2[%d:%d] into s1 at %d.' % (s2[j1:j2], j1, j2, i1)
        s1[i1:i2] = s2[j1:j2]
    elif tag == 'replace':
        print 'Replace %s from s1[%d:%d] with %s from s2[%d:%d].' % (s1[i1:i2], i1, i2, s2[j1:j2], j1, j2)
        s1[i1:i2] = s2[j1:j2]

    print ' s1 =', s1

print ' s1 == s2:', s1==s2
        
