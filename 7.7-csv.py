## 7.7 csv - Comma-Separated Value Files
# or Character-Separated Value Files, whatever
import csv, sys, random, textwrap
from contextlib import closing
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
## 7.7.1 Reading
# use reader to create an object for reading data from a CSV file.
# The reader can be used as an iterator to process the rows of the file in order
demo_data_file = "data/7.7-csv_data.csv"
with closing( open( demo_data_file, 'r' ) ) as f:
    reader = csv.reader(f)
    for row in reader:
        print row
        
# The parser handles line breaks embedded within strings in a row, so sometimes a row can be more than one line in the file
# For example:
    # "Connor","Col
    # lins"
# This appears in text as two lines, but will be parsed as:
    # "Connor", "Col\nlins"

## 7.7.2 Writing
# Writing to CSV files is very similar to reading them
# Use writer() to create and object for writing, and then iterate over rows using writerow() to print them
with closing( open( demo_data_file, 'w' ) ) as f:
    writer = csv.writer(f)
    
    writer.writerow( [ "Title 1", "Title 2", "Title 3", ] )
    for i in xrange(3):
        writer.writerow( [ i+1, chr(ord('a') + i), '08/%02d/13' % (i + 1) ] )
print

# The default quoting behaviour is different for the writer, so the second and third columns in the previous example are not quoted
# to add quoting, set the quoting arguments to one of the other quoting modes
for quoting in random.sample( [ csv.QUOTE_ALL, csv.QUOTE_MINIMAL, csv.QUOTE_NONNUMERIC, csv.QUOTE_NONE ] , 4 ):
    # random.sample() is used to change the final output quoting behaviour so different styles can be observed in the file by running this program multiple times and inspecting the resulting csv.
    with closing( open( demo_data_file, 'w' ) ) as wf:
        writer = csv.writer( wf, quoting=quoting )
        writer.writerow( [ 'Title 1', 'Title 2', 'Title 3', ] )
        for i in xrange(0, 3*(quoting+1), (quoting+1)):
            writer.writerow( ( i+1, chr(ord('a') + i), '08/%02d/13' % (i + 1) ) )
            
    # Read back the data as written before the next quoting style replaces it    
    with closing( open( demo_data_file, 'r' ) ) as rf:
        reader = csv.reader(rf)
        for row in reader:
            print row
        print
    # This doesn't appear to do anything when displayed this way but:
        # QUOTE_ALL should quote everything
        # QUOTE_MINIMAL should quote fields with special characters - Default.
        # QUOTE_NONNUMERIC sould quote anything that isn't an integer or a float.
        # QUOTE_NONE will not quote anything on output
    # the file does have the specified quoting patterns though

## 7.7.3 Dialects
# Dialects are the grouped parameters defining the formatting standard for CSV files.
# Since there is no *standard* standard, dialects allow for constrained flexibility

print csv.list_dialects()
print

# Registering a new dialect is pretty easy
csv.register_dialect('pipes', delimiter='|')

with closing( open( 'data/7.7-csv_data-pipes.csv', 'r' )) as f:
    reader = csv.reader( f, dialect='pipes' )
    for row in reader:
        print row
print
       
# The available dialect parameters are :
    # Attribute         Default         Meaning
    # delimiter         ,               Field separator (one character)
    # doublequote       True            Flag controlling if quotechar instances are doubled
    # escapechar        None            Character used to indicate an escape sequence
    # lineterminator    \r\n            String used by the writer to terminate a line
    # quotechar         "               String used to surround fields containing special characters (one character)
    # quoting           QUOTE_MINIMAL   Controls quoting behaviour (as described above)
    # skipinitialspace  False           Ignores whitespace after the field delimiter
    
csv.register_dialect( 'escaped',
    escapechar = '\\',
    doublequote= False,
    quoting    = csv.QUOTE_NONE,
)

csv.register_dialect( 'singlequote',
    quotechar = "'",
    quoting   = csv.QUOTE_ALL,
)
quoting_modes = dict( ( getattr(csv, n) , n ) for n in dir(csv) if n.startswith('QUOTE_') )

for name in sorted( csv.list_dialects() ):
    print "Dialect: '%s'\n" % name
    dialect = csv.get_dialect(name)
    
    print "  delimiter   = %-6r   skipinitialspace = %r" % ( dialect.delimiter, dialect.skipinitialspace )
    print "  doublequote = %-6r   quoting = %r" % ( dialect.doublequote, dialect.quoting )
    print "  quotechar   = %-6r   lineterminator = %r" % ( dialect.quotechar, dialect.lineterminator )
    print "  escapechar  = %-6r" % ( dialect.escapechar )
    
    writer = csv.writer( sys.stdout, dialect=dialect )
    writer.writerow( ('col1', 1, '01/09/2013','Special chars: "\' %s to parse' % dialect.delimiter) )
    print
    
# Obviously, if you know the format in advance that is the best
# but the Sniffer class can be used to try to guess if necessary
# the sniff() method dakes a sample of the input data and optionally an argument defining possible delimiting characters

# generate sample data for all known dialects
samples = []
for name in sorted( csv.list_dialects() ):
    buffer = StringIO()
    dialect = csv.get_dialect(name)
    writer = csv.writer( buffer, dialect=dialect )
    writer.writerow( ('col1', 1, '01/09/2013','Special chars: "\' %s to parse' % dialect.delimiter) )
    samples.append( (name, dialect, buffer.getvalue() ) )
    
# guess the dialect for a given sample, then use the results to parse the data
sniffer = csv.Sniffer()
for name, expected, sample in samples:
    print "Dialect: '%s'\n" % name
    dialect = sniffer.sniff(sample, delimiters=',\t|')
    reader = csv.reader( StringIO(sample), dialect=dialect )
    print reader.next()
    print
    
## 7.7.4 Using Field Names
# The csv module also contains classes for working with rows of dictionaries
# DictReader and DictWriter translate rows to dictionaries instead of lists.
# Keys for the dictionary can be passed in or inferred from the first row in the input (headers)

with closing( open( 'data/7.7-csv_data-dicts.csv', 'r' ) ) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print row
        
# DictWriter must be given a list of field names so it can order the columns properly
with closing( open( 'data/7.7-csv_data-dicts.csv', 'w' ) ) as f:
    fieldnames = ('Title 1', 'Title 2', 'Title 3')
    headers = dict( (n,n) for n in fieldnames )
    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(headers)
    
    for i in xrange(3):
        writer.writerow( { 
            'Title 1': i+1,
            'Title 2': chr( ord('a') + i),
            'Title 3': '08/%02d/13' % (i + 1),
        } )
print
    