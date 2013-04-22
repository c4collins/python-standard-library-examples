# -*- coding: utf-8 -*-
import re

pattern = 'this'
text = 'Does this text match the pattern?'


## Simple text match
match = re.search(pattern, text)

s = match.start()
e = match.end()

print 'Found "%s"\nin "%s"\nfrom %d to %d ("%s")' % (match.re.pattern, match.string, s, e, text[s:e])


## Compiling RegexObjects

regexes = [ re.compile(p)
			for p in ['this', 'that']
			]

print "Text: %r\n" % text

for regex in regexes:
	print 'Seeking "%s" ->' % regex.pattern,

	if regex.search(text):
		print "Match!"
	else:
		print "No match!"

## Multiple Matches

text = 'abbaaabbbbaaaaa'
pattern = 'ab'

 # findall returns all non-overlapping substrings that match
for match in re.findall(pattern, text):
    print 'Found "%s"' % match

 # finditer produces Match instances rather than strings

for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print 'Found "%s" at %d:%d' % (text[s:e], s, e)

## Pattern Syntax

def test_patterns(text, patterns=[]):
    """Given source text and a list of patterns, look for matchs for each pattern within the text and print them to stdout"""
    # Look for each pattern in the text and print the results
    for pattern, desc, in patterns:
        print "Pattern %r (%s)\n" % (pattern, desc)
        print ' %r' % text
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = '.' * (s + n_backslashes)
            print ' %s%r' % (prefix, substr)
        print
    return

test_patterns(text, [
    (pattern, "'a' followed by 'b'."),
                    ])

## Repetition

test_patterns( 'abbaabbba',
            [ ('ab*', "'a' followed by 0 or more 'b'"),
              ('ab+', "'a' followed by 1 or more 'b'"),
              ('ab?', "'a' followed by 0 or 1 'b'"),
              ('ab{3}', "'a' followed by three 'b'"),
              ('ab{2,3}', "'a' followed by two or three 'b'"),
            ])
 # ? means Don't be greedy
test_patterns( 'abbaabbba',
            [ ('ab*?', "'a' followed by 0 or more 'b'"),
              ('ab+?', "'a' followed by 1 or more 'b'"),
              ('ab??', "'a' followed by 0 or 1 'b'"),
              ('ab{3}?', "'a' followed by three 'b'"),
              ('ab{2,3}?', "'a' followed by two or three 'b'"),
            ])

## Character Sets

test_patterns( 'abbaabbba',
            [ ('[ab]', "either 'a' or 'b'"),
              ('a[ab]+', "'a' followed by 1 or more 'a' or 'b'"),
              ('a[ab]+?', "'a' followed by 1 or more 'a' or 'b', not greedy"),
            ])
 # the caret (^) means to look for characters NOT in the set following
test_patterns('This is some text -- with punctuation.',
            [ ('[^-. ]+', "Sequences without '-', '.', or ' '"),
            ])
 # character ranges are enclosed in square brackets, like [a-zA-Z]
test_patterns('This is some text -- with punctuation.',
            [ ('[a-z]+', "sequences of lowercase letters"),
              ('[A-Z]+', "sequences of uppercase letters"),
              ('[a-zA-Z]+', "sequences of lowercase or uppercase letters"),
              ('[A-Z][a-z]+', "sequences of uppercase followed by lowercase letters"),
            ])
 # use a period (.) to indicate a match with any character
test_patterns( 'abbaabbba',
            [ ('a.', "'a' followed by a single character"),
              ('b.', "'b' followed by a single character"),
              ('a.*b', "'a' followed any number of characters and then a 'b'"),
              ('a.*?b', "'a' followed any number of characters and then a 'b', not greedy"),
            ])

## Escape Codes

 # \d is a digit
 # \D is a non-digit
 # \s is whitespace (space, tab, newline, etc.)
 # \S is non-whitespace
 # \w is alphanumeric
 # \W is non-alphanumeric

test_patterns( 'A prime #1 example!',
        [ ( r'\d+', 'sequence of digits' ),
          ( r'\D+', 'sequence of non-digits' ),
          ( r'\s+', 'sequence of whitespace' ),
          ( r'\S+', 'sequence of non-whitespace' ),
          ( r'\w+', 'sequence of alphanumerics' ),
          ( r'\W+', 'sequence of non-alphanumerics' ),
        ])
 # backslashes can be used to escape characters that would otherwise be interpreted as regex codes
