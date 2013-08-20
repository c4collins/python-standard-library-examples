## 5.1 Decimal
# The decimal module implements fixed and floating-point calculations for most purposes
import decimal, pprint, threading
from Queue import PriorityQueue

## 5.1.1 Decimal

fmt = '{0:<25} {1:<25}'
print fmt.format('Input', 'Output')
print fmt.format('-' * 25, '-' * 25)

# Integer
print fmt.format(5, decimal.Decimal(5))

# String
print fmt.format('3.14', decimal.Decimal('3.14'))

# Float
f = 0.1
print fmt.format(repr(f), decimal.Decimal(str(f)))
print fmt.format('%.23g' % f, str(decimal.Decimal.from_float(f))[:25])

# Tuple - can be used to store or transmit values reconstructable into precise Decimals
# ( sign , ( digit1, digit2, ..., digitn ), integer exponent )
# for the sign: 0 = negative, 1 = positive
t = (0, (1,1), -2)
print fmt.format(t, decimal.Decimal(t))
p = (1, (3,1,4,1), -3)
print fmt.format(p, decimal.Decimal(p))
print
## 5.1.2 Arithmetic
# Decimal overloads the simple arithmetic operators, so instances can be manipulated the same way as numeric types.

a = decimal.Decimal('5.1')
b = decimal.Decimal('3.14')
c = 4
d = 3.14

print 'a     =', repr(a)
print 'b     =', repr(b)
print 'c     =', repr(c)
print 'd     =', repr(d)
print
print 'a + b =', a + b
print 'a - b =', a - b
print 'a * b =', a * b
print 'a / b =', a / b
print 
print 'a + c =', a + c
print 'a - c =', a - c
print 'a * c =', a * c
print 'a / c =', a / c
print
print 'a + d =', 
try:
    print a+d
except TypeError, e:
    print e
    
print '\nlog10(a)=', a.log10()
print 'ln(a)   =', a.ln()
print 'log10(b)=', b.log10()
print 'ln(b)   =', b.ln()
print

## 5.1.3 Special Values

for value in ['Infinity', 'naN', '0']:
    print decimal.Decimal(value), decimal.Decimal('-'+value)
print

# Math with Infinity
print 'Infinity + 1:', decimal.Decimal('Infinity') + 1
print 'Infinity - 1:', decimal.Decimal('Infinity') - 1

# Comparing NaN
print decimal.Decimal('NaN') == decimal.Decimal('Infinity')
print decimal.Decimal('NaN') != decimal.Decimal(1)

## 5.1.4 Context
# Contexts are used to override the default decimal settings
context = decimal.getcontext()
print '\nEmax     =', context.Emax
print 'Emin     =', context.Emin
print 'capitals =', context.capitals
print 'prec     =', context.prec
print 'rounding =', context.rounding
print 'flags    ='
pprint.pprint(context.flags)
print 'traps    ='
pprint.pprint(context.traps)
print

d = decimal.Decimal('0.123456')
for i in xrange(4):
    decimal.getcontext().prec = i
    print i, ':', d, d*1

ROUNDING_MODES = [
    'ROUND_CEILING',
    'ROUND_DOWN',
    'ROUND_FLOOR',
    'ROUND_HALF_DOWN',
    'ROUND_HALF_EVEN',
    'ROUND_HALF_DOWN', 
    'ROUND_UP',
    'ROUND_05UP',
    ]
header_fmt = '{:10} ' + ' '.join(['{:^8}'] * 6)
print header_fmt.format(' ',
                         '1/8 (1)', '-1/8 (1)',
                         '1/8 (2)', '-1/8 (2)',
                         '1/8 (3)', '-1/8 (3)',
                        )

for rounding_mode in ROUNDING_MODES:
    print '{0:10}'.format(rounding_mode.partition('_')[-1]),
    for precision in [1,2,3]:
        context.prec =precision
        context.rounding = getattr(decimal, rounding_mode)
        value = decimal.Decimal(1) / decimal.Decimal(8)
        print '{0:^8}'.format(value),
        value = decimal.Decimal(-1) / decimal.Decimal(8)
        print '{0:^8}'.format(value),
    print
print

context.prec = 28   # Resetting to defaults
context.rounding = ROUNDING_MODES[4]

# Since python 2.5, context can be applied to a block using with
with decimal.localcontext() as c:
    c.prec = 2
    print 'Local precision:', c.prec
    print '3.14 / 3 =', (decimal.Decimal('3.14') / 3)
print
print 'Default precision:', decimal.getcontext().prec
print '3.14 / 3 =', (decimal.Decimal('3.14') /3)
print

#setup a context with limited precision
c = decimal.getcontext().copy()
c.prec = 3
# create a constant
pi = c.create_decimal('3.1415926')

print 'PI    :', pi
print 'Result:', decimal.Decimal('2.01') * pi
print

# The 'global' context is actually thread-local, so each thread can be configured with different values
class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)
    
    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put( (self.prec, a* b) )
        return

a = decimal.Decimal('3.14')
b = decimal.Decimal('1.234')
# A PriorityQueue will return values sorted by precision, no matter what order the threads finish
q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in xrange(1,6)]
for t in threads:
    t.start()
for t in threads:
    t.join()
for i in xrange(5):
    prec, value = q.get()
    print prec, '\t', value
