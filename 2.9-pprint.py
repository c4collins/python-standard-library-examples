## pprint!
 # pretty print prints things prettily

data = [ ( 1,
           { 'a':'A',
             'b':'B',
             'c':'C',
             'd':'D'
           }),
         ( 2,
           { 'e':'E',
             'f':'F',
             'g':'G',
             'h':'H',
             'i':'I',
             'j':'J',
             'k':'K',
             'l':'L'
             }),
         ]

import logging
from pprint import pprint, pformat

print 'Print:'
print data
print
print 'PPrint:'
pprint(data)

 # use pformat() to build a formatted string

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    )
logging.debug('Logging pformatted data')
formatted = pformat(data)
for line in formatted.splitlines():
    logging.debug(line.rstrip())

 # the PrttyPrinter class can be used in customd classes (not just Strings)
 # if they define a __repr__() method

class node(object):
    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]

    def __repr__(self):
        return ( 'node('+ repr(self.name) + ', ' + repr(self.contents) + ')' )

trees = [
         node('node-1', []),
         node('node-2', [ node('node-2.1'), node('node-2.2.') ] ),
         node('node-3', [ node('node-3.1') ]),
        ]

pprint(trees)

 # pprint will indicate recursion
data.append(data)
print '\ndata.append(data)'
pprint(data)
data = data[0:2]
print
 # pprint can take two aguments, depth and width
 # depth tells how deep to print (duh)

pprint( data, depth = 2)

 # and width tells... width!
for pwidth in [ 8, 80 ]:
    print '\nwidth:', pwidth
    pprint( data, width = pwidth)
