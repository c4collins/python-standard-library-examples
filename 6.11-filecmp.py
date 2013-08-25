## 6.11 filecmp
# compare files AND directories
import filecmp, os, pprint

## 6.11.1 Example Data
# just set up some example data.
def mkfile(filename, body=None):
    with open(filename, 'w') as f:
        f.write(body or filename)
    return
    
def make_example_dir(top):
    if not os.path.exists(top):
        os.mkdir(top)
    curdir = os.path.abspath(os.curdir)
    os.chdir(top)
    
    os.mkdir('dir1')
    os.mkdir('dir2')
    
    mkfile('dir1/file_only_in_dir1')
    mkfile('dir2/file_only_in_dir2')
    
    os.mkdir('dir1/dir_only_in_dir1')
    os.mkdir('dir2/dir_only_in_dir2')
    
    os.mkdir('dir1/common_dir')
    os.mkdir('dir2/common_dir')
    
    mkfile('dir1/common_file', 'this file is the same')
    mkfile('dir2/common_file', 'this file is the same')
    
    mkfile('dir1/not_the_same')
    mkfile('dir2/not_the_same')
    
    mkfile('dir1/file_in_dir1', 'this is a file in dir1')
    os.mkdir('dir2/file_in_dir1')
    
    os.chdir(curdir)
    return
    
# this should only run the first time this program is executed in any location
if not os.path.exists('data/6.11-filecmp/dir1'):
    os.chdir( os.path.dirname(__file__) or os.getcwd() )
    make_example_dir('data/6.11-filecmp')
    make_example_dir('data/6.11-filecmp/dir1/common_dir')
    make_example_dir('data/6.11-filecmp/dir2/common_dir')
    
## 6.11.2 Comparing Files
# cmp() compares two files
# shallow=False searches the file contents as well as metadata
files = ['common_file', 'not_the_same', 'file_only_in_dir1', ]
for file in files:
    if file is not 'file_only_in_dir1':
        print '{:20}:'.format(file),
        print filecmp.cmp('data/6.11-filecmp/dir1/' + file, 'data/6.11-filecmp/dir2/' + file), 
        print filecmp.cmp('data/6.11-filecmp/dir1/' + file, 'data/6.11-filecmp/dir2/' + file, shallow=False)
    else:
        print '{:20}:'.format("Identical"),
        print filecmp.cmp('data/6.11-filecmp/dir1/' + file, 'data/6.11-filecmp/dir1/' + file), 
        print filecmp.cmp('data/6.11-filecmp/dir1/' + file, 'data/6.11-filecmp/dir1/' + file, shallow=False)
print

# cmpfiles() is used to compare a set of files in two directories
d1_contents = set( os.listdir('data/6.11-filecmp/dir1') )
d2_contents = set( os.listdir('data/6.11-filecmp/dir2') )

common = list( d1_contents & d2_contents)
common_files = [f 
                for f in common
                if os.path.isfile( os.path.join( 'data/6.11-filecmp/dir1', f ))
                ]
                
print 'Common files:', common_files
# compare the directories
match, mismatch, errors = filecmp.cmpfiles('data/6.11-filecmp/dir1',
                                           'data/6.11-filecmp/dir2',
                                           common_files)
print 'Match    :', match
print 'Mismatch :', mismatch
print 'Errors   :', errors
print

## 6.11.3 Comparing Directories
# dircmp() allows for recursive comparison of large directory trees
# dircomp().report() prints a bunch of info
filecmp.dircmp('data/6.11-filecmp/dir1', 'data/6.11-filecmp/dir2').report()
print
# dircomp().report_full_closure() includes all parallel subdirectories
filecmp.dircmp('data/6.11-filecmp/dir1', 'data/6.11-filecmp/dir2').report_full_closure()
print

## 6.11.4 Using Differences in a Program
# creating a dircmp instance does not incur overhead for unused data
# all of these attributes are only calculated when accessed
# left_list  is generated from the the first  argument
# right_list is generated from the the second argument
# common is items found in both left_list and right_list
dc =filecmp.dircmp('data/6.11-filecmp/dir1', 'data/6.11-filecmp/dir2')
print 'Left  :'
pprint.pprint(dc.left_list)
print 'Right :'
pprint.pprint(dc.right_list)
print 'Common :'
pprint.pprint(dc.common)
print

# inputs can be filtered by passing a list of names to ignore to the constructor
dc =filecmp.dircmp('data/6.11-filecmp/dir1', 'data/6.11-filecmp/dir2', ignore=['common_file'])
print 'Left  :'
pprint.pprint(dc.left_list)
print 'Right :'
pprint.pprint(dc.right_list)
print 'Common :'
pprint.pprint(dc.common)
print

# There are common_dirs, common_files, and common_funny,
dc =filecmp.dircmp('data/6.11-filecmp/dir1', 'data/6.11-filecmp/dir2')
print 'Common Dirs    :'
pprint.pprint(dc.common_dirs)
print 'Common Files   :'
pprint.pprint(dc.common_files)
print 'Common Funny   :'
pprint.pprint(dc.common_funny)
print
# and also same_files, diff_files, and funny_files
print 'Same Files     :'
pprint.pprint(dc.same_files)
print 'Different Files:'
pprint.pprint(dc.diff_files)
print 'Funny Files    :'
pprint.pprint(dc.funny_files)
print
# And also the subdirectories are saved in case they're needed
print 'Subdirectories :'
pprint.pprint(dc.subdirs)