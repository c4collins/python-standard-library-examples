import zipfile, datetime
from contextlib import closing

# to access the rest of the metadata, use infolist() or getinfo()
def print_info(archive_name):
    fmt = "\t{:12} : {}"
    with closing( zipfile.ZipFile( archive_name ) ) as zf:
        for info in zf.infolist():
            if info.create_system == 0:
                system = 'Windows'
            elif info.create_system == 3:
                system = 'Unix'
            else:
                system = 'UNKNOWN'
        
            print info.filename
            print fmt.format( "Comment", info.comment )
            print fmt.format( "Modified", datetime.datetime(*info.date_time) )
            print fmt.format( "System", system )
            print fmt.format( "ZIP version", info.create_version )
            print fmt.format( "Compressed", info.compress_size ), "bytes"
            print fmt.format( "Uncompressed", info.file_size ), "bytes"
            print
