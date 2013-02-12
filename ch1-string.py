import string
# maketrans() and capwords are not being moved to the string object from the string module
# Also, string.Template

s = "The quick brown fox jumped over the lazy dog."
leet = string.maketrans('abegiloprstz', '463611092572')

print "Base String     :", s
print "Capwords String :", string.capwords(s)
print "Translate String:", s.translate(leet)


values = { 'var':'foo' }


# Template vs. string interpolation

t = string.Template("""
Variable        : $var
Escape          : $$
Variable in text: ${var}iable
""")

print '\nTEMPLATE:', t.substitute(values)

s = """
Variable        : %(var)s
Escape          : %%
Variable in text: %(var)siable
"""

print 'INTERPOLATION:', s % values


# substitute vs. save substitute with templates
t = string.Template("$var is here, but $missing is not provided")

try:
	print 'substitute()     :', t.substitute(values)
except KeyError, err:
	print 'ERROR:', str(err)
finally:
	print 'safe_substitute():', t.safe_substitute(values)


# Advanced templates, using delimter and idpattern class attributes
template_text = '''
Delimiter  : %%
Replaced   : %with_underscore
Ignored    : %notunderscored
'''

d = { 'with_underscore': 'replaced', 
	  'notunderscored': 'not replaced'
	  }

class MyTemplate(string.Template):
	delimiter = '%'
	idpattern = '[a-z]+_[a-z]+'

t = MyTemplate(template_text)
print '\nModified ID pattern:'
print t.safe_substitute(d)

print t.pattern.pattern

import re # regular expressions

class NewTemplate(string.Template):
	delimiter = '{{'
	pattern = r'''
	\{\{(?:
	(?P<escaped>\{\{)|
	(?P<named>[_a-z][_a-z0-9]*)\}\}|
	(?P<braced>[_a-z][_a-z0-9]*)\}\}|
	(?P<invalid>)
	)
	'''

n = NewTemplate('''
	{{{{
	{{var}}
	''')

print 'MATCHES:', n.pattern.findall(n.template)
print 'SUBSTITUTED:', n.safe_substitute(var='replacement')


# Text-wrapping 
import textwrap
# (does this work in Django?)

sample_text = '''
The textwrap module can be used to format text for output in siuations where pretty-printing is desired.  It offers programmatic functionality similar to the paragraph wrapping or filling features found in most text editors.
'''
dedented_text = textwrap.dedent(sample_text)


print 'No dedent:\n'
print textwrap.fill(sample_text, width=48)
print '\nDedented:\n'
print dedented_text

dedented_text = dedented_text.strip()

for width in [45, 70]:
	print '%d Columns:\n' % width
	print textwrap.fill(dedented_text, width=width)
	print

print textwrap.fill(dedented_text, 
		initial_indent='',
		subsequent_indent = ' ' * 4,
		width=50
		)