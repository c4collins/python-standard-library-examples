# encoding:utf-8
## 13.1 smtplib - Simple Mail Transfer Protocol Client
# smtplib includes the class SMTP, which can be used to communicate with mail servers to send mail.
import smtplib
import email.utils
import getpass
from email.mime.text import MIMEText


# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 13 - Email - smtplib", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Functions

## Classes

## Constants
chapter_sections = [ { 'host':"192.168.1.150", 'port':1025},
    {
        'message':"This is the body of the message.",
        'Subject':"Test Message",
        'To':"connor@bittchinsdesign.ca",
        'From':"contact@bittchinsdesign.ca",
    },
    {},
    {},
]

## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections)+1 ):
    logger = logging.getLogger("13.1 smtplib - Simple Mail Transfer Protocol Client")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("13.1.1 Sending an Email Message")
        # The most common use of SMTP is to connect to a mail server and send a message.
        # This mail server host name and port can be passed to the constructor, or connect() can be invoked explicitly.
        # Once connected, call sendmail() with the envelope parameters and the body of the message.
        # The message text should be compliant with RFC2882 (as smtplib does not modify the contents or headers).
        # That means the caller needs to add the From: and To: headers.

        msg = MIMEText( chapter_sections[1]['message'])
        msg['To'] = email.utils.formataddr(( 'Recipient', chapter_sections[1]['To'] ))
        msg['From'] = email.utils.formataddr(( 'Author', chapter_sections[1]['From'] ))
        msg['Subject'] = chapter_sections[1]['Subject']

        server = smtplib.SMTP(chapter_sections[0]['host'], chapter_sections[0]['port'])
        server.set_debuglevel(True) # show communications with the server

        try:
            # Note that the sender/recipient could be different here than in the message headers, allowing for BCC.
            server.sendmail( msg['From'], [ msg['To'], 'connor.collins@gmail.com', ], msg.as_string() )
        finally:
            server.quit()

    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("13.1.2 Authentication and Encryption")
        # The SMTP class also handles authentication and TLS encryption, when the server supports them.
        # to determine if the server supports TLS, call ehlo() directly to identify the client to the server
        # and ask what extensions are available.
        # Then call has_extn() to check the results.
        # After TLS is started, ehlo() must be called again before authenticating

        # Prompt the user for connection info
        to_email = raw_input("Recipient: ")
        servername = raw_input("Mail server name: ")
        username = raw_input("Username: ")
        password = getpass.getpass("%s's password: " % username)

        # Create the message
        msg = MIMEText("Test message text from 13.1.2 Authentication and Encryption.")
        msg.set_unixfrom('author')
        msg['To'] = email.utils.formataddr(("Recipient", to_email))
        msg['From'] = email.utils.formataddr(("Author", 'contact@bittchinsdesign.ca'))
        msg['Subject'] = "13.1.2 Authentication and Encryption"

        server = smtplib.SMTP(servername)
        try:
            server.set_debuglevel(False)

            # Identify ourselves
            server.ehlo()

            # If we can encrypt this session, do it.
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo() # eridentify ourselves over TLS

            server.login(username, password)

            server.sendmail( 'contact@bittchinsdesign.ca', [to_email, 'connor.collins@gmail.com', ], msg.as_string() )
        finally:
            server.quit()

    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("13.1.3 Verifying an Email Address")
        # The SMTP protocol includes a command to ask a server whether an address is valid.
        # Usually VRFY is disabled to prevent spammers from finding legitimate email addresses.
        # But if it is enabled, a client can ask the server about an address and receive a status code indicating
        # validity, along with the users's Full Name, if it is available.

        server = smtplib.SMTP(chapter_sections[0]['host'], chapter_sections[0]['port'])
        server.set_debuglevel(True) # show communications with the server
        addresses = ['admin', 'contact', 'webmaster',]

        try:
            for address in addresses:
                logger.info("%s : %s", address, server.verify(address) )
        finally:
            server.quit()


else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        parser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
