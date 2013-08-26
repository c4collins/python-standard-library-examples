## 7.5 sqlite3 - Embedded Relational Database
import sqlite3, os, sys, csv
from contextlib import closing

# this is the database used for this file, and the schema for it below.

#Column      Type    Description
# name        text    project name
# description text    long project description
# deadline    date    due date for the entire project

#Column         Type        Description
# id             number      unique task identifier
# priority       integer     numerical property; lower is more important
# details        text        full task details
# status         text        task status( new, pending, done, or cancelled)
# deadline       date        due date for the task
# completed_on   date        when was the task completed
# project        text        name of the project for this task

# this can all be defined via DDL (data definition language) and written to a file
# it could also just be saved to a file in some other manner (like with a text editor),
# or it can be loaded from memory
        
schema = """-- Schema for to-do application examples

--projects are high-level activities made up of tasks
create table project (
    name        text    primary key,
    description text,
    deadline    date
);

-- Tasks are steps that can be taken to complete a project
create table task (
    id             integer  primary key     autoincrement   not null,
    priority       integer  default 1,
    details        text,
    status         text,
    deadline       date,
    completed_on   date,
    project        text     not null        references project(name)
);
"""
# this is the output format for the individual tasks when listed
# it comes up a lot in this file, so I thought it would be nice to have a single string to make changes on
task_fmt = '{:2d} ({:d}) {:50s} [{:8s}] ({:s})'

## 7.5.1 Creating a Database
# An SQLite db is stored as a single file on the file system
db_filename = 'data/7.5-sqlite3_to-do.db'
db_is_new = not os.path.exists(db_filename)

schema_filename = 'data/7.5-sqlite3_to-do_schema.sql'
schema_is_new = not os.path.exists(schema_filename)

with closing( sqlite3.connect(db_filename) ) as conn:
    if db_is_new:
        print "Database was created."   
    else:
        print "Database already exists."

    if schema_is_new:
        # The next step is creating a schema

        with closing( open(schema_filename, 'w+' ) ) as schema_file:
            schema_file.write(schema)
        print "  Schema was created."
    else: 
        print "  Schema already exists."
print

# apply the schema (from file, in this case)
# [though I'm overwriting the variable which already has the schema so this is not exactly useful]
with closing( sqlite3.connect(db_filename) ) as conn:
    if (db_is_new or schema_is_new) :
        print "Applying Schema"
        with closing( open(schema_filename, 'r') ) as f:
            schema = f.read()
        # however you obtain the schema data, run it with executescript() on the db
        conn.executescript(schema)
        print " Schema Applied"
        print

        # since this block is only called when one/two of the two things required before you can insert data
        # did not exist prior to this instance of code, which means this data needs to get shovelled in.
        data = """
        insert into project ( name, description, deadline )
        values ( 'pystl', 'Python Standard Library by Example', '2013-08-31' );

        insert into task ( details, status, deadline, project )
        values ( 'Chapter 6', 'done', '2013-08-25', 'pystl' );

        insert into task ( details, status, deadline, project )
        values ( 'Chapter 7', 'pending', '2013-08-26', 'pystl' );

        insert into task ( details, status, deadline, project )
        values ( 'Chapter 8', 'new', '2013-08-27', 'pystl' );        
        """ 
        with closing( sqlite3.connect(db_filename) ) as conn:
            print "Inserting Initial Data"
            conn.executescript(data)
    
## 7.5.2 Retrieving Data
# to retrieve values, create a cursor from a database connection.
# A cursor provides a consistent view of data and is the primary means or transacting with a relational db

with closing( sqlite3.connect(db_filename) ) as conn:
    # create cursor
    cursor = conn.cursor()
    # execute query through cursor
    cursor.execute("""
    select id, priority, details, status, deadline from task where project = 'pystl'
    """)
    # read data from cursor
    for row in cursor.fetchall():
        task_id, priority, details, status, deadline = row
        print task_fmt.format( task_id, priority, details, status, deadline )
    print
    
    # there`s also a fetchone() that just fetches the first result,
    cursor.execute("""
    select name, description, deadline from project
    """)
    
    project_name, description, deadline = cursor.fetchone()
    print "Project details for %s (%s) [%s]" % ( description, project_name, deadline )
    
    # and a fetchmany(x) that just fetches [up to] x results.
    cursor.execute("""
    select id, priority, details, status, deadline from task 
    where project = ?
    """, ( project_name, ) )
    print "Two results:"
    for row in cursor.fetchmany(2):
        task_id, priority, details, status, deadline = row
        print task_fmt.format( int(task_id), int(priority), details, status, deadline )
    print "Five more results:"    
    for row in cursor.fetchmany(5):
        task_id, priority, details, status, deadline = row
        print task_fmt.format( int(task_id), int(priority), details, status, deadline )
        
