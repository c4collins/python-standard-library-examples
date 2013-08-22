# encoding:UTF-8
## 5.4 math
# The math module implements IEEE functions that would otherwise be found in the native platform C libraries
import math, random

## 5.4.1 Special Constants
print 'pi:', math.pi
print ' e:', math.e

## 5.4.2 Testing for Exceptional Values
print '\n{:^3} {:6} {:6} {:5}'.format('e', 'x', 'x**2', 'isinf')
print '{:-^3} {:-^6} {:-^6} {:-^5}'.format('', '', '', '')
for e in range(0, 201, 20):
    x = 10.0 ** e
    y = x*x
    print '{:3d} {!s:6} {!s:6} {!s:5}'.format(e, x, y, math.isinf(y))
    
x = 10.0 ** 200
print '\nx    =', x
print 'x*x  =', x*x
print 'x**2 =',
try:
    print x**2
except OverflowError, err:
    print err
    
x = x*x
y = x/x
print '\nx        =', x
print 'isnan(x) =', math.isnan(x)
print 'y = x/x  =', x/x
print 'y == nan =', y == float('nan')
print 'isnan(y) =', math.isnan(y)
print 

## 5.4.2 converting to Integers
# simplest method is trunc() but there are others
HEADINGS = ('i', 'int', 'trunc', 'floor', 'ceil')
print ' '.join(['{:^5}'] * 5).format(*HEADINGS)
print ' '.join(['{:-^5}'] * 5).format('','','','','',)
fmt = ' '.join(['{:5.1f}'] * 5)
TEST_VALUES = []
for i in xrange(20):
    # Gamma distribution
    rand = random.gammavariate( 1,2 )
    if i % 2 == 0:
        rand *= -1
    TEST_VALUES.append( rand )
for t in sorted(TEST_VALUES):
    print fmt.format(t, int(t), math.trunc(t), math.floor(t), math.ceil(t) )
print

## 5.4.4 Alternate Representations
# modf separates the number into a (portion, whole)
for i in xrange(6):
    print '{}/2 = {}'.format(i, math.modf(i/2.0))
print

# frexp(x) returns (m, e), where x = m + 2**e
print ' '.join(['{:^7}'] * 3).format('x','m','e')
print ' '.join(['{:-^7}'] * 3).format('','','')
for x in [0.1, 0.5, 4.0]:
    m,e = math.frexp(x)
    print '{:7.2f} {:7.2f} {:7d}'.format( x, m, e )
    
# ldexp(m,e) returns x, where x = m + 2**e
print ' '.join(['{:^7}'] * 3).format('m','e','x')
print ' '.join(['{:-^7}'] * 3).format('','','')
for m,e in [ (0.8, -3), (0.5, 0), (0.5, 3) ]:
    x = math.ldexp(m, e)
    print '{:7.2f} {:7d} {:7.2f}'.format( m, e, x )
print

## 5.4.5 Positive and Negative Signs
print math.fabs(-1.1)
print math.fabs(-0.0)
print math.fabs( 0.0)
print math.fabs( 1.1)
print

HEADINGS = ('f', 's', '< 0', '> 0', '= 0')
print ' '.join(['{:^5}'] * 5).format(*HEADINGS)
print ' '.join(['{:-^5}'] * 5).format('', '', '', '', '')
for f in [ -1.0, 0.0, 1.0, 
            float('-inf'), 
            float('inf'), 
            float('-nan'), 
            float('nan')
          ]:
    s = int(math.copysign(1, f))
    print '{:5.1f} {:5d} {!s:5} {!s:5} {!s:5}'.format( f, s, f < 0, f > 0, f== 0 )
    
## 5.4.6 Commonly Used Calculations
values = [ 0.1 ] * 10

s = 0.0
for i in values:
    s += i

print "\nInput values:", values
print 'for loop    : {:.20f}'.format(s)
print 'sum()       : {:.20f}'.format(sum(values))
print 'math.fsum() : {:.20f}'.format(math.fsum(values)) # fsum accurately adds up floats
print

# factorial() accepts floats, but only if they can be converted to an integer without losing value.
for i in [ 0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.1 ]:
    try:
        print '{:2.0f}  {:6.0f}'.format( i, math.factorial(i) )
    except ValueError, err:
        print 'Error computing factorial(%s):' % i, err
print

