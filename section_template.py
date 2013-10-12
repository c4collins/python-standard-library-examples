# encoding:utf-8
## 10.4 multiprocessing - Manage Processes like Threads
#

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 10 - Processes and Threads - multiprocessing", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Constants
chapter_sections = [ {},
    {},{},{},{},{},{},{},{},{},
    {},{},{},{},{},{},{},{},{},
]
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections) ):
    logger = logging.getLogger("10.4 multiprocessing - Manage Processes like Threads")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("10.4.1 Multiprocessing Basics")
        #
    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("10.4.2 Importable Target Functions")
        #
    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("10.4.3 Determining the Current Process")
        #
    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("10.4.4 Daemon Processes")
        #
    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("10.4.5 Waiting for Processes")
        #
    if results.section == 6 or results.section == 0:
        logger = logging.getLogger("10.4.6 Terminating Processes")
        #
    if results.section == 7 or results.section == 0:
        logger = logging.getLogger("10.4.7 Process Exit Status")
        #
    if results.section == 8 or results.section == 0:
        logger = logging.getLogger("10.4.8 Logging")
        #
    if results.section == 9 or results.section == 0:
        logger = logging.getLogger("10.4.9 Subclassing Process")
        #
    if results.section == 10 or results.section == 0:
        logger = logging.getLogger("10.4.10 Passing Messages to Processes")
        #
    if results.section == 11 or results.section == 0:
        logger = logging.getLogger("10.4.11 Signalling Between Processes")
        #
    if results.section == 12 or results.section == 0:
        logger = logging.getLogger("10.4.12 Controlling Access to Resources")
        #
    if results.section == 13 or results.section == 0:
        logger = logging.getLogger("10.4.13 Synchronizing Operations")
        #
    if results.section == 14 or results.section == 0:
        logger = logging.getLogger("10.4.14 Controlling Concurrent Access to Resources")
        #
    if results.section == 15 or results.section == 0:
        logger = logging.getLogger("10.4.15 Managing Shared State")
        #
    if results.section == 16 or results.section == 0:
        logger = logging.getLogger("10.4.16 Shared Namespaces")
        #
    if results.section == 17 or results.section == 0:
        logger = logging.getLogger("10.4.17 Process Pools")
        #
    if results.section == 18 or results.section == 0:
        logger = logging.getLogger("10.4.18 Implmenting MapReduce")
        #

else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        argparser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
