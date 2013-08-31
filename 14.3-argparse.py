## 14.3 argparse - Command-Line Option and Argument Parsing
# argparse deprecates optparse and getopt and has more features in general
# argparse is the current standard, and deprecates the other two modules
import argparse, datetime
from ConfigParser import ConfigParser   # Parser for config files similar to the Windows .ini files
import shlex                            # Simple lexical analysis of syntaxes resembling those found in the Unix shell

## 14.3.1 Comparing with optparse
# argparse is very closely related to optparse
# I don't really care as I haven't used either ever
# argparse should be used in all new programs if it will be available

## 14.3.2 Setting up a parser
# First step when using argparse is to create a parser object and tell it about what arguments to expect.
# The parser can then be used to process the command line arguments when the program runs.
parser = argparse.ArgumentParser(
    description="Simple Examples"
)

## 14.3.3 Defining Arguments
# Arguments trigger different actions, specified by the action argument to add_argument
# Supported actions include:
    # storing the argument (singly or as part of a list
    # storing a constant value when the argument is encountered
    # counting the number of times an argument is seen
    # calling a callback to custom processing instructions
# The default is to store the argument 
# using dest to declare the location of the data and type to change the type if necessary

## 14.3.4 Parsing a Command Line
# By default, the arguments are taken as a list form sys.argv[1:], but any list of strings can be used
# The options are processed using the GNU/POSIX system, so option & argument values can be mixed
# The return value from parse_args) is a Namespace containing the arguments to the command, as attributes

## 14.3.5 Simple Examples
# A Boolean, a string, and an integer walk into a command and get into an argument
parser.add_argument( '-a', action='store_true', default=False )
parser.add_argument( '-b', action='store', dest='b' )
parser.add_argument( '-c', action='store', dest='c', type=int )
print parser.parse_args( ['-a', '-bval', '-c', '3' ] )

# longer argument names functions the same way
parser = argparse.ArgumentParser(
    description="Long arguments"
)
parser.add_argument( '--noarg', action='store_true', default=False )
parser.add_argument( '--witharg', action='store', dest='witharg' )
parser.add_argument( '--witharg2', action='store', dest='witharg2', type=int )
print parser.parse_args( [ '--noarg', '--witharg', 'val', '--witharg2=4' ] )

# argparse also handles non-optional arguments
parser = argparse.ArgumentParser(
    description="Non-optional"
)
parser.add_argument( 'count', action='store', type=int )
parser.add_argument( 'units', action='store' )
print parser.parse_args( [ "3", "inches" ] )
parser = argparse.ArgumentParser(
    description="Non-optional"
)
try:
    parser.parse_args( [ "some", "inches" ] )
except:
    print "Improper argument format."
print

    ## Argument Actions
# There are six built-in actions that can be triggered
    # store - Optionally converts type and stores the value.  This is default.
    # store_const - Save a defines value as part of the argument specification rather than a value from the argument.
        # This is typically used to set non-Boolean flags.
    # store_true / store_false - saves the according Boolean value.
    # append - Saves the value to a list.  Can have repeat occurrences.
    # append_const - Save a value defined in the argument specification to a list.
    # version - Print version details about the program and then exits.
parser = argparse.ArgumentParser(
    description="Argument Actions"
)
parser.add_argument( '-s', action='store', dest='simple_value', 
                    help="Store a simple value", )
parser.add_argument( '-c', action='store_const', dest='constant_value', const='value-to-store',
                    help="Store a constant value", )
parser.add_argument( '-t', action='store_true', dest='boolean_switch', default=False,
                    help="Set a switch to true", )
parser.add_argument( '-f', action='store_false', dest='boolean_switch', default=True,
                    help="Set a switch to false", )
parser.add_argument( '-a', action='append', dest='collection', default=[],
                    help="Add repeated values to a list", )                    
parser.add_argument( '-A', action='append_const', dest='const_collection', const='value-1-to-append', default=[],
                    help="Add values to a list", )
parser.add_argument( '-B', action='append_const', dest='const_collection', const='value-2-to-append', default=[],
                    help="Add different values to a list", )
parser.add_argument( '--version', action='version', version='%(prog)s 1.0',
                    help="Add values to a list", )
