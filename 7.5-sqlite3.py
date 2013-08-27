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
def create_new_database( db_filename, schema_filename, add_starter_data=False ):
    # An SQLite db is stored as a single file on the file system
    db_is_new = not os.path.exists(db_filename)
    schema_is_new = not os.path.exists(schema_filename)

    if db_is_new or schema_is_new:
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
            
            if add_starter_data:
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
                    print "Inserting Starter Data"
                    conn.executescript(data)
    
## 7.5.2 Retrieving Data
# to retrieve values, create a cursor from a database connection.
# A cursor provides a consistent view of data and is the primary means or transacting with a relational db
def fetch_project_tasks(project_name, fetch_type = 'all'):
    with closing( sqlite3.connect(db_filename) ) as conn:
        # create cursor
        cursor = conn.cursor()
        # execute query through cursor
        cursor.execute("""
            select id, priority, details, status, deadline from task where project = ?
            """, (project_name, ) )
            
        if fetch_type == 'all':
            # read data from cursor
            for row in cursor.fetchall():
                task_id, priority, details, status, deadline = row
                print task_fmt.format( task_id, priority, details, status, deadline )
            print
        
        elif fetch_type == 'one':
            # there`s also a fetchone() that just fetches the first result,
            for row in cursor.fetchone():
                task_id, priority, details, status, deadline = row
                print task_fmt.format( task_id, priority, details, status, deadline )
            print
            
        elif fetch_type == 'many':
            # and a fetchmany(x) that just fetches [up to] x results.
            how_many = 5
            print how_many, "results:"
            for row in cursor.fetchmany( how_many ):
                task_id, priority, details, status, deadline = row
                print task_fmt.format( task_id, priority, details, status, deadline )
            
## 7.5.3 Query Metadata
# after execute() has been called, the cursor sets it's description attribute 
# to hold info about the data that will be returned by the fetch methods.
# the description = ( (column_name, type, display_size, internal_size, precision, scale, null_flag), ...)
# though, sqlite3 only returns the name, because it doesn't enforce size or type restraints
def display_columns(db_filename, project_name):
    with closing( sqlite3.connect(db_filename) ) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        select * from task where project = ?
        """, ( project_name, ) )
        
        print "\nTask table for %s has these columns:" % project_name
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
def display_rows_via_objects(db_filename, project_name):
    with closing( sqlite3.connect(db_filename) ) as conn:
        # Change the row_factory to use sqlite3.Row
        conn.row_factory = sqlite3.Row
        
        cursor = conn.cursor()
        
        cursor.execute("""
        select name, description , deadline from project
        where name = ?
        """, ( project_name, ) )
        
        p_name, description, deadline = cursor.fetchone()
        print "Project details for %s (%s) [%s]" % ( description, p_name, deadline )
        
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
def named_parameters(db_filename, project_name):
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

# query parameters can be used with select, insert, and update statements, as long as a literal value is legal in the context
def update_task_status(id, status):
    # run as `python 7.5-sqlite3.py update id status`
   
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

def insert_data_from_csv(data_filename):
    #  run as `python 7.5-sqlite3.py insert data_file.csv`
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
               

## 7.5.7 Defining New Column Types
# SQLite only supports integer, floating point, or text columns
# sqlite3 has the ability to store any type of Python data

# conversion for types supported beyond the base three is enabled in the db connection by using the detect_types flag.
# if the columns were declared using the desired type when the table was defined, PARSE_DECLTYPES will provide them



## Function Controls
if __name__ == '__main__':
    # check for special commands as arguments
    arg_command = sys.argv[1] if len(sys.argv) >= 2 else None
    if arg_command is None:
        print "No command entered"
    elif arg_command == 'create_db':
        # create a new database file using the supplied file locations
        # if any filename that doesn't exist is given, it will be created
        # if a schema filename that doesn't exist is given the schema from the book will be created
        db_filename = sys.argv[2]
        schema_filename = sys.argv[3]
        create_new_database( db_filename, schema_filename )
    elif arg_command == 'create_demo_db':
        # if you want the database to be populated with sample data matching the book's schema use this function instead
        db_filename = sys.argv[2]
        schema_filename = sys.argv[3]
        create_new_database( db_filename, schema_filename, True )
        
    elif arg_command == 'columns':
        # display the columns in the task table.
        try:
            db_filename = sys.argv[2]
        except IndexError:
            print "You must specify the db to read from"
            raise
        try:
            project_name = sys.argv[3]  ## this doesn't really make sense but it could with a little work
        except IndexError:
            print "You must specify the project name"
            raise
        display_columns( db_filename, project_name )
        
    elif arg_command == 'object_rows':
        # display the rows, like fetch, but using objects instead of tuples.
        db_filename = sys.argv[2]
        project_name = sys.argv[3]
        display_rows_via_objects( db_filename, project_name )
        
    # there are a few options when it comes to asking for the fetch commands
    elif arg_command == 'fetch' and len(sys.argv) == 3:
        # default to fetchall() if no second argument is passed
        project_name = sys.argv[2]
        fetch_project_tasks( project_name, 'all' )
    elif arg_command == 'fetch':
        # otherwise, pass in the second argument as the fetch_type
        project_name = sys.argv[2]
        fetch_type = sys.argv[3]
        fetch_project_tasks( project_name, fetch_type )
    
    elif arg_command == 'insert':
        # insert the data from the csv file specified
        csv_file_location = sys.argv[2]
        insert_data_from_csv( csv_file_location )
        
    elif arg_command == 'update':
        # update the status of the indicated task
        task_id = int( sys.argv[2] )
        new_task_status = sys.argv[3]
        update_task_status( task_id, new_task_status )
    else:
        print "Command not recognized."