test_patterns( r'\d+ \D+ \s+',
        [ ( r'\\.\+', 'escape code'),
        ])

## Anchoring

 # ^ is the start of a string or line
 # $ is the end of a string or line
 # \A is the start of a string
 # \Z is the end of a string
 # \b is an empty string a tthe beginning or end of a word
 # \B is an empty string not at the beginning or end of a word

test_patterns( 'This is some text -- with punctuation.',
        [ ( r'^\w+', 'word at start of string'),
          ( r'\A\w+', 'word at start of string'),
          ( r'\w+\S*$', 'word near end of string, skip punctuation'),
          ( r'\w+\S*\Z', 'word near end of string, skip punctuation'),
          ( r'\w*t\w*', 'word containing "t"'),
          ( r'\bt\w+', '"t" at start of word'),
          ( r'\w+t\b', '"t" at end of word'),
          ( r'\Bt\B', '"t" not at start or end of word'),
        ])

## Constraining the Search

 # match() will just check for a match at the start of an input
 # search() will search the whole input to find a match
text = "This is some text -- with punctuation."
pattern = 'is'
print "Text   : ", text
print "Pattern: ", pattern

m = re.match(pattern, text)
print "Match  : ", m
s = re.search(pattern, text)
print "Search : ", s

print
pattern = re.compile(r'\b\w*is\w*\b')

print "Text   : ", text
print "Pattern: ", pattern

pos = 0
while True:
        match = pattern.search(text, pos)
        if not match:
                break
        s = match.start()
        e = match.end()
        print '  %2d : %2d = "%s"' % (s, e-s, text[s:e])
        # move forward in position for the next search
        pos = e
print

## Pattern Groups

test_patterns( 'abbaaabbbbaaaaa',
        [ ('a(ab)', '"a" followed by literal "ab"' ),
          ('a(a*b*)', '"a" followed by 0-n "a" and 0-n "b"' ),
          ('a(ab)*', '"a" followed by 0-n "ab"' ),
          ('a(ab)+', '"a" followed by 1-n "ab"' ),
        ])

 # match substrings from indivisual groups within a pattern with the groups() method of the Match object

print text
print

patterns = [
        ( r'^(\w+)', 'word at start of string'),
        ( r'(\w+)\S*$', 'word at end, with optional punctuation'),
        ( r'(\bt\w+)\W+(\w+)', 'word starting with "t", and the following word'),
        ( r'(\w+t)\b', 'word ending with "t"'),
        ]

for pattern, desc in patterns:
        regex = re.compile(pattern)
        match = regex.search(text)
        print 'Pattern %r (%s)\n' % (pattern, desc)
        print ' ', match.groups()
        print

print
print 'Input text            : ', text

 # word starting with "t" and then another word
regex = re.compile(r'(\bt\w+)\W+(\w+)')
print 'Pattern               : ', regex.pattern

match = regex.search(text)
print 'Entire match          : ', match.group(0)

print 'Word starting with "t": ', match.group(1)
print 'Word after "t" word   : ', match.group(2)

 # name groups with the syntax (?P<name>pattern)
 # retrieve the dict that contains the name with groupdict()
print
print text
print

for pattern in [ r'^(?P<first_word>\w+)',
                 r'(?P<last_word>\w+)\S*$',
                 r'(?P<t_word>\bt\w+)\W+(\w+)',
                 r'(?P<ends_with_t>\w+t)\b',
                ]:
        regex = re.compile(pattern)
        match = regex.search(text)
        print 'Matching "%s" ' % pattern
        print '  ', match.groups()
        print '  ', match.groupdict()
        print

def test_patterns2(text, patterns=[]):
    """Given source text and a list of patterns, look for matches for each pattern within the text and print them to stdout"""
    # look for each pattern in the text and print the results
    for pattern, desc in patterns:
        print 'Pattern %r (%s) \n' % (pattern, desc)
        print '  %r' % text
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = ' ' * (s)
            print '  %s%s%s ' % (prefix, text[s:e], ' '*(len(text)-e)),
            print match.groups()
            if match.groupdict():
                print '%%s' % ( ' ' * (len(text)-s), match.groupdict())
        print
    return