given_args = [ ['-s', 'value', ],
               ['-c', ],
               ['-t', ],
               ['-f', ],
               ['-a', 'one', '-a', 'two', '-a', '3', ], 
               # ['--version',],    # This will explicitly kill the program
               # ['-h', ],          # This will explicitly kill the program
               ['-A', '-B', ],  ]

display_fmt = "{:20} = {}"               
for args in given_args:
    print display_fmt.format("Arguments", args )
    results = parser.parse_args(args)
    print display_fmt.format("simple_value", results.simple_value)
    print display_fmt.format("constand_value", results.constant_value)
    print display_fmt.format("boolean_switch", results.boolean_switch)
    print display_fmt.format("collection", results.collection)
    print display_fmt.format("const_collection", results.const_collection)
print
    
    ## Option Prefixes
# The default prefix is a dash '-', as this conforms to UNIX standards
# but argparse supports other prefixes, like the '/' used in Windows
parser = argparse.ArgumentParser(
    description="Option Prefixes",
    prefix_chars="-+/",
)
parser.add_argument( '-a', action='store_false', default=None,
                     help="Turn A off", )
parser.add_argument( '+a', action='store_true', default=None,
                     help="Turn A on", )                     
parser.add_argument( '//noarg', '++noarg', action='store_true', default=False,
                     help="Set True", )
given_args = [ ['+a', ], ['-a', ], ['//noarg', ], ['++noarg', ], ]
for args in given_args:
    print display_fmt.format("Arguments", args )
    results = parser.parse_args(args)
    print display_fmt.format("a", results.a)
    print display_fmt.format("noarg", results.noarg)
print
    
    ## Sources of Arguments
# So far I've been passing lists of arguments to the parser, 
# but I could also use sys.argv[1:] to get them
parser = argparse.ArgumentParser(
    description="Argument Sources"
)
parser.add_argument( '-a', action='store_true', default=False )
parser.add_argument( '-b', action='store', dest="b" )
parser.add_argument( '-c', action='store', dest="c", type=int )

config = ConfigParser()
config.read('data/14.3-argparse_config.ini')

config_value = config.get('cli', 'options')
argument_list = shlex.split( config_value )
print "Config   :", config_value
print "Args List:", argument_list
print "Results  :", parser.parse_args( argument_list )

# Using fromfile_prefix_chars, you can tell argparse how to recognize an argument that specifies 
# an input file that contains a set of arguments 
parser = argparse.ArgumentParser(
    description="fromfile Prefix",
    fromfile_prefix_chars='@',
)
parser.add_argument( '-a', action='store_true', default=False )
parser.add_argument( '-b', action='store', dest="b" )
parser.add_argument( '-c', action='store', dest="c", type=int )
print "Alternate:", parser.parse_args(['@data/14.3-argparse_fromfile-prefix.txt'])

## 14.3.6 Automatically Generated Options
# argparse will automatically add options to generate help and show the version information for the application
# if configured to do so.
parser = argparse.ArgumentParser(
    description="Automatically Generated Options",
    add_help=False, # set to true to generate help, but it kills the program and we must persist
    version="1.0",
)
parser.add_argument( '-a', action='store_true', default=False )
parser.add_argument( '-b', action='store', dest="b" )
parser.add_argument( '-c', action='store', dest="c", type=int )
print parser.parse_args()

## 14.3.7 Parser Organization
    ## Sharing Parsing Rules
# When you need to share sets of common arguments across a set of argument parsers
# (Such as a series of programs all requiring --user and --password arguments)
# You can define a common parent parser
# since help will be added by each individual module, it's turned off in the parent
parser = argparse.ArgumentParser(add_help=False, description="Sharing Parsing Rules", )
parser.add_argument('--user', action='store' )
parser.add_argument('--password', action='store' )

parser2 = argparse.ArgumentParser( parents=[ parser, ], add_help=True, description="Sharing Parsing Rules 2",  )
parser2.add_argument('--local_arg', action='store_true', default=False )
print parser2.parse_args() # ( ['-h', ] ) # -h works to generate help, but it's deadly

    ## Conflicting Options
