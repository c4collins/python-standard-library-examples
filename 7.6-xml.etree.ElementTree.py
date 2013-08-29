## 7.6 xml.etree.ElementTree - XML Manipulation API
# XML documents are represented in memory b ElementTree and Element objects, connected in a tree structure which represents the hierarchy of the XML file.
from xml.etree import ElementTree
from xml.etree.ElementTree import ( Element, SubElement, Comment, )
from xml.dom import minidom
from contextlib import closing
import csv, sys, datetime

## 7.6.1 Parsing an XML Document

# parsing an entire document tree with parse() returns an ElementTree instance
# this can be useful, but also more memory-intensive than an event-based approach
with closing( open('data/7.6-xml.etree.ElementTree_podcasts.opml', 'r') ) as f:
    tree = ElementTree.parse(f)
print "ElementTree object:", tree
print

## 7.6.2 Traversing the Parsed Tree
# to visit all children in order, use iter() to create a generator
print "All nodes:",
for node in tree.iter():
    node.tag, 
print
    
# indicate a specific tag and only receive those results
for node in tree.iter('outline'):
    name = node.attrib.get('text')
    url = node.attrib.get('xmlUrl')
    if name and url:
        print ' - %s' % name
        print '    %s' % url
    else:
        print '\n', name
print

## 7.6.3 Finding Nodes in a Document
# use findall() to look for nodes with descriptive search characteristics
print "using './/outline':"
for node in tree.findall('.//outline'):
    name = node.attrib.get('text')
    url = node.attrib.get('xmlUrl')
    if url:
        print '%-41s : %s' % (name+" xmlUrl", url)
    else:
        print "Outline node '%s' does not contain an xmlUrl attribute." % name
print

# this can be sepcified even further buy only looking into the second level of outlines
print "using './/outline/outline':"
for node in tree.findall('.//outline/outline'):
    url = node.attrib.get('xmlUrl')
    # no if is needed because all elements should have the xmlUrl
    # None would be the result of a date-entry error, not a node to not display
    print '%-41s : %s' % ( node.attrib.get('text') + " xmlUrl", url)
print

## 7.6.4 Parsed Node Attributes
# The items returned bu iter() and findall() are Element objects, each representing a single node
# Each Element has attributes for accessing data pulled from the XML
with closing( open( 'data/7.6-xml.etree.ElementTree_data.xml', 'r') ) as f:
    tree = ElementTree.parse(f)
  
# shows how to access attribute values
node=tree.find('./with_attributes')
print node.tag
for name, value in sorted(node.attrib.items()):
    print '  %-4s = "%s"' % (name, value)
print

# shows how to access contents and tail text sections
for path in ['./child', './child_with_tail']:
    node=tree.find(path)
    print node.tag
    print '  child node text:', node.text
    print '  child node tail:', node.tail

# shows that conversion of special characters is done automatically
node = tree.find('entity_expansion')
print node.tag
print '  in attribute:', node.attrib['attribute']
print '  in text     :', node.text.strip()
print

## 7.6.5 Watching Events While Parsing
# The other API for processing XML-based documents is event based
# the parser generates a start event and an end event from opening and closing tags
# Data can be extracted form the document by iterating over the event stream
# The event types are:
    # start - A new tag has been encountered, the closing angle bracket has been processed, but not the contents
    # end - The closing angle bracket has been processed, all children have been processed
    # start-ns - Start a namespace declaration
    # end-ns - end a namespace declaration
# iterparse() returns an iterable that produced tuples with the name of the event and the triggering node.

depth = 0
prefix_width = 8
prefix_dots = '.' * prefix_width
line_template = ''.join([
    '{prefix:<0.{prefix_len}}',
    '{event:8}',
    '{suffix:<{suffix_len}}',
    '{node.tag:<12} ',
    '{node_id}',
])
EVENT_NAMES = ['start', 'end', 'start-ns', 'end-ns']

for (event, node) in ElementTree.iterparse('data/7.6-xml.etree.ElementTree_podcasts.opml', EVENT_NAMES):
    if event == 'end':
        depth -= 1
    
    prefix_len = depth*2
    
    print line_template.format(
        prefix    = prefix_dots,
        prefix_len= prefix_len,
        suffix    = '',
        suffix_len= (prefix_width - prefix_len),
        node      = node,
        node_id   = id(node),
        event     = event,
    )
    
    if event == 'start':
        depth += 1
