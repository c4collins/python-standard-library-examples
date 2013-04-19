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