# Instead of generating an error when there are conflicting argument names
# set the conflict_handler='resolve' and watch out for odd masking

# Default with error
parser2 = argparse.ArgumentParser( parents=[ parser, ], description="Conflicting Options - Default with error",  )
try:
    parser2.add_argument( '--user', action='store' )
except argparse.ArgumentError, err:
    print "ERROR :: ", err
print parser2.parse_args( [ '--user', 'user', '--password', 'password', ] )

# Resolved conflict
parser2 = argparse.ArgumentParser( parents=[ parser, ], conflict_handler='resolve', description="Conflicting Options - Resolved conflict",  )
parser2.add_argument( '--user', action='store' )
print parser2.parse_args( [ '--user', 'user', '--password', 'password', ] )

# Masked option
parser2 = argparse.ArgumentParser( conflict_handler='resolve', description="Conflicting Options - Masked option",  )
parser2.add_argument( '-b', action='store' )
parser2.add_argument( '--long-b','-b', action='store' )
print parser2.parse_args( )

# Unmasked option
parser2 = argparse.ArgumentParser( conflict_handler='resolve', description="Conflicting Options - Unmasked option",  )
parser2.add_argument( '--long-b','-b', action='store' )
parser2.add_argument( '-b', action='store' )
print parser2.parse_args( )

    ## Argument Groups
# argparse combines the argument definitions into groups
# By default there are two, one for options and one for position-based arguments
# But it's very easy to make and assign new groups

parser = argparse.ArgumentParser(add_help=False, description="Argument Groups", )
group = parser.add_argument_group('authentication')
group.add_argument('--user', action='store' )
group.add_argument('--password', action='store' )

parser2 = argparse.ArgumentParser( parents=[ parser, ], description="Argument Groups 2",  )
parser2.add_argument('--local_arg', action='store_true', default=False )
print parser2.parse_args() # ( ['-h', ] ) # -h shows them in groups now.  lovely.

    ## Mutually Exclusive Options
# Defining mutually exclusive options is a special case of the option grouping feature.
# It uses add_mutually_exclusive_group() instead of add_argument_group()
parser = argparse.ArgumentParser( description="Mutually Exclusive Options", )
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', action='store_true' )
group.add_argument('-b', action='store_true' )
print parser.parse_args( ['-a', ], ) #( ['-h', ] )
print parser.parse_args( [ '-b', ] )
# ( -a A | -b B )

    ## Nesting Parsers
# The parent= parser approach from earlier is ~okay~, but there is another way - subparsers
parser = argparse.ArgumentParser( description="Nesting Parsers - Superparser", )
subparsers = parser.add_subparsers( help='commands', )

# This example is based around a program to work with file system directories
# A list command
list_parser = subparsers.add_parser( 'list', help="List Contents" )
list_parser.add_argument( 'dirname', action='store', help="Directory to list")
# A create command
create_parser = subparsers.add_parser( 'create', help="Create Directory" )
create_parser.add_argument( 'dirname', action='store', help="Directory to create")
create_parser.add_argument( '--read-only', action='store_true', default=False, help="Set read-only permission")
# A delete command
delete_parser = subparsers.add_parser( 'delete', help="Delete Directory" )
delete_parser.add_argument( 'dirname', action='store', help="Directory to delete")
delete_parser.add_argument( '--recursive', '-r', action='store_true', default=False, help="Remove directory contents as well.")

# Then when the arguments are parsed, the Namespace object returns only the relevant values.
print parser.parse_args( ['delete', '-r', 'foo' ] )

## 14.3.8 Advanced Argument Processing
# The examples so far have shown simple Boolean flags, options with strings or numerical arguments, and positional ones
# argparse also supports sophisticated argument specification for variable-length arguments lists, enumeration, and constants
    ## Variable Argument Lists
# A single argument definition can be configured to consume multiple arguments on the command line being parsed.
# Set nargs to one of the flag values below based on the number of required or expected arguments
    # N - The absolute number of arguments (i.e 3)
    # ? - 0 or 1 arguments
    # * - 0 or all arguments
    # + - all, and at least one, arguments