print
       
# the event based model is more natural for some operations, such as converting XML to another format
writer = csv.writer( sys.stdout, quoting=csv.QUOTE_NONNUMERIC )
# sys.stdout instead of a file so you can taste the difference quality makes.

group_name = ''
print "Converting to CSV:"
for (event, node) in ElementTree.iterparse('data/7.6-xml.etree.ElementTree_podcasts.opml', events=['start']):
    if node.tag != 'outline':
        # ignore anything not part of the outline
        continue
    if not node.attrib.get('xmlUrl'):
        # Remember the current group
        group_name = node.attrib['text']
    else:
        # Output a podcast entry
        writer.writerow( ( 
            group_name, 
            node.attrib['text'], 
            node.attrib['xmlUrl'], 
            node.attrib.get('htmlUrl', ''), 
        ) )
print

## 7.6.6 Creating a Custom Tree Builder
# The ElementTree parser uses XMLTreeBuilder to process the XML and call methods on a target class
# The usual output is an ElementTree instance created by the default TreeBuilder class
# Replacing TreeBuilder with another class allows it to receive events before the Element nodes are created,
# potentially bypassing that source of overhead entirely.

class PodcastListToCSV(object):
    def __init__(self, outputFile):
        self.writer = csv.writer( outputFile, quoting=csv.QUOTE_NONNUMERIC )
        self.group_name = ''
        return
    def start(self, tag, attrib):
        if tag != 'outline':
            # ignore anything not part of the outline
            return
        if not attrib.get('xmlUrl'):
            # Remember the current group
            self.group_name = attrib['text']
        else:
            # Output a podcast entry
            self.writer.writerow( ( 
                self.group_name, 
                attrib['text'], 
                attrib['xmlUrl'], 
                attrib.get('htmlUrl', ''), 
            ) )
    def end(self, tag):
        # Ignore closing tags
        pass
    def data(self, data):
        # Ignore data inside nodes
        pass
    def close(self):
        # Nothing special to do here
        return

print "Using a custom tree-building class:"
target = PodcastListToCSV( sys.stdout )
with closing( ElementTree.XMLTreeBuilder(target=target) ) as parser:
    with closing( open('data/7.6-xml.etree.ElementTree_podcasts.opml', 'r') ) as f:
        for line in f:
            parser.feed(line)                
print

## 7.6.7 Parsing Strings
# To work ith smaller bits of XML text, use XML() with the string containing the XML as the only argument
xml_string_to_parse = """
<root>
    <group>
        <child id="a">This is child "a".</child>
        <child id="b">This is child "b".</child>
    </group>
    <group>
        <child id="c">This is child "c".</child>
    </group>
</root>
"""

print "Using XML():"
parsed = ElementTree.XML( xml_string_to_parse )
print "parsed=", parsed
def show_node(node):
    print node.tag
    if node.text is not None and node.text.strip():
        print "  text: '%s'" % node.text
    if node.tail is not None and node.tail.strip():
        print "  tail: '%s'" % node.tail
    for (name, value)  in sorted( node.attrib.items() ):
        print "  %-4s = '%s'" % ( name, value )
    for child in node:
        show_node(child)
    return
      
# unlike with parse() the returned value is an Element instead of an ElementTree
# Elements can be iterated upon directly instead of using iterparse()
for elem in parsed:
    show_node(elem)
print
    
# for structures XML that uses the id attribute it identify unique nodes there is XMLID()
print "Using XMLID():"
tree, id_map = ElementTree.XMLID( xml_string_to_parse )
for (key, value) in sorted( id_map.items() ):
    print "  %-4s = '%s'" % ( key, value )
print

## 7.6.8 Building Documents wih Element Nodes
# ElementTree is also capable of creating well-formed XML documents from Element objects
# The Element class can produce a serialized form of its contents which can then be stored
# There are three helper functions useful when creating a hierarchy of Element nodes
    # Element() creates a standard node
    # SubElement() attached a new node to a parent
    # Comment() creates a node that serializes using XML's comment syntax

top = Element('top')

comment = Comment("Generated for pystl")
top.append( comment )

child = SubElement( top, 'child' )
child.text = "This child contains text."

child_with_tail = SubElement( top, 'child_with_tail' )
child_with_tail.text = "This child has regular text."
child_with_tail.tail = "And 'tail' text."