test_patterns2( 'abbaabbba', [ ( r'a((a*)(b*))', 'a followed by 0-n "a" and 0-n "b"' ) ] )

 # Use the pipe symbol (|) to OR groups, but be careful
test_patterns2( 'abbaabbba',
            [ ( r'a((a+)|(b+))', '"a" then a sequence of "a" or a sequence of "b"' ),
              ( r'a((a|b)+)', '"a" then a sequence of (ab)' ),
            ])

 # create noncapturing groups with the syntax (?:pattern)

test_patterns2( 'abbaabbba',
            [ ( r'a((a+)|(b+))', 'capturing form' ),
              ( r'a((?:a+)|(?:b+))', 'non-capturing form' ),
            ])

## Search Options

 # re.IGNORECASE causes lereral characters and charater ranges in thhe pattern to match
 # both uppercase and lowercase letters (Oh, yeah, that surprises me)
pattern = r'\bT\w+'
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print "Test:\n %r" % text
print "Pattern:\n %s" % pattern
print "Case-sensitive:"
for match in with_case.findall(text):
    print ' %r' % match
print "Case-insensitive:"
for match in without_case.findall(text):
    print ' %r' % match
print

 # re.MULTILINE makes the '^' and '$' anchors apply to each line, as well as the entire input
text = "This is some text -- with punctuation.\nAnd a second line!"

pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

print "Text:\n %r" % text
print "Pattern:\n %s" % pattern
print "Single Line :"
for match in single_line.findall(text):
        print " %r" % (match,)
print "Multiline   :"
for match in multiline.findall(text):
        print " %r" % (match,)
print

 # usually the period (.) matches everythign but newlines, re.DOTALL makes it also match newlines.
pattern = r'.+'
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print "Text:\n %r" % text
print "Pattern:\n %s" % pattern
print "Single Line :"
for match in no_newlines.findall(text):
        print " %r" % (match,)
print "Multiline   :"
for match in dotall.findall(text):
        print " %r" % (match,)
print

 # re expects ASCII input and output, but you can make it expect Unicode with re.UNICODE
 # in Python 2, anyway.  Python 3 defaults ot Unicode, so, you know.

import codecs
import sys

   # Set stdout encoding to UTF-8. This broke IDLE's shell for me, but it works without it
   # sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)

u_text = u'Français złoty Österreich'
pattern = ur'\w+'
ascii_pattern = re.compile(pattern)
unicode_pattern = re.compile(pattern, re.UNICODE)

print 'Text    :', text
print 'Pattern :', pattern
print 'ASCII   :', u', '.join(ascii_pattern.findall(u_text))
print 'Unicode :', u', '.join(unicode_pattern.findall(u_text))
print

 # Verbose Expression Syntax allows for whitespace and comments in what would otherwise quickly
 # become untenable statments to understand or manage (via re.VERBOSE)

terse_address = re.compile('[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)', re.UNICODE)
verbose_address = re.compile(
        '''
        [\w\d.+-]+      # username
        @
        ([\w\d.]+\.)+   # domain name prefix
        (com|org|edu)   # TODO: support more TLDs
        ''',
        re.UNICODE | re.VERBOSE )
expanded_address = re.compile(
        '''
        # A name is made up of letters, and may include "."
        # for title abbreviations and middle initials.
        ((?P<name>
                ([\w.,]+\s+)*[\w.,]+)
                \s*
                # email addresses are wrapped in angle brackets: < >
                # but only if a name is found, so keep the start bracket in this group
                <
        )? # the entire name is optional

        # The address itself: username@domain.tld
        (?P<email>
                [\w\d.+-]+      # username
                @
                ([\w\d.]+\.)+   # domain name prefix
                (com|edu|org)   # limit the allowed TLDs
        )
        >?      # optional closing bracket
        ''',
        re.UNICODE | re.VERBOSE )

candidates_short = [
        u'first.last@example.com',
        u'first.last+category@gmail.com',
        u'valid-address@mail.example.com',
        u'not-valid@example.foo',
        ]
candidates_long = [
        u'first.last@example.com',
        u'first.last+category@gmail.com',
        u'valid-address@mail.example.com',
        u'not-valid@example.foo',
        u'First Last <first.last@example.com>',
        u'No Brackets first.last@example.com',
        u'First Last',
        u'First Middle Last <first.last@example.com>',
        u'First M. Last <first.last@example.com>',
        u'<first.last@example.com',
        ]

