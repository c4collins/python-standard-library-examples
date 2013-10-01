# encoding:utf-8
## 13.2 smtpd - Simple Mail Servers
# The smtpd module includes classes for building simple mail transport protocol servers.
# It is the server side of the protocol used by smtplib.
import smtpd
import asyncore

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 13 - Email - smtpd", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Functions

## Classes
class CustomSMTPServer( smtpd.SMTPServer ):
    logger = logging.getLogger("CustomSMTPServer")
    def process_message(self, peer, mailfrom, rcpttos, data):
        logger.info('Receiving message from: %s', peer)
        logger.info('Message addressed from: %s', mailfrom)
        logger.info('Message addressed to  : %s', rcpttos)
        logger.info('Message length        : %s', len(data))
        logger.info('Message               :\n%s', data)


## Constants
chapter_sections = [ {},
    {},
    {},
    {},
]

## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections) ):
    logger = logging.getLogger("13.2 smtpd - Simple Mail Servers")

    if results.section == 1:
        logger = logging.getLogger("13.2.1 Mail Server Base Class")
        # The base class for all the provided example servers is SMTPServer.
        # It handles communicating with the client and receiving incoming data, and provides a convenient hook to
        # override so the message can be processed once it is fully available.
        # The constructor arguments are the local address to listen for connections and
        # the remote address where proxied messages should be delivered
        # The method process_message() is provided as a hook to be overridden by a derived class.
        # It is called when the message is completely received, and is given these arguments:
            # peer - The client's address, a tuple containing IP and port
            # mailfrom - The message envelope's From infromation.
            # rcpttos - List of message recipients from the message envelope.
            # data - the full RFC 2882 message body.
        # The default implementation of process_message() raises a NotImplementedError
        # This example defines a sublclss that overrides the method to print information about the messages it receives.
        server = CustomSMTPServer(( "192.168.1.150", 1025), None)

        # SMTPServer requires asyncore, so to run the server we cal; asyncore.loop()
        asyncore.loop()

    if results.section == 2:
        logger = logging.getLogger("13.2.2 Debugging Server")
        # The previous example shows the arguments to process_message(), but smtpd also includes a server specifically
        # designed for more complete debugging, called DebuggingServer.  It prints the entrie incoming message to the
        # console, then stops processing (it doesn't proxy the message to a real mail server)
        server = smtpd.DebuggingServer(( "192.168.1.150", 1025), None)
        asyncore.loop()

    if results.section == 3:
        logger = logging.getLogger("13.2.3 Proxy Server")
        # The PureProxy class implements a straightforward proxy server.  incoming messages are forwarded upstream to
        # the server given as an argument to the constructor.
        # WARNING: Running this has a good chance to make you into an open relay.
        server = smtpd.PureProxy(( "192.168.1.150", 1025), ('192.168.1.160', 1025))
        asyncore.loop()

else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
