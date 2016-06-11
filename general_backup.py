import subprocess
import sys
import colors
import random
import os
import argparse

# Output files:
# output_path/database.sql.tgz
# output_path/archive_###.tgz

def backup_sql(output_path):
	# create SQL dump
	dumpfile = output_path + os.sep + 'database.sql'
	cmd = 'mysqldump -u root -p --all-databases > {}'.format(output_path)
	code = subprocess.call(cmd, shell=True)
	if code != 0:
		return code
		
	# compress the dump
	dump_compressed_file = output_path + os.sep + 'database.sql.tgz'
	cmd = []
	cmd.append('tar')
	cmd.append('-avcf')
	cmd.append(dump_compressed_file)
	cmd.append(dumpfile)
	code = subprocess.call(cmd)
	
	return code
	
	
def find_abs_path_relative_of(query_path, relative_path):
	previous_working_dir = os.path.abspath(os.getcwd())
	os.chdir(relative_path)
	result = os.path.abspath(query_path)
	os.chdir(previous_working_dir)
	return result
	
	
def backup_directories(input_file_path, output_path, original_working_directory):
	os.chdir('/')
	try:
		input_file = open(input_file_path, 'r')
	except:
		print('Error opening file {}'.format(input_file_path))
		return -1
	
	counter = 0
	for line in input_file:
		input_folder_path = find_abs_path_relative_of(line, original_working_directory)
		output_archive_name = output_path + os.sep + 'archive_{}.tgz'.format(counter)
		cmd = []
		cmd.append('tar')
		cmd.append('-avcf')
		cmd.append(output_archive_name)
		cmd.append(input_folder_path)
		code = subprocess.call(cmd)
		if code != 0:
			print('Error when compressing folder {}'.format(line))
			return code
			
	return 0
	

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
                        default=None,
						required=True
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
	current_working_directory = os.path.abspath(os.getcwd())

	
	if args.sql:
		code = backup_sql(output_path)
	if code != 0:
		print('MySQL backup returned {}'.format(code))
		return code
	
	code = backup_directories(input_file_path, output_path, current_working_directory)
	if code != 0:
		print('Directories backup not completed successfully')
		return code

    return code
    
# ==============================================================================
# call main if executed as script
if __name__ == '__main__':
    sys.exit(main())

