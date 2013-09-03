## 16.3 unittest - Automated Testing Framework
import unittest

## 16.3.1
# Tests, as defined by unittest, have two parts: code to manage test dependencies (called fixtures) and the test itself
# Individual tests are created by subclassing TestCase and overriding or adding appropriate methods

class SimplisticTest( unittest.TestCase ):
    
    def test ( self ):
        self.failUnless(True)
        
## 16.3.2 Running Tests
# The easiest way is to include some code at the bottom of each test file and simply run the script directly from the CLI
# So go look at the EOF for this code
    
## 16.3.3 Test Outcomes
# Tests have three possible outcomes
    # ok    - The test passes
    # FAIL  - The test does not pass and raises an AssertionError exception
    # ERROR - the test raises any exception other than AssertionError
# There is no explicit way to make a test pass, they should be designed to not fail

class OutcomesTest( unittest.TestCase ):
    
    def testPass(self):
        return
    
    def testFail(self):
        self.failIf(True)
        
    def testError(self):
        raise RuntimeError("Test error!")

        
class FailureMessageTest( unittest.TestCase ):
    
    def testFail(self):
        self.failIf(True, "this is a failure message")
        
## 16.3.2 Asserting Truth
# Most tests  assert the truth of some condition.
# There are a few different ways to write truth-checking tests, depending on the perspective of the author and desired outcome of the code

class TruthTest( unittest.TestCase ):

    def testFailUnless(self):
        self.failUnless(True)
        
    def testAssertTrue(self):
        self.assertTrue(True)
        
    def testFailIf(self):
        self.failIf(True)
        
    def testAssertFalse(self):
        self.assertFalse(True)
        
## 16.3.5 Testing Equality
# As a special case, unittest includes methods for testing the equality of two values

class EqualityTest (unittest.TestCase):
    
    def testExpectEqual(self):
        self.failUnlessEqual(1, 3-2)
        
    def testExpectEqualFails(self):
        self.failUnlessEqual(2, 3-2)
        
    def testExpectNotEqual(self):
        self.failIfEqual(2, 3-2)
        
    def testExpectNotEqualFails(self):
        self.failIfEqual(1, 3-2)

## 16.3.6 Almost Equal?
# In addition to strict equality, it's mpossible to test for near equality of floating point numbers using failIfAlmostEqual() and failUnlessAlmostEqual()

class AlmostEqualTest (unittest.TestCase):
    
    def testEqual(self):
        self.failUnlessEqual(1.1, 3.3-2.2)
        
    def testAlmostEqual(self):
        self.failUnlessAlmostEqual(1.1, 3.3-2.2, places=1)
        
    def testNotAlmostEqual(self):
        self.failIfAlmostEqual(1.1, 3.3-2.0, places=1)

## 16.3.7 Testing for Exceptions
# if a test raises an exception other than AssertionError, it is treated as an error.
# This is useful for uncovering mistakes while modifying code that has existing test coverage
# There are circumstances, however, in which the test should verify that some code does produce an exception.
# One example is when an invalid value is given to an attribute of an object.
# In such cases, failUnlessRaises() or assertRaises() make the code mode clear than trapping the exception in the test.

def raises_error(*args, **kwds):
    raise ValueError( "Invalid value: " + str(args) + str(kwds) )

class ExceptionTest( unittest.TestCase ):
    
    def testTrapLocally(self):
        try:
            raises_error('a', b='c')
        except ValueError:
            pass
        else:
            self.fail('Did not see ValueError')
    
    def testfailUnlessRaises(self):
        self.failUnlessRaises(ValueError, raises_error, 'a', b='c')
        
## 16.3.8 Test Fixtures
# fixtures are outside resources needed by a test.
# For example, on test might need an instance of another class that provides configuration settings or another chared resource.
# Other test fixtures include database connections and temporary files.
# Many peole would argue that external resources makes these not unit tests, but they are being silly pedants because it works
# TestCase includes a special hook to configure and clean up any fixtures needed by tests.
# To configure the fixtures, override setUp().  To clean up, override tearDown()

class FixturesTest( unittest.TestCase ):
    
    def setUp(self):
        print "In setUp()"
        self.fixture = range(1, 10)
        
    def tearDown(self):
        print "In tearDown()"
        del self.fixture
        
    def test(self):
        print "In test()"
        self.failUnlessEqual(self.fixture, range(1,10))

## 16.3.9 Test Suites
# The stdlib documentation descibes how to organize test suites manually.
# Automated test discovery is more manageable for large code bases in which related tests are not all in the same place.
# Tools such as nose and py.test make it easier o manage tests when they are spread over multiple files and directories.

## 16.3.2 Running Tests
# The easiest way is to include the following at the bottom of each test file and simply run the script directly from the CLI

if __name__ == '__main__':
    unittest.main()