def email_validation(address, candidates):
        for candidate in candidates:
                match = address.search(candidate)
                print
                print 'Candidate: %s' % candidate
                print ' Results : %s' % ('Matches' if match else 'No match')
                if match:
                        print ' Name :',  'Unknown' if not match.groupdict() else match.groupdict()['name']
                        print ' Email:', 'Unknown' if not match.groupdict() else match.groupdict()['email']
        print

email_validation(terse_address, candidates_short)
email_validation(verbose_address, candidates_short)
email_validation(expanded_address, candidates_long)

 # Instead of adding flags when compiling an expression, flags can be embedded into the expression string itself
 # by prepending the string with one or more of the following tags in the format of (?i) or (?imu)
 
 # Flag         Abbreviation
 # IGNORECASE   i
 # MULTILINE    m
 # DOTALL       s
 # UNICODE      u
 # VERBOSE      x

text = "This is some text -- with punctuation."
pattern = r'(?i)\bT\w+'
regex = re.compile(pattern)
print 'Text    :', text
print 'Pattern :', pattern
print 'Matches :', regex.findall(text)

 # (?=pattern) for lookahead patterns, and (?!pattern) for negative lookahead patterns

lookahead_address = re.compile(
        '''
        # A name is made up of letters, and may include "."
        # for title abbreviations and middle initials.

        ((?P<name>
                ([\w.,]+\s+)*[\w.,]+
                )
                \s+
        ) # the name is not optional
        
        # Email addresses are wrapped in angle brackets, but only if they are bot present or neither is.
        (?=
                (<.*>$) | ([^<].*[^>]$)
              # wrapped |  not wrapped  in angle brackets
        ) # LOOKAHEAD
        <? # optional opening angle bracket
        # The address itself: username@domain.tld
        (?P<email>
                (?!noreply@.*$) # Ignore noreply addresses # NEGATIVE LOOKAHEAD
                [\w\d.+-]+      # username
                @
                ([\w\d.]+\.)+   # domain name prefix
                (com|edu|org)   # limit the allowed TLDs
        )
        >?      # optional closing bracket
        ''',
        re.UNICODE | re.VERBOSE)

candidates_lookahead = [
        u'First Last <first.last@example.com>',
        u'No Brackets first.last@example.com',
        u'No Reply noreply@example.com',
        u'Open Bracket <first.last@example.com',
        u'Close Bracket first.last@example.com>',
        ]

email_validation(lookahead_address, candidates_lookahead)

 # You can also do positive look-behinds with (?<=pattern)

twitter = re.compile(
         '''
        # a Twitter handle: @username
        (?<=@)
        ([\w\d_]+)      # username
        ''',
         re.UNICODE | re.VERBOSE)

text = 'This text contains two Twitter handles.  One for @ThePSF, and one for the authore, @doughellmann.'

print text
for match in twitter.findall(text):
        print 'Handle:', match
print


## Self Referencing Expressions
 # They can be done with numbers, where \1 refers to the first group in the expression
 # and then can be referenced from a Match object (named match) with match.group(1)


self_number_address = re.compile(
        r'''
        # The regular name
        (\w+)           # first name
        \s+
        (([\w.]+)\s+)?  # optional middle name or initial
        (\w+)           # last name

        \s+

        <
        # the address : first_name.last_name@domain.tld
        (?P<email>
                \1              # first name
                \.
                \4              # last name
                @
                ([\w\d.]+\.)+   # domain name prefix
                (com|org|edu)   # limit matching TLDs
        )

        >
        ''',
        re.UNICODE | re.VERBOSE | re.IGNORECASE )

candidates_self_reference = [
        u'First Last <first.last@example.com>',
        u'Different Name <first.last@example.com>',
        u'First Middle Last <first.last@example.com>',
        u'First M. Last <first.last@example.com>',
        u'no.brackets@example.org',
        ]

for candidate in candidates_self_reference:
        print 'Candidate:', candidate
        match = self_number_address.search(candidate)
        if match:
                print ' Match name :', match.group(1), match.group(4)
                print ' Match email:', match.group(5)
        else:
                print ' No match!'
        print
print

 # However, the referencing can also be done with names, which is a lot nicer looking, and is easier to manage

