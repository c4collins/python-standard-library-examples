## 7.1 Pickle
# note that pickle is insecure, and should only be used when you can trust the source

## 7.1.1 Importing
# like StringIO, pickle has an identical but faster C counterpart called cPickle
try:
    import cPickle as pickle
    import cStringIO as StringIO
except:
    print "The slower, non-C versions of pickle and String IO are being used."
    import pickle, StringIO
import sys

## 7.1.2 Encoding and Decoding Data in Storage
data = [ { 'a' : 'A', 'b' : 2, 'c' : 3.0 } ]
print 'DATA    :', data

data_string = pickle.dumps(data)
print 'PICKLE  : %r' % data_string
unpickled = pickle.loads(data_string)
print 'UNPICKLE: %r' % unpickled
print 'SAME    :', unpickled is data
print 'EQUAL   :', unpickled == data
print

## 7.1.3 Working with Streams
# pickle provides convenience functions for working with file-like streams

class SimpleObject(object):
    def __init__(self, name):
        self.name = name
        l = list(name)
        l.reverse()
        self.name_backwards = ''.join(l)
        return

data = []
data.append(SimpleObject('pickle'))
data.append(SimpleObject('cPickle'))
data.append(SimpleObject('last'))

# Simulate a file with StringIO
out_s = StringIO.StringIO()

# Write to the stream
for o in data:
    print 'WRITING : %s (%s)' % (o.name, o.name_backwards)
    pickle.dump(o, out_s)
    out_s.flush()
    
# set up a readable stream
in_s = StringIO.StringIO(out_s.getvalue())

# Read the data
while True:
    try:
        o = pickle.load(in_s)
    except EOFError:
        break
    else:
        print 'READ    : %s (%s)' % (o.name, o.name_backwards)
print
       
## 7.1.4 Problems Reconstructing Objects
# Since only the data is saved in a pickle
# the class definition must already exist when unpickling
filename = sys.argv[1]
with open('data/7.1-'+filename, 'wb') as out_s:
    # Write to the stream
    for o in data:
        print 'WRITING : %s (%s)' % (o.name, o.name_backwards)
        pickle.dump(o, out_s)

# This only works because the SimpleObject class is defined in this file.  If it wasn't, it would have to be imported first        
with open('data/7.1-'+filename, 'rb') as in_s:
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print 'READ    : %s (%s)' % (o.name, o.name_backwards)
print

## 7.1.5 Unpicklable Objects
# sockets, file handles, db connections, etc. cannot be saved in a meaningful way
# Objects with unpickleable attributes can define __getstate__ and __setstate__

## 7.1.6 Circular References
# The pickle protocol automagically handles circular references

class Node(object):
    """A simple diagraph"""
    def __init__(self, name):
        self.name = name
        self.connections = []
        
    def add_edge(self, node):
        """create an edge between this node and the other."""
        self.connections.append(node)
    
    def __iter__(self):
        return iter(self.connections)

def preorder_traversal(root, seen=None, parent=None):
    """Generator function to yield the edges in a graph."""
    if seen is None:
        seen = set()
    
    yield (parent, root)
    
    if root in seen:
        return
    
    seen.add(root)
    
    for node in root:
        for parent, subnode in preorder_traversal(node, seen, root):
            yield (parent, subnode)
    # to fully understand how this works, I had to read: http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained
    # the yield statement returns an iterator, and this one happens to be recursive too
    
def show_edges(root):
    """Print all the edges in the graph."""
    for parent, child in preorder_traversal(root):
        if not parent:
            continue
        print '%5s -> %2s (%s)' % ( parent.name, child.name, id(child) )
        
# Set up the nodes
root = Node("root")
a = Node('a')
b = Node('b')
c = Node('c')

# Add edges between them
root.add_edge(a)
root.add_edge(b)
a.add_edge(b)
b.add_edge(a)
b.add_edge(c)
a.add_edge(a)

print 'ORIGINAL GRAPH:'
show_edges(root)

# Pickle and unpickle the graph to create a new set of nodes
dumped = pickle.dumps(root)
reloaded = pickle.loads(dumped)

print 'RELOADED GRAPH:'
show_edges(reloaded)

    