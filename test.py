'''
Created on Feb 6, 2020

@author: Normal
'''
import subprocess
import os
import re
import sys
import argparse
import shutil

# array of needed .h files = [need.h, this.h, that.h]
# Find way to remove duplicate .h files

# dict for all the includes = 
#   [{/test/path/CI : actualfilename1.h}, {/test/path/CI : actualfilename2.h}, {}, {}]

# Adds command line options, 'filename' is positional while 'report' and 'backup' are optional.
# The 'backup' variable saves the file's name to be made a copy of. 
# **Still needs save functionality.**
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("-r", "--report", action="store_true", 
                     help="returns a file with a report of data in it")
parser.add_argument("-b", "--backup", action="store_true", 
                     help="saves a backup of the makefile")
args = parser.parse_args()

# If options are set, return correct output.
# Print report of things that make Donny boy look good.
if args.report:
    print("here report boy.")
# Create a backup of the file called fileBACKUP
if args.backup:
    print("here backup boy.")
    shutil.copy2(args.filename, (re.sub("\.make", "BACKUP.make", args.filename)))

# Check to make sure the correct version of python is being used to run this script.
# Check first number of version
if (sys.version_info[0] != 3): 
    raise Exception("You are not using the supported version of Python (3.3) for this script.")
else:
    # Check second number of version
    if((sys.version_info[1] != 3)): 
        raise Exception("You are not using the supported version of Python (3.3) for this script.")

# Save file location from command line arguments and check to make sure file exists. 
# Must use quotation marks around file location, or else cmd will see it as multiple args.
makefile_input = sys.argv[1]
if os.path.exists(makefile_input):
    print('File located, beginning scan')
else:
    raise Exception("File not found")

# Find all lines that have include paths and store them in an array
makefile_path = open(makefile_input)
include_paths = []
for line in makefile_path:
    if '-I' in line: 
        include_paths.append(line)

# Loop to extract the include path and remove everything else
counter = 0
IncludePathsCounter = len(include_paths)
while counter < IncludePathsCounter:
    tempString = include_paths[counter]
    # Remove -I at beginning of string
    include_paths[counter] = (re.sub(r'.*\$', '$', tempString)).strip(' ').rstrip()
    # Get just the $(...) from the string
    tempString = re.search(r'\$\(.*\)', include_paths[counter])
    tempString = tempString.group().strip(' ')
    # Get just the variable name from the $(...)
    tempString = re.search(r'\(([^\)]+)', tempString).group(1).strip(' ')
    # Restart line reader in file
    makefile_path.seek(0)
    for i in makefile_path:
        # Find EXACT word in each line
        if (re.search(r'\b' + tempString + r'\b', i) is not None and '=' in i):
            # Strip variable name
            tempVar = re.search(r'=.*$', i).group().strip(' ')
            # Strip equals sign
            tempVar = (re.sub(r'=', '', tempVar)).strip(' ')
            # Replace the $(...) with the actual include path. Strip \ if at end
            include_paths[counter] = (re.sub(r'\$.*\)', tempVar, include_paths[counter])).strip(' ').rstrip('\\')
            break
    counter += 1
makefile_path.close()

# Print out strings
for i in include_paths:
    print(i)