## 7.5.3 Query Metadata
# after execute() has been called, the cursor sets it's description attribute 
# to hold info about the data that will be returned by the fetch methods.
# the description = ( (column_name, type, display_size, internal_size, precision, scale, null_flag), ...)
# though, sqlite3 only returns the name, because it doesn't enforce size or type restraints
with closing( sqlite3.connect(db_filename) ) as conn:
    cursor = conn.cursor()
    
    cursor.execute("""
    select * from task where project = ?
    """, ( project_name, ) )
    
    print "\nTask table has these columns:"
    for colinfo in cursor.description:
        print colinfo
    print
        
## 7.5.4 Row Objects
# the default rows returned by the fetch methods are tuples
# this requires the caller to be responsible for the order and number of values in the query
# it is much easier to use a Row object and access values using their column names
# then the actual db structure can change all it wants without affecting the program

# Connection objects have a row_factory property that allows the calling code to control the type of object representing each row
# sqlite3 also includes a Row class intended to be used as a row_factory (wow)
with closing( sqlite3.connect(db_filename) ) as conn:
    # Change the row_factory to use sqlite3.Row
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    
    cursor.execute("""
    select name, description , deadline from project
    where name = ?
    """, ( project_name, ) )
    p_name, description, deadline = cursor.fetchone()
    print "Project details for %s (%s) [%s]" % ( description, project_name, deadline )
    
    cursor.execute("""
    select id, priority, details, status, deadline from task 
    where project = ?
    order by deadline
    """, ( p_name, ) )
    

    for row in cursor.fetchmany(5):
        # read data from cursor using the Row object
        print task_fmt.format(  row['id'], row['priority'], row['details'], row['status'], row['deadline'] )
    print
## 7.5.5 Using Variables with Queries
# the proper way to use dynamic values in queries is with host variables
# Positional Arguments are indicated must match in number to the arguments provided
# I read ahead and have been doing this for this whole file because I knew merging strings wasn't good
    # Positional arguments are indicated with ?s
    
# Named Parameters are useful in more complex queries and especially when values are used more than once
    # Names parameters are indicated like :param_name
with closing( sqlite3.connect(db_filename) ) as conn:
    # Change the row_factory to use sqlite3.Row
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    
    cursor.execute("""
    select name, description , deadline from project
    where name = ?
    """, ( project_name, ) )
    p_name, description, deadline = cursor.fetchone()
    print "Project details for %s (%s) [%s]" % ( description, project_name, deadline )
    
    cursor.execute("""
    select id, priority, details, status, deadline from task 
    where project = :project_name
    order by deadline
    """, {'project_name':p_name} )  # see, here is the named parameter in use

    for row in cursor.fetchmany(5):
        # read data from cursor using the Row object
        print task_fmt.format(  row['id'], row['priority'], row['details'], row['status'], row['deadline'] )   
    print

# check for special commands as arguments
arg_command = sys.argv[1] if len(sys.argv) >= 2 else None
if arg_command is None:
    pass
    
# query parameters can be used with select, insert, and update statements, as long as a literal value is legal in the context
elif arg_command == 'update':  # could also read `def update_task_status(id, status):` and then pass in those values to do that
    # run as `python 7.5-sqlite3.py update id status`
    id = int( sys.argv[2] )
    status = sys.argv[3]

    
    with closing( sqlite3.connect(db_filename) ) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        select details, status from task 
        where id = ?
        order by deadline
        """, ( id, ) )
        
        t_details, t_status = cursor.fetchone()
        print "Updating status of task #%s - %s to [%s]" % ( id, t_details, status )

        cursor.execute( """
        update task
        set status = :status
        where id = :id
        """, { 'status':status, 'id':id } )
        
        conn.commit()
    
## 7.5.6 Bulk Loading
# use executemany() to apply the same set of SQL instructions to a large set of data
# this avoids complicating the code with loops and lets the underlying library apply loop optimization
elif arg_command == 'insert':
    #  run as `python 7.5-sqlite3.py insert data_file.csv`
    data_filename = sys.argv[2]
    SQL = """
    insert into task (details, priority, status, deadline, project)
    values (:details, :priority, :status, :deadline, :project)
    """
    
    with closing( open( data_filename, 'r' ) ) as csv_file:
        # create a csv.DictReader to handle the data
        csv_reader = csv.DictReader(csv_file)
        
        with closing( sqlite3.connect(db_filename) ) as conn:
            cursor = conn.cursor()
            cursor.executemany(SQL, csv_reader)
            
            conn.commit()
                
print "Completed assessing arguments."