# gamma() is similar to factorial, but it also works with real numbers
# gamma = (n-1)!
for i in [ 0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6 ]:
    try:
        print '{:2.0f}  {:6.0f}'.format( i, math.gamma(i) )
    except ValueError, err:
        print 'Error computing gamma(%s):' % i, err
print
        
# lgamma() is similar to factorial, but it also works with real numbers
# lgamma = log(gamma(())
for i in [ 0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6 ]:
    try:
        print '{:2.1f}  {:.20f}  {:.20f}'.format( i, math.lgamma(i), math.log(math.gamma(i)) )
    except ValueError, err:
        print 'Error computing lgamma(%s):' % i, err
print

# fmod is the modulus operation (%) for floats, but the algorithm is a little different
print '{:^4} {:^4} {:^5} {:^5}'.format('x', 'y', '%', 'fmod')
print '{:-^4} {:-^4} {:-^5} {:-^5}'.format('', '', '', '')
for x, y in [ (5, 2), (5, -2), (-5, 2)]:
    print '{:^4} {:^4} {:^5} {:^5}'.format(x, y, x%y, math.fmod(x, y))
print

## 5.4.7 Exponents and Logarithms
# pow(r, e) for p**e
for x,y in [
    # Typical Cases
    (2,3), (2.1, 3.2),
    # Always 1
    (1.0, 5), (2.0, 0),
    # NaN
    (2, float('nan')),
    # Roots
    (9.0, 0.5), (27.0, 1.0/3),
    ]:
    print '{:5.1f} ** {:5.3f} = {:6.3f}'.format(x, y, math.pow(x, y))
print

# sqrt(x) for x**(1/2)
for x in [ 9.0, 3, -1, 144, 145]:
    try:
        print math.sqrt(x)
    except ValueError, err:
        print 'Cannot compute sqrt(%5.2f):' % x, err
print

# log(x, b) finds y where x = b**y
# log(x) defaults to a base of e, that is log(x) is equivalent to a written 'ln(x)'
print math.log(8)
print math.log(8, 2)
print math.log(0.5, 2)
print
# there is also a log10(x) which is more precise than log(x, 10)
print '{:2} {:^12} {:^10} {:^20} {:8}'.format( 'i', 'x', 'accurate', 'inaccurate', 'mismatch' )
print '{:-^2} {:-^12} {:-^10} {:-^20} {:-^8}'.format( '', '', '', '', '' )
for i in xrange(10):
    x = math.pow(10, i)
    accurate = math.log10(x)
    inaccurate = math.log(x, 10)
    match = '' if int(inaccurate) == i else '*'
    print '{:2d} {:12.1f} {:10.8f} {:20.18f} {:^5}'.format( i, x, accurate, inaccurate, match )
print

# log1p(x) calculates ln(x+1), and is more accurate at values very close to 0
x = 0.00000000000000000000000000000001
print 'x       :', x
print '1 + x   :', 1+x
print 'log(1+x):', math.log(1+x)
print 'log1p(x):', math.log1p(x)
print

# exp(x) computes e**x, and is again slightly more accurate
x = 2
fmt = '%.20f'
print fmt % (math.e ** 2)
print fmt % math.pow(math.e, 2)
print fmt % math.exp(2)
print

# expm1() is the inverse of log1p() and calculates e**x-1
x = 0.00000000000000000000000000000001
print 'x       :', x
print 'exp(x)-1:', math.exp(x)-1
print 'expm1(x):', math.expm1(x)
print

## 5.4.8 Angles
# To convert from degrees to radians, use radians(x)
print ' '.join(['{:^7}'] * 3).format( 'Degrees', 'Radians', 'Expected' )
print ' '.join(['{:-^7}'] * 3).format( '', '', '' )
for deg, expected in [
    (   0,         0 ),
    (  30, math.pi/6 ),
    (  45, math.pi/4 ),
    (  60, math.pi/3 ),
    (  90, math.pi/2 ),
    ( 180, math.pi   ),
    ( 270, 3 / 2.0 * math.pi ),
    ( 360, 2        * math.pi ),
]:
    print '{:7d} {:7.2f} {:7.2f}'.format( deg, math.radians(deg), expected )
print

