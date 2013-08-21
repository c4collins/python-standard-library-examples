## 5.3 Random
# Uses the Mersenne Twister algorithm
import random, os, itertools, time, decimal, math
import cPickle as pickle

## 5.3.1 Generating Random numbers
for i in xrange(5):
    print '%04.3f' % random.random(),
print

# uniform() will generate numbers within a specified range
for i in xrange(5):
    print '%04.3f' % random.uniform(1,100),
print

# Seeding gives the same set of 'random' data each time
random.seed(1)
for i in xrange(5):
    print '%04.3f' % random.random(),
print
random.seed(1)
for i in xrange(5):
    print '%04.3f' % random.random(),
print
random.seed(1)
for i in xrange(5):
    print '%04.3f' % random.random(),
print '\n'

## 5.3.3 Saving State
if os.path.exists('5.3.3-state.dat'):
    #Restore the previously saved state
    print "Found '5.3.3-state.dat', initializing random module"
    with open('5.3.3-state.dat', 'rb') as f:
        state = pickle.load(f)
    random.setstate(state)
else:
    # Use a known start state
    print "No '5.3.3-state.dat', seeding"
    random.seed(1)

# Produce random values
for i in xrange(3):
    print '%04.3f' % random.random(),
print '\n'
 
# Save state for next time
with open('5.3.3-state.dat', 'wb') as f:
    pickle.dump(random.getstate(), f)

# Produce more random values
print "After saving state:"
for i in xrange(3):
    print '%04.3f' % random.random(),
print '\n'

# Random integers
print '[1, 100]:',
for i in xrange(3):
    print random.randint(1,100),

print '\n[-5 ,5]:',
for i in xrange(3):
    print random.randint(-5, 5),
print

for i in xrange(3):
    print random.randrange(0, 101, 5), # random.randrange(min, max, step)
print '\n'

## 5.3.5 Picking Random Items
for j in xrange(2):
    outcomes = { 'heads':0, 'tails':0, }
    sides = outcomes.keys()
    random.seed() # reset the seed to a random value
    for i in xrange(10000):
        outcomes[ random.choice(sides) ] += 1
        
    for key in sides:
        print key,':',outcomes[key]
    print

## 5.3.6 Permutations

FACE_CARDS = ('J', 'Q', 'K', 'A')
SUITS = ('H', 'D', 'C', 'S')

def new_deck():
    return list( itertools.product(
                    itertools.chain( xrange(2, 11), FACE_CARDS ), 
                    SUITS 
                ))
                
def show_deck(deck):
    p_deck = deck[:]
    while p_deck:
        row = p_deck[:13]
        p_deck = p_deck[13:]
        for j in row:
            print '%2s%s' % j,
        print
        
# Make a new deck, with the cards in order
deck = new_deck()
print "\nInitial deck:"
show_deck(deck)

# Shuffle and sisplay the shuffled deck
random.shuffle(deck)
print "\nShuffled Deck:"
show_deck(deck)

# Deal 4 hands of 5 cards
hands = [ [], [], [], [] ]
for i in xrange(5):
    for h in hands:
        h.append(deck.pop())

# Show the hands
print "\nHands:"
for n, h  in enumerate(hands):
    print '%d:' % (n+1)
    for c in h:
        print '%2s%s' % c,
    print

# Show remaining deck
print "\nRemaining deck:"
show_deck(deck)

## 5.3.6 Sampling
with open('/usr/share/dict/words', 'rt') as f:
    words = f.readlines()
words = [w.rstrip() for w in words ]
for w in random.sample(words, 5):
    print w,
print "\n"

## 5.3.8 Multiple Simultaneous Generators
# Each instance of Random can have these properties set on it's own, and can be utilized separately
print "Default Initialization:\n"

r1 = random.Random()
r2 = random.Random()

for i in xrange(3):
    print '%04.3f  %04.3f' % (r1.random(), r2.random())
    
print "\nSame seed:\n"
seed = time.time()
r1 = random.Random(seed)
r2 = random.Random(seed)
for i in xrange(3):
    print '%04.3f  %04.3f' % (r1.random(), r2.random())
    
print "\nForce jumpahead on r2:\n"
r2.jumpahead(1024)

for i in xrange(3):
    print '%04.3f  %04.3f' % (r1.random(), r2.random())
    
