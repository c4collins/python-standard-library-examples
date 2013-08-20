## 5.2 Fractions
# The Fraction class implements numerical operations for rational numbers
import fractions, decimal, math

## 5.2.1 Creating Fraction Instances
# using tuples
for n,d in [(1,2), (2,4), (3,6)]:
    f = fractions.Fraction(n, d)
    print '%s/%s = %s' % (n, d, f)
print

# using string fractions
for s in ["1/2", "2/4", "3/6"]:
    f = fractions.Fraction(s)
    print '%s = %s' % (s, f)
print

# using string floats
for s in ["0.5", "1.5", "2.0"]:
    f = fractions.Fraction(s)
    print '%s = %s' % (s, f)
print

# using raw floats and from_float()
for v in [0.1, 0.5, 1.5, 2.0]:
    f = fractions.Fraction.from_float(v)
    print '%s = %s' % (v, f)
    if f.numerator > 20000:
        print "      odd things can happen when the numbers can't be properly represented."
print

# using decimal floats and from_decimal()
for v in [ decimal.Decimal('0.1'), 
            decimal.Decimal('0.5'), 
            decimal.Decimal('1.5'), 
            decimal.Decimal('2.0'), 
         ]:
    f = fractions.Fraction.from_decimal(v)
    print '%s = %s' % (v, f)
print

## 5.2.2 Arithmetic
f1 = fractions.Fraction(1,2)
f2 = fractions.Fraction(3,4)

print '%s + %s = %s' % (f1, f2, f1+f2)
print '%s - %s = %s' % (f1, f2, f1-f2)
print '%s * %s = %s' % (f1, f2, f1*f2)
print '%s / %s = %s' % (f1, f2, f1/f2)


## 5.2.3 Approximating Values
print 'PI       =', math.pi
f_pi = fractions.Fraction(str(math.pi))
print 'No limit =', f_pi

for i in [ 1, 6, 11, 60, 70, 90, 100 ]:
    limited = f_pi.limit_denominator(i)
    print '{0:8} = {1}'.format(i, limited)