# To convert from radians to degrees, use degrees(x)
print ' '.join(['{:^8}'] * 3).format( 'Radians', 'Degrees', 'Expected' )
print ' '.join(['{:-^8}'] * 3).format( '', '', '' )
for expected, rad in [
    (   0,         0 ),
    (  30, math.pi/6 ),
    (  45, math.pi/4 ),
    (  60, math.pi/3 ),
    (  90, math.pi/2 ),
    ( 180, math.pi   ),
    ( 270, 3 / 2.0 * math.pi ),
    ( 360, 2        * math.pi ),
]:
    print '{:8.2f} {:8.2f} {:8.2f}'.format( rad, math.degrees(rad), expected )
print

## 5.4.9 Trigonometry
# All of the trigonometric functions in the standard library take angles expressed as radians.
print ' '.join(['{:7}'] * 5).format('Degrees', 'Radians', 'Sine', 'Cosine', 'Tangent')
print ' '.join(['{:-^7}'] * 5).format('', '', '', '', '')

fmt = ' '.join(['{:7.2f}'] * 5)

for deg in xrange(0, 361, 30):
    rad = math.radians(deg)
    if deg in (90, 270):
        t = float('inf')
    else:
        t = math.tan(rad)
    print fmt.format( deg, rad, math.sin(rad), math.cos(rad), t )
print

# Given a point (x,y) for a triangle with points at [(0,0), (x,0), (x,y)] can be calculated
# using the formula (x**2 + y**2) ** 1/2 (Pythagorean's Theorum)
print '{:^7} {:^7} {:^10}'.format( 'X', 'Y', 'Hypotenuse' )
print '{:-^7} {:-^7} {:-^10}'.format( '', '', '' )
for x, y in [
    # simple points
    (1,1), (-1, -1), 
    # sqrt
    (math.sqrt(2), math.sqrt(2)), 
    # 3-4-5 triangle
    (3,4),
    # on the circle
    (math.sqrt(2)/2, math.sqrt(2)/2), # pi/4 radians
    (0.5, math.sqrt(3)/2) # pi/3 radians
]:
    h = math.hypot(x, y)
    print '{:7.2f} {:7.2f} {:7.2f}'.format( x, y, h )
print

# The same function [hypot(x,y)] can be used to find the length of any line
print ' '.join(['{:^8}'] * 5).format('X1', 'Y1', 'X2', 'Y2', 'Distance')
print ' '.join(['{:-^8}'] * 5).format('', '', '', '', '')

for (x1, y1), (x2, y2) in [ 
    ((  5,  5 ), (  6,  6 )),
    (( -6, -6 ), ( -5, -5 )),
    ((  0,  0 ), (  3,  4 )),    # 3-4-5 triangle
    (( -1, -1 ), (  2,  3 )),    # 3-4-5 triangle
]:
    x = x1 - x2
    y = y1 - y2
    h = math.hypot(x, y)
    print ' '.join(['{:8.2f}'] * 5).format( x1, y1, x2, y2, h )
print

print '{:^3} {:^6} {:^6} {:^6}'.format('R', 'Arcsin', 'Arccos', 'Arctan')
print '{:-^3} {:-^6} {:-^6} {:-^6}'.format('', '', '', '')
for r in [ 0, 0.5, 1 ]:
    print '{:3.1f} {:6.4f} {:6.4f} {:6.4f}'.format( r, math.asin(r), math.acos(r), math.atan(r) )
print

## 5.4.10 Hyperbolic Functions
# Hyperbolic functions  appear in linear differential equations
print '{:^4} {:^6} {:^6} {:^6}'.format('X', 'sinh', 'cosh', 'tanh')
print '{:-^4} {:-^6} {:-^6} {:-^6}'.format('', '', '', '')
for x in xrange(0, 11, 2):
    x = x/10.0
    print '{:4.2f} {:6.4f} {:6.4f} {:6.4f}'.format( x, math.sinh(x), math.cosh(x), math.tanh(x) )
print

## 5.4.11 Special Functions
# Gauss Error function
print '{:^5} {:7}'.format('X', 'erf(x)')
print '{:-^5} {:-^7}'.format('', '')
for x in [-3, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 3]:
    print '{:5.2f} {:7.4f}'.format( x, math.erf(x) )
print

# And the complimentar error functions
print '{:^5} {:7}'.format('X', 'erfc(x)')
print '{:-^5} {:-^7}'.format('', '')
for x in [-3, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 3]:
    print '{:5.2f} {:7.4f}'.format( x, math.erfc(x) )
print