parser = argparse.ArgumentParser( description="Advanced Argument Processing - Variable Argument Lists", )
parser.add_argument('--three', nargs=3)
parser.add_argument('--optional', nargs='?')
parser.add_argument('--all', nargs='*', dest='all')
parser.add_argument('--one-or-more', nargs='+')
print parser.parse_args() # ( ['-h', ] )
print parser.parse_args( ['--three','a','b','c' ] )
print parser.parse_args( ['--optional', ] )
print parser.parse_args( ['--optional','ac' ] )
print parser.parse_args( ['--all','a','b','c' ] )
print parser.parse_args( ['--one-or-more','a','b','c' ] )
print parser.parse_args( ['--one-or-more','a' ] )

    ## Argument Types
# argparse treats all argument values as strings, unless it's told to convert the string to another type
# The type parameter to add_argument() defines a converter function, which is used by ArgumentParser
# to transform the argument value from a string to another type

parser = argparse.ArgumentParser(description="Advanced Argument Processing - Argument Types")

print parser.add_argument('-i', type=int)
print parser.parse_args( ['-i', "20" ])
print parser.add_argument('-f', type=float)
print parser.parse_args( ['-f', "3.14125926" ])

# Any callable that takes a single string argument can be passed as type
def parser_datetime( input ):
    hour, minute = input.split(':')
    return datetime.time( int(hour), int(minute) )

# To limit an input argument to a value within a predefined set, use the choices parameter
parser.add_argument('--time', type=parser_datetime, nargs='*', choices = (
    [ datetime.time(h, m) for m in xrange(0,60,10) for h in xrange(0,24) ]
))
print parser.parse_args( ['--time', "09:30", "12:10", "00:20" ])

    ## File Arguments
# Although file objects can be instantiated with a single string argument, that doesn't include access mode
# FileType provides a flexible way to provide file and buffer specifications
parser = argparse.ArgumentParser( description="Advanced Argument Processing - File Arguments" )
print parser.add_argument('-i', metavar='in-file', type=argparse.FileType('r'))
print parser.add_argument('-o', metavar='out-file', type=argparse.FileType('w'))

results = parser.parse_args(['-i' ,'data/14.3-argparse_fileargs-in.txt', '-o', 'data/14.3-argparse_fileargs-out.txt'])
print "Input  File:", results.i
print "Output File:", results.o

    ## Custom Actions
# In addition to the built in actions, custom actions can be defined by providing an object that implements the Action API
# The object passed as action to add_argument() should:
    # take parameters describing the argument being defined (all the same args as given to add_argument())
    # return a callable object that takes as parameters:
        # the parser processing the arguments,
        # the Namespace holding the parse results,
        # the value of the argument being acted upon, and
        # the option_string that triggered the action
        
# A class argparse.Action is provided as a convenient starting point for defining new actions
# The constructor handles the argument definitions, so only __call__() needs to be overridden in the subclass

class CustomAction( argparse.Action ):
    def __init__(self, option_strings, dest=None, nargs=None, 
        const=None, default=False, type=None, choices=None, 
        required=None, help=None, metavar=None
    ):
        argparse.Action.__init__(self, option_strings=option_strings, dest=dest, nargs=nargs, 
        const=const, default=default, type=type, choices=choices, 
        required=required, help=help, metavar=metavar)
        print "Initializing CustomAction"
        
        for name, value in sorted(locals().items()):
            if name == 'self' or value is None:
                continue
            print ' %s = %r' % (name, value)
        print
        return
        
    def __call__(self, parser, namespace, values, option_string=None):
        print "Processing Custom Action for '%s'" % self.dest
        print "\tParser = %s" % id(parser)
        print "\tValues = %r" % values
        print "\toption_string = %r" % option_string
        
        # Do some processing of input values
        if isinstance(values, list):
            values = [v.upper() for v in values ]
        else:
            values = values.upper()
        # Save the results in the namespace using the destination
        setattr(namespace, self.dest, values)
        print

parser = argparse.ArgumentParser( description="Advanced Argument Processing - Custom Actions" )
parser.add_argument('-a', action=CustomAction)
parser.add_argument('-m', action=CustomAction, nargs="*")
print parser.parse_args( ['-a', 'value', '-m', 'multivalue', 'second',] )

        