## 5.3.9 SystemRandom
# SystemRandom has the same API as Random, but uses os.urandom() to generate values
# this means seed() and setstate() do nothing because the randomness is coming from the system
print "Default Initialization:\n"

r1 = random.SystemRandom()
r2 = random.SystemRandom()

for i in xrange(3):
    print '%04.3f  %04.3f' % (r1.random(), r2.random())
    
print "\nSame seed:\n"
seed = time.time()
r1 = random.SystemRandom(seed)
r2 = random.SystemRandom(seed)
for i in xrange(3):
    print '%04.3f  %04.3f' % (r1.random(), r2.random())
    
## 5.3.10 Nonuniform Distributions
# Set up context for rounding
c = decimal.getcontext().copy()
c.rounding = 'ROUND_UP'
c.prec = 2

    ## Normal
mu    = 7.5    # mean
sigma = 2.0    # std. deviation
print "\nNormal(mu=%d, sigma=%d):" % (mu, sigma)
normal = []
for i in xrange(20):
    normal.append(c.create_decimal( random.normalvariate( mu, sigma ) ))
normal = sorted(normal)
for n in normal:
    print "%02.1d" % n,
    
    ## Gauss-Normal
print "\n(Gauss) Normal(mu=%d, sigma=%d):" % (mu, sigma)
gauss = []
for i in xrange(20):
    gauss.append(c.create_decimal( random.gauss( mu, sigma ) ))
gauss = sorted(gauss)
for g in gauss:
    print "%02.1d" % g,
    
    ## Log-Normal
print "\n(Logarithmic) Normal(mu=%d, sigma=%d):" % (mu, sigma)
lognormal = []
for i in xrange(15):
    lognormal.append(c.create_decimal( random.lognormvariate( mu, sigma ) ))
lognormal = sorted(lognormal)
for l in lognormal:
    print "%02.1d" % l,    

    ## Triangular
low  = 0
high = 10
mode = 7.5
print "\nTriangular(low=%d, high=%d, mode=%d)" % ( low, high, mode)
triangular = []
for i in xrange(20):
    triangular.append( c.create_decimal( random.triangular( low, high, mode ) ) )
triangular = sorted(triangular)
for t in triangular:
    print "%02.1d" % t,

    ## Exponential
lambd = 1.0 / 7.5 # lambd is (1.0 / the desired mean)
print "\nExponential(lambd=%0.4r)" % ( lambd )
exponential = []
for i in xrange(20):
    exponential.append( c.create_decimal( random.expovariate( lambd ) ) )
exponential = sorted(exponential)
for e in exponential:
    print "%02.1d" % e,

    ## Pareto distribution
alpha = 1     # shape parameter
print "\n(Long Tail) Pareto(alpha=%d)" % ( alpha )
pareto = []
for i in xrange(20):
    pareto.append( c.create_decimal( random.paretovariate( alpha ) ) )
pareto = sorted(pareto)
for p in pareto:
    print "%02.1d" % p,
    
    ## Angular (Von Mises)
mu    = math.pi * 1.5  # radians between 0 and 2*pi
kappa = 1.5            # concentration, must be >= 0
print "\n(Von Mises) Angular(mu=%d, kappa=%d)" % ( mu, kappa )
angular = []
for i in xrange(20):
    angular.append( c.create_decimal( random.vonmisesvariate( mu, kappa ) ) )
angular = sorted(angular)
for a in angular:
    print "%02.1d" % a,
    
    ## Beta distribution
alpha = 1
beta  = 2
print "\nBeta(alpha=%d, beta=%d)" % ( alpha, beta )
beta_v = []
for i in xrange(20):
    beta_v.append( random.betavariate( alpha, beta ) )
beta_v = sorted(beta_v)
for b in beta_v:
    print c.create_decimal(b),
    
    ## Gamma distribution
print "\nGamma(alpha=%d, beta=%d)" % ( alpha, beta )
gamma = []
for i in xrange(20):
    gamma.append( random.gammavariate( alpha, beta ) )
gamma = sorted(gamma)
for g in gamma:
    print c.create_decimal(g),
    
    ## Weibull distribution
print "\nWeibull(alpha=%d, beta=%d)" % ( alpha, beta )
weibull = []
for i in xrange(20):
    weibull.append( random.weibullvariate( alpha, beta ) )
weibull = sorted(weibull)
for w in weibull:
    print c.create_decimal(w),