import subprocess
import sys
import colors
import random
import os
import argparse

def main(argv=None):
    # ..........................................................................
    # load command line arguments
    if argv is None:
        argv = sys.argv[1:]

    # ..........................................................................
    # parse command line arguments (argparse)
    parser = argparse.ArgumentParser()
	
    parser.add_argument('input',
                        help='List of directories to save',
                        nargs=1,
                        default=None
                        )

    parser.add_argument('--out',
                        help='Output directory',
                        required=True
                        )
    
    parser.add_argument('--sql',
                        action='store_true',
                        help='Backup the MySQL database',
                        default=False
                        )

    args = parser.parse_args(argv)

    code = 0

	input_file_path = os.path.abspath(args.input)
	output_path = os.path.abspath(args.out)
	
	os.chdir('/')
	
	backup_sql(output_path)
	
	backup_directories(input_file_path, output_path)

    exit(code)
    
# ==============================================================================
# call main if executed as script
if __name__ == '__main__':
    sys.exit(main())

