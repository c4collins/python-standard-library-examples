import re

pattern = 'this'
text = 'Does this text match the pattern?'


# Simple text match
match = re.search(pattern, text)

s = match.start()
e = match.end()

print 'Found "%s"\nin "%s"\nfrom %d to %d ("%s")' % (match.re.pattern, match.string, s, e, text[s:e])


# Compiling RegexObjects

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

# multiple matches

text = 'abbaaabbbbaaaaa'