self_named_address = re.compile(
        r'''
        # The regular name
        (?P<first_name>\w+)           # first name
        \s+
        (([\w.]+)\s+)?  # optional middle name or initial
        (?P<last_name>\w+)           # last name

        \s+

        <
        # the address : first_name.last_name@domain.tld
        (?P<email>
                (?P=first_name)        # first name
                \.
                (?P=last_name)         # last name
                @
                ([\w\d.]+\.)+           # domain name prefix
                (com|org|edu)           # limit matching TLDs
        )

        >
        ''',
        re.UNICODE | re.VERBOSE | re.IGNORECASE )

for candidate in candidates_self_reference:
        print 'Candidate:', candidate
        match = self_named_address.search(candidate)
        if match:
                print ' Match name :', match.groupdict()['first_name'], match.groupdict()['last_name']
                print ' Match email:', match.groupdict()['email']
        else:
                print ' No match!'
        print
print

 # it's even possible to change the pattern based on whether a previous group matched or not
 
self_checked_address = re.compile(
        r'''
        ^
        # A name is made up of letters, spaces, and may include '.' for titles, abbreviations, and initials
        (?P<name>
                ([\w.*]+\s*)+
        )?

        # email addresses are wrapped in brackets, but only if a name is found
        (?(name)
                # remainder wrapped in angle brackets because there is a name
                (?P<brackets>(?=(<.*>$)))
                |
                # remainder does not include angle brackets without name
                (?=([^<].*[^>]$))
        )

        # only look for a bracket if the lookahead assertion found them both
        (?(brackets)<|\s*)
        
        # the address : first_name.last_name@domain.tld
        (?P<email>
                [\w\d.+-]+              # username
                @
                ([\w\d.]+\.)+           # domain name prefix
                (com|org|edu)           # limit matching TLDs
        )

        # only look for a bracket if the lookahead assertion found them both
        (?(brackets)>|\s*)
        
        $
        ''',
        re.UNICODE | re.VERBOSE )

candidates_checked = [
        u"First Last <first.last@example.com>",
        u"No Brackets first.last@example.com",
        u"Open Bracket <first.last@example.com",
        u"Close Bracket first.last@example.com>",
        u"no.bracket@example.com",
        ]

for candidate in candidates_checked:
        print 'Candidate:', candidate
        match = self_checked_address.search(candidate)
        if match:
                print ' Match name :', match.groupdict()['name']
                print ' Match email:', match.groupdict()['email']
        else:
                print ' No match!'
        
        print
print


## Modifying Strings with Patterns
 # Use sub(sub_text, text) to replace all occurences of a pattern with another string
 # The simplest way to do it is by using numbered groups

bold = re.compile(r'\*{2}(.*?)\*{2}')
text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.sub(r'<strong>\1</strong>', text)
print

 # but it's basically the same to use named groups, as \g<group_name>

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}', re.UNICODE)
text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.sub(r'<strong>\g<bold_text></strong>', text)
print

 # you can also add a count value, which is the maximum number of substitutions that will be performed

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}', re.UNICODE)
text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.sub(r'<strong>\g<bold_text></strong>', text, count=1 )
print

 # subn() works almost the same as sub(), but it also returns the number of substitutions made

bold = re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}', re.UNICODE)
text = 'Make this **bold**. This **too**.'

print 'Text:', text
print 'Bold:', bold.subn(r'<strong>\g<bold_text></strong>', text )
print

 # Splitting strings with str.split() only works with literal values as separators
 # but the same function can be recreated if needed in situatuons where a regular expression is better
 # findall can work but it has some limitations, so there's also re.split()

text = '''Paragraph one\non two lines.\n\nParagraph two.\n\n\nParagraph three.'''

print "Missing the last paragraph, tsk tsk tsk:"
for num, para in enumerate(re.findall(r'(.+?)\n{2,}', text, flags=re.DOTALL)):
         print num, repr(para)
         print
print 'with findall:'
for num, para in enumerate(re.findall(r'(.+?)(\n{2,}|$)', text, flags=re.DOTALL)):
         print num, repr(para)
         print
print 'with split:'
for num, para in enumerate(re.split(r'\n{2,}', text)):
         print num, repr(para)
         print
print 'with split and grouping of the pattern:'
for num, para in enumerate(re.split(r'(\n{2,})', text)):
         print num, repr(para)
         print
