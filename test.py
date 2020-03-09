'''
Created on Feb 6, 2020

@author: Normal
'''
import subprocess
import os
import re
import sys

# Check to see if help option is an argument. Print if it is, else exit the system.
for arg in sys.argv:
    if(arg == '-help'):
        print("here is a help menu")
        sys.exit()

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
    include_paths[counter] = (re.sub(r'.*\$', '$', tempString)).rstrip()
    counter += 1

# Print out strings
for i in include_paths:
    print(i)