child_with_entity_ref = SubElement( top, 'child_with_entity_ref' )
child_with_entity_ref.text = "This & That"

print "An XML string has been built:"
print ElementTree.tostring( top )
print

## 7.6.9 Pretty-Printing XML
# ElementTree doesn't add any whitespace, which is useful, but quite ugly
# xml.dom.minidom's toprettyxml() method makes it look a lot better for printing

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ')
    
print "Prettified:"
print prettify( top )
print

## 7.6.10 Setting Element Properties
generated_on = str( datetime.datetime.now() )

# Configure one attribute with set()
root = Element('opml')
root.set('version', '1.0')

root.append(
    Comment( "Generated by 7.6-xml.etree.ElementTree.py for Python Standard Library by Example" )
)

head = SubElement(root, 'head')

title = SubElement(head, 'title')
title.text = "My Podcasts"

dc = SubElement(head, 'dateCreated')
dc.text = generated_on
dm = SubElement(head, 'dateModified')
dm.text = generated_on

body = SubElement(root, 'body')

with closing( open('data/7.6-xml.etree.ElementTree_podcasts.csv', 'r') ) as f:
    current_group = None
    reader = csv.reader(f)
    for row in reader:
        print row
        group_name, podcast_name, xml_url, html_url = row
        if current_group is None or group_name != current_group.text:
            # Start a new group
            current_group = SubElement( body, 'outline', {'text':group_name} )
         
        # Add this podcast to the group, setting all attributes at once
        podcast = SubElement( current_group, 'outline', {
            'text'   : podcast_name,
            'xmlUrl' : xml_url,
            'htmlUrl': html_url,
        } )
        
print prettify(root)
print

## 7.6.11 Building Trees from Lists of Nodes
# Multiple children can be added to an Element instance together with extend()
# The argument to extend() is any iterable, including a list or another Element instance
top = Element( 'top' )

children = [
    Element( 'child', num=str(i) )
    for i in xrange(3)
]
top.extend(children)

print prettify(top)
print

# When another Element(0 instance is given, the children of that node are added to the new parent
top = Element( 'top' )

parent = SubElement( top, 'parent' )

children = ElementTree.XML("""
    <root><child num="0" /><child num="1" /><child num="2" /></root>
""")
parent.extend( children )

print prettify( top )

# In this case the not with the tag root created by parsing the XML string has 3 children, which are added to the parent node
# The root node is not part of the output tree

# If the values passed to extend() exist somewhere in the tree already, they will still be there, and will be repeated in the output.

top = Element( 'top' )

parent_a = SubElement( top, 'parent', id='A' )
parent_b = SubElement( top, 'parent', id='B' )

# Create children
children = ElementTree.XML("""
    <root><child num="0" /><child num="1" /><child num="2" /></root>
""")

# Set the id to the Python object id of the node to make duplicates easier to spot
for c in children:
    c.set( 'id', str( id(c) ) )

# Add to first parent
parent_a.extend( children )
print "A:"
print prettify( top )
print

# Add to second parent
parent_b.extend( children )
print "B:"
print prettify( top )
print

## 7.6.12 Serializing XML to a Stream
# tostring() is implemented by writing to an in-memory file-like object and then returning a string representing the entire element tree.
# When workig with large amounts of data, it takes less data and makes more efficient use of I/O to use write() instead

top = Element( 'top' )

comment = Comment( "Generated for PySTL" )
top.append( comment )

child = SubElement( top, 'child' )
child.text = "This child contains text."

child_with_tail = SubElement( top, 'child_with_tail' )
child_with_tail.text = "This child has regular text."
child_with_tail.tail = "And 'tail' text."

child_with_entity_ref = SubElement( top, 'child_with_entity_ref' )
child_with_entity_ref.text = "This & That"

empty_child = SubElement( top, 'empty_child' )

# This example writes to sys.stdout, but could be written to file as well
ElementTree.ElementTree( top ).write( sys.stdout )
print "\n"

# write() takes a mothod argument for dealing with empty nodes
for method in [ 'xml', 'html', 'text' ]:
    print method
    ElementTree.ElementTree(top).write(sys.stdout, method=method)
    print "\n"
# xml prints empty nodes as a single empty child tag
# html prints empty nodes as the tag pair required by my HTML
# text skips empty nodes entirely
