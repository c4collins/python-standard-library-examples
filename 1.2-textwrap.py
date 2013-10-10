# encoding:utf-8
## 1.2 textwrap - Formatting Text Paragraphs
# The textwrap module can be used to format text or output when pretty-printing is desired.  It offers programmatic
# functionality similar to the paragraph wrapping or filling features found in many text editors.
import textwrap
import os
import base64

# Set up logging
import logging
logging.basicConfig( level=logging.DEBUG,
                     format="[%(levelname)-5s] %(asctime)s.%(msecs)d (%(name)s) %(message)s",
                     datefmt='%H:%M:%S',
                     )

# Argument Parsing
import argparse
argparser = argparse.ArgumentParser( description="Chapter 1 - Text - textwrap", add_help=True )
argparser.add_argument( '--section','-s', action='store', type=int, dest='section',
                        help="Enter the section number to see the results from that section.  "
                             "i.e for XX.YY.1, enter 1, for XX.YY.10 enter 10.",
                        )
results = argparser.parse_args()

## Constants
chapter_sections = [ { 'filename':'textwrap_sample_text.py'},
    {},
    {},
    {},
    {},
    {},
]
## Runtime Configuration
if results.section in xrange( 0, len(chapter_sections) ):
    logger = logging.getLogger("1.2 textwrap - Formatting Text Paragraphs")

    if results.section == 1 or results.section == 0:
        logger = logging.getLogger("1.2.1 Example Data")
        # The examples in this section use the following file, which will be created if it doesn't exist.
        filename = chapter_sections[0]['filename']
        if not os.path.isfile( filename ):
            with open( filename, 'w') as f:
                f.write(base64.b64decode("""c2FtcGxlX3RleHQgPSAiIiINCiAgICBUaGUgdGV4dHdyYXAgbW9kdWxlIGNhbiBiZSB1c2VkIHRvIGZ\
                vcm1hdCB0ZXh0IGZvciBvdXRwdXQgaW4NCiAgICBzaXR1YXRpb25zIHdoZXJlIHByZXR0eS1wcmludGluZyBpcyBkZXNpcmVkLiAgSXQgb2\
                ZmZXJzDQogICAgcHJvZ3JhbW1hdGljIGZ1bmN0aW9uYWxpdHkgc2ltaWxhciB0byB0aGUgcGFyYWdyYXBoIHdyYXBwaW5nDQogICAgb3IgZ\
                mlsbGluZyBmZWF0dXJlcyBjb3VudCBpbiBtYW55IHRleHQgZWRpdG9ycy4NCiAgICAiIiINCg=="""
                ))

    if results.section == 2 or results.section == 0:
        logger = logging.getLogger("1.2.2 Filling Paragraphs")
        # fill() takes text as an input and produces formatted text.
        # Sort of.  It combines the lines, but all the whitespace remains, including spaces/indents from linebreaks.
        from textwrap_sample_text import sample_text
        logger.info("No dedent:\n%s", textwrap.fill(sample_text, width=50))


    if results.section == 3 or results.section == 0:
        logger = logging.getLogger("1.2.3 Removing Existing Indentation")
        # Removing the whitespace prefix from all lines in the sample text produces better results and allows for
        # the use of docstrings or embedded multiline strings straight from python code whil;e removing code formatting.
        from textwrap_sample_text import sample_text
        logger.info("Dedented:\n%s", textwrap.dedent(sample_text))

    if results.section == 4 or results.section == 0:
        logger = logging.getLogger("1.2.4 Combining Dedent and Fill")
        # Obviously, the thing to do is pass the dedented text into fill with some arbitrary length.
        from textwrap_sample_text import sample_text
        for width in [ 4, 8, 15, 16, 23, 42, 55, 72, 80  ]:
            logger.info("%d Columns Wide:\n%s", width, textwrap.fill(textwrap.dedent(sample_text), width=width))

    if results.section == 5 or results.section == 0:
        logger = logging.getLogger("1.2.5 Hanging Indents")
        # Just as the width of the output can be set, the indent of the first line can be controlled independently
        from textwrap_sample_text import sample_text
        for width in [ 42, 75  ]:
            logger.info("%d Columns Wide:\n%s", width, textwrap.fill(
                    textwrap.dedent(sample_text),
                    width=width,
                    initial_indent='',
                    subsequent_indent=" "*4,
                    ))
else:
    # If the command isn't recognized because it wasn't given, show the help.
    if not results.section:
        argparser.parse_args(['-h'])
    else:
        # If the command isn't recognized because it"s wrong, show an error.
        logger = logging.getLogger("ERROR")
        logger.warning("Command not recognized: %s", results.section)
