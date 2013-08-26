## whichdb - Identify DBM-Style Database Formats
import platform
from contextlib import closing

# anydbm and which db were merged into dbm in python3, so it's a little different
# most of the examples are just python2 (because that's what I use)
# but I figured since this was such a short section I'd implement it in python3 too

if platform.python_version() >= '3':
    exec("print( 'python version:', platform.python_version() )")
    import dbm
    # use contextlib.closing to handle the db's close()
    with closing( dbm.open('data/7.3-dbm_type.db', 'n') ) as db:
        db['key']    = 'value'

    exec("print( 'whichdb?:', dbm.whichdb('data/7.3-dbm_type.db') )")
else:
    exec("print 'python version:', platform.python_version()")
    import anydbm, whichdb
    # use contextlib.closing to handle the db's close()
    with closing( anydbm.open('data/7.3-dbm_type.db', 'n') ) as db:
        db['key']    = 'value'

    exec("print 'whichdb?:', whichdb.whichdb('data/7.3-dbm_type.db')")
