'''
Created on Feb 6, 2020

@author: Team Bear
'''
import subprocess
import os
import re
import sys
import argparse
import shutil
from collections import OrderedDict

# Adds command line options, 'filename' is positional while 'report' and 'backup' are optional.
# The 'backup' variable saves the file's name to be made a copy of. 
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("-r", "--report", action="store_true", 
                     help="returns a file with a report of data in it")
parser.add_argument("-b", "--backup", action="store_true", 
                     help="saves a backup of the makefile")
args = parser.parse_args()

# Create a backup of the file called fileBACKUP
if args.backup:
    print("Backup is being created...")
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

# Loop to store every .h file from the include paths into the directory.
dict_include = {}
for includepath in include_paths:
    # Store ONLY files in current directory and save to array
    curdir = os.listdir(includepath.strip())
    for curfile in curdir:
        # Concatenate include path and the current file
        curfilepath = includepath.strip() + '/' + curfile
        # If path is a file and not a dir, save it to dictionary of include files
        if os.path.isfile(curfilepath):
            dict_include[curfilepath] = curfile

# Loop to get every source code file
makefile_path.seek(0)
source_line = []
for line in makefile_path:
    if '.cpp' in line or '.cxx' in line or '.C' in line: 
        source_line.append(line.strip().rstrip('\\'))
makefile_path.close()

# Loop to get every header file from top of source files
count = 0
sourcelength = len(source_line)
headerfiles = []
while count < sourcelength:
    cur_source = os.path.dirname(makefile_input) + '/' + source_line[count]
    open_source = open(cur_source)
    for line in open_source:
        if '#include "' in line:
            headerfiles.append(re.search(r'\"(.*)\"', line).group(1))
    count += 1

# Loop to compare the needed header files with all of the included header files
goodheaders = []
badheaders = []
for key in dict_include:
    if dict_include[key] in headerfiles:
        goodheaders.append(key)
    else:
        badheaders.append(key)

# Print report that shows percentage of bad header files
if args.report:
    print(str(round(((len(badheaders)/len(dict_include))*100),2)) + "%" 
    + " of included header files are not being used.")

# Print our the good headers and bad headers (Test)
print("\nThe good headers:")
for i in goodheaders:
    print(i)
print("\nThe bad headers:")
for i in badheaders:
    print(i)

# Print out values in dictionary (Test)
#print(dict_include)

# Print out include paths (Test)
#for i in include_paths:
#    print(i)

# Print out the source files (Test)
#for i in source_line:
#    print(i)

# Print out the header files (Test)
#for i in headerfiles:
#    print(i)