# encoding:utf-8
## 14.8 ConfigParser
# Use the ConfigParser module to manage user-editable configuration files for an application.
# The contents of the configuration files can be organized into groups, abd several option-value types are supported,
# including integers, floating-point values, and Booleans.  Option values can be combined using Python formating strings
# to build longer values such as URLs from shorter values like hostnames and port numbers.
import ConfigParser
import codecs
import sys

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 14 - Application Building Blocks - ConfigParser", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Functions

## Classes

## Constants
chapter_sections = [ { 'filename':"14.8-ConfigParser_configfile.ini", },
    {},
    { 'unicode_filename':"14.8-ConfigParser_configfile_unicode.ini", },
    { 'types':"14.8-ConfigParser_types.ini", 'allow_no_value':"14.8-ConfigParser_allow_no_value.ini", },
    {},
    {},
    { 'search':"14.8-ConfigParser_option-search-path.ini", },
    { 'interpolation':"14.8-ConfigParser_interpolation.ini", 'defaults':"14.8-ConfigParser_defaults.ini", },
]

## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections) ):
    logger = logging.getLogger("14.8 ConfigParser - Work with Configuration Files")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("14.8.1 Configuration File Format")
        # The file format used by ConfigParser is similar to the format used by older versions of Microsoft Windows.
        # It consists of one or more named sections, each of which can contain individual options with names and values.
        # Config file sections are identified by looking for lines starting with [ and ending with ].
        # The value between the brackets is the section name and can contain any characters except square brackets.
        # Options are listed one per line within a section.  The line starts with the name of the option, which is
        # separated from the value by a colon or an equal sign.  Whitespace around the separator is ignored on parsing.
        # This sample config file has a section names "bug_tracker" with three options.
        with open(chapter_sections[0]['filename'], 'w') as f:
            logger.info("Writing file: %s",chapter_sections[0]['filename'])
            f.write("[bug_tracker]\n")
            f.write("url = http://192.168.1.150:8080/bugs/\n")
            f.write("username = server\n")
            f.write("password = SECRET\n")
            f.write("\n")
            f.write("[wiki]\n")
            f.write("url = http://192.168.1.150:8080/wiki/\n")
            f.write("username = server\n")
            f.write("password = SECRET\n")

    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("14.8.2 Reading Configuration Files")
        # The most common use for configuration files is to have a user or systems administrator edit the file with a
        # regular text editor to set application behaviour defaults and then have the application read the file, parse
        # it, and act based on its contents.  Use the read() method of SafeConfigParser to read the configuration data.
        parser = ConfigParser.SafeConfigParser()
        logger.info("Reading file: %s",chapter_sections[0]['filename'])
        parser.read( chapter_sections[0]['filename'] )
        logger.info( "Username: %s", parser.get( 'bug_tracker', 'username') )
        logger.info( "URL     : %s", parser.get( 'bug_tracker', 'url') )

        # The read method also accepts a list of filenames; each name in turn is scanned and, if the file exists, opened
        # and read.
        parser = ConfigParser.SafeConfigParser()
        logger.info("Reading file: %s",chapter_sections[0]['filename'])
        logger.info("Reading file: %s", 'not_a_file.ini')
        candidates = [chapter_sections[0]['filename'], chapter_sections[2]['unicode_filename'], 'not_a_file.ini' ]
        # read() returns a list containing the names of the files successfully loaded, so the program can discover
        # whhich config files are missing and if those absences are acceptable.
        found = parser.read( candidates )
        missing = set(candidates) - set(found)
        logger.info("These files were loaded: %r", sorted(found) )
        logger.info("These files are missing: %r", sorted(missing) )

        # Config files containing Unicode data should be opened using the codecs module to set the proper encoding value
        # changing the password value of the original input to contain Unicode characters and saving the results in
        # UTF-8 encoding.
        with open(chapter_sections[2]['unicode_filename'], 'w') as f:
            logger.info("Writing file: %s",chapter_sections[2]['unicode_filename'])
            f.write("[bug_tracker]\n")
            f.write("url = http://192.168.1.150:8080/bugs/\n")
            f.write("username = server\n")
            f.write("password = An ḃfuil do ċroí ag bualaḋ ó ḟaitíos an ġrá a ṁeall lena ṗóg éada ó ṡlí do leasa ṫú\n")

        # The codecs file handle can be passed to readfp() which uses readline() to get and parse lines from the file.
        parser = ConfigParser.SafeConfigParser()
        logger.info("Reading file: %s",chapter_sections[2]['unicode_filename'])
        with codecs.open( chapter_sections[2]['unicode_filename'], 'r', encoding='utf-8' ) as f:
            parser.readfp(f)

        password = parser.get('bug_tracker', 'password')
        logging.info("Password: %s", password.encode('utf-8') )
        logging.info("Type    : %s", type(password) )
        logging.info("repr    : %r", repr(password) )

    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("14.8.3 Accessing Configuration Settings")
        # SafeConfigParser includes methods for examining the structure of the parsed configuration, including listing
        # the sections and options, and getting their values.  The configuration file includes two sections for separate
        # web services.
        parser = ConfigParser.SafeConfigParser()
        parser.read(chapter_sections[0]['filename'])

        for section_name in parser.sections():
            logger.info('Section: %s', section_name )
            logger.info("Options: %s", parser.options(section_name))
            for name, value in parser.items(section_name):
                logger.info("\t%s: %s", name, value)

        # To test if a section exists, use has_section(), passing the section name.
        # Testing if a section exists before using get is a good way to avoid exceptions for missing data
        sections = ['wiki', 'bug_tracker', 'dvcs']
        options = ['url', 'username', 'password', 'description']
        for section in sections:
            logger.info("%-12s: %s", section, parser.has_section(section) )
            # Use has_option() to test if an option exists within a section
            for option in options:
                has_option = parser.has_option(section, option)
                logger.info("%s.%-12s: %s", section, option, has_option)

        # All section and option names are treated as strings, but option values can be strings, integers, floating-
        # point numbers, and Booleans.  There is a range of possible Boolean values that are converted to true or false.
        # This example shows one of each type.
        parser = ConfigParser.SafeConfigParser()
        parser.read(chapter_sections[3]['types'])

        logger.info("Integers:")
        for name in parser.options('ints'):
            string_value = parser.get('ints', name)
            value = parser.getint('ints', name)
            logger.info("\t%-12s : %-7r -> %d", name, string_value, value)

        logger.info("Floats:")
        for name in parser.options('floats'):
            string_value = parser.get('floats', name)
            value = parser.getfloat('floats', name)
            logger.info("\t%-12s : %-7r -> %0.2f", name, string_value, value)

        logger.info("Booleans:")
        for name in parser.options('Booleans'):
            string_value = parser.get('Booleans', name)
            value = parser.getboolean('Booleans', name)
            logger.info("\t%-12s : %-7r -> %s", name, string_value, value)

        # Usually, the parser requires an explicit value for each option, but with the SafeConfigParser parameter
        # allow_no_value set to True, an option can appear by itself on a line in the input file and be used as a flag

        # require values
        try:
            parser = ConfigParser.SafeConfigParser()
            parser.read( chapter_sections[3]['allow_no_value'] )
        except ConfigParser.ParsingError, err:
            logger.debug("Could not parse: %s", err)

        # Allow stand-alone option names
        logger.info("Trying again with allow_no_value=True")
        parser = ConfigParser.SafeConfigParser( allow_no_value=True )
        parser.read( chapter_sections[3]['allow_no_value'] )
        for flag in ['turn_thing_on', 'turn_other_thing_on']:
            logger.info( flag )
            exists = parser.has_option('flags', flag)
            logger.info("has_option : %s", exists)
            # when an option has no explicit value, has_option() reports that the option exists and get() returns None.
            if exists:
                logger.info( "%10s : %s", "get", parser.get('flags', flag) )


    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("14.8.4 Modifying Settings")
        # While SafeConfigParser is primaril intended to be configured by reading settings from files, settings can
        # also be populated by calling add_section() to create a new section and set() to add or change an option.
        parser = ConfigParser.SafeConfigParser()

        parser.add_section('bug_tracker')
        parser.add_section('wiki')
        # All options must be set as strings, even if they will be retrieved as integer, float, or Boolean.
        parser.set('bug_tracker', 'url', 'http://192.168.1.150:8080/bugs/')
        parser.set('bug_tracker', 'username', 'server')
        parser.set('bug_tracker', 'password', 'SECRET')
        parser.set('wiki', 'url', 'http://192.168.1.150:8080/wiki/')

        logger.info("After adding sections and options:")
        for section in parser.sections():
            logger.info(section)
            for name, value in parser.items(section):
                logger.info("%10s = %r", name, value)

        # Sections and options can be removed from a SafeConfigParser with remove_section() and remover_option().
        parser.remove_option('bug_tracker', 'password')
        # Removing a section removes all options it contains.
        parser.remove_section('wiki')

        logger.info("After removing sections and options:")
        for section in parser.sections():
            logger.info(section)
            for name, value in parser.items(section):
                logger.info("%10s = %r", name, value)


    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("14.8.5 Saving Configuration Files")
        # Once a SafeConfigParser is populated with desired data, it can be saved to a file by calling the write()
        # method.  This makes it possible to provide a user interface for editing the configuration settings, without
        # having to write any code to manage the file.
        parser = ConfigParser.SafeConfigParser()

        parser.add_section('bug_tracker')
        parser.set('bug_tracker', 'url', 'http://192.168.1.150:8080/bugs/')
        parser.set('bug_tracker', 'username', 'server')
        parser.set('bug_tracker', 'password', 'SECRET')

        # The write method takes a file-like object as the argument.  it writes the data out in the INI format so it
        # can be parsed again by SafeConfigParser
        parser.write(sys.stdout)

    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("14.8.6 Option Search Path")
        # SafeConfigParser uses a multistep search process when looking for an option.  Before starting the option
        # search, the section name is tested.
            # If the section does not exist, and the name is not the special value DEFAULT, NoSectionError is raised.
            # If the option name appears in the vars dictionary passed to get(), the value from vars is returned
            # If the option name appears in the specified section, the value from that section is returned
            # If the option name appears in the DEFAULT section, that value is returned
            # If the option name appears in the defaults dictionary passed to the constructor, that value is returned.
            # If the name is not found in any of these locations NoOptionError is raised.
        option_names = ['from-default',
                        'from-section', 'section-only',
                        'file-only', 'init-only', 'init-and-file',
                        'from_vars',
                        ]
        # Initialize the parser with some defaults
        parser = ConfigParser.SafeConfigParser(
            defaults = {
                'from-default':'value from defaults passed to init',
                'init-only':'value from defaults passed to init',
                'init-and-file':'value from defaults passed to init',
                'from-section':'value from defaults passed to init',
                'from-vars':'value from defaults passed to init',
            }
        )

        logging.info( "Defaults before loading file:")
        defaults = parser.defaults()
        for name in option_names:
            if name in defaults:
                logger.info("\t%-15s = %r", name, defaults[name])

        # Load the config file
        parser.read( chapter_sections[6]['search'])

        logging.info( "Defaults after loading file:")
        defaults = parser.defaults()
        for name in option_names:
            if name in defaults:
                logger.info("\t%-15s = %r", name, defaults[name])

        # Define some local overrides
        vars = {'from-vars':'value from vars'}

        # Show the values of all the options
        logger.info( "\nOption Lookup:")
        for name in option_names:
            value = parser.get('sect', name, vars=vars)
            logger.info("\t%-15s = %r", name, value)

        # Show error messages for options that do not exist
        logger.info("\n Error cases:")

        try:
            logger.debug("No such options : %s", parser.get('sect', 'no-option'))
        except ConfigParser.NoOptionError, err:
            logger.error( str(err) )

        try:
            logger.debug("No such section : %s", parser.get('no-sect', 'no-option'))
        except ConfigParser.NoSectionError, err:
            logger.error( str(err) )

    if results.section == 7 or results.section == 0:
        logger = logging.getLogger("14.8.7 Combining Values with Interpolation")
        # SafeConfigParser provids a feature called interpolation hat can be used to combine values together.  Values
        # containing standard Python format strings trigger the interpolation feature when they are retrieved with get()
        # Options named within the value being fetched are replaced with their values in turn, until no more
        # substitution is necessary.

        # The URL examples from earlier in the section can be rewritten to use interpolation to make it easier to change
        # only part of the value.  For example, this configuration file separates the protocol, hostname, and port.
        parser = ConfigParser.SafeConfigParser()

        parser.add_section('bug_tracker')
        parser.set('bug_tracker', 'protocol', 'http')
        parser.set('bug_tracker', 'server_host', 'localhost')
        parser.set('bug_tracker', 'port', '8080')
        parser.set('bug_tracker', 'url', '%(protocol)s://%(server_host)s:%(port)s/bugs/')
        parser.set('bug_tracker', 'username', 'server')
        parser.set('bug_tracker', 'password', 'SECRET')

        # The write method takes a file-like object as the argument.  it writes the data out in the INI format so it
        # can be parsed again by SafeConfigParser
        with open( chapter_sections[7]['interpolation'], mode='w' ) as f:
            parser.write(f)

        parser = ConfigParser.SafeConfigParser()
        parser.read( chapter_sections[7]['interpolation'] )

        # interpolation is done each time get() is called
        logger.info("Original: %s", parser.get('bug_tracker', 'url'))
        parser.set('bug_tracker', 'port', '8002')
        # Because interpolation is done by get() changes made to one part of url changes the return value
        logger.info("New port: %s", parser.get('bug_tracker', 'url'))
        logger.info("Without interpolation: %s", parser.get('bug_tracker', 'url', raw=True))

        # Values for interpolation do not need to appear in the same section as the original option
        # Defaults can be mixed with override values.  With this config file, the value for URL comes from the DEFAULT
        # section.
        parser = ConfigParser.SafeConfigParser()
        parser.read( chapter_sections[7]['defaults'] )

        logger.info( "Tracker URL: %s", parser.get('bug_tracker', 'url'))
        logger.info( "Default URL: %s", parser.get('DEFAULT', 'url'))

        # Substitution stops after MAX_INTERPOLATION_DEPTH steps to avoid problems due to recursive references

        parser = ConfigParser.SafeConfigParser()

        parser.add_section('sect')
        parser.set('sect', 'opt', '%(opt)s')
        parser.set('sect', 'url', 'http://%(server)s:%(port)s/bugs/')

        try:
            logger.info( parser.get('sect', 'opt'))
        # An InterpolationDepthError is raised if there are too many substitution steps
        except ConfigParser.InterpolationDepthError, err:
            logger.error( err )

        try:
            logger.info( parser.get('sect', 'url'))
        # An InterpolationMissingOptionError is raised if there are missing values
        except ConfigParser.InterpolationMissingOptionError, err:
            logger.error( err )

else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        argparser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
