import subprocess
import sys
import random
import os
import argparse
import shutil

def restore_mysql(input_path):
    os.chdir(input_path)
    
    mysql_dump_tgz = 'database.sql.tar.gz'
    if os.path.isfile(mysql_dump_tgz):
        # extract
        mysql_dump_sql = 'database.sql'
        cmd = ['tar','-xf',mysql_dump_tgz]
        code = subprocess.call(cmd)
        if code != 0:
            print('Error when extracting the mysql dump archive')
            return code
        
        cmd = 'mysql -u root -p < {}'.format(mysql_dump_sql)
        code = subprocess.call(cmd, shell=True)
        if code != 0:
            print('Error when restoring the mysql database')
            return code
        
    return 0

def restore_folders(input_path):
    os.chdir('/')
    errors_occurred = False
    for file_path in os.listdir(input_path):
        abs_file_path = os.path.abspath(input_path + os.sep + file_path)
        stem, ext = os.path.splitext(abs_file_path)
        if ext == '.tgz':
            print('Processing {}'.format(abs_file_path))
            cmd = ['tar','xf',abs_file_path]
            code = subprocess.call(cmd)
            if code != 0:
                print('Error when processing {}'.format(abs_file_path))
                errors_occurred = True
    if errors_occurred:
        return -1
    else:
        return 0
    


def main(argv=None):
    # ..........................................................................
    # load command line arguments
    if argv is None:
        argv = sys.argv[1:]

    # ..........................................................................
    # parse command line arguments (argparse)
    parser = argparse.ArgumentParser()
    
    parser.add_argument('folder',
                        help='Input backup folder',
                        default=None
                        )

    args = parser.parse_args(argv)
    
    code = 0

    input_path = os.path.abspath(args.folder)
    current_working_directory = os.path.abspath(os.getcwd())

    # restore MySQL
    code = restore_mysql(input_path)
    if code != 0:
        print('MySQL restore failed')
        return code
    
    # restore folders
    code = restore_folders(input_path)
    if code != 0:
        print('Directories restore not completed successfully')
        return code

    return code

    
# ==============================================================================
# call main if executed as script
if __name__ == '__main__':
    sys.exit(main())

