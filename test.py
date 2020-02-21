'''
Created on Feb 6, 2020

@author: Normal
'''
import subprocess
import os
import re

# Check to make sure file exists. If not, keep asking until valid path is given.
file_exists = True
while file_exists:     
    # ask user for path name of makefile and save into a variable
    print('Enter the path name for your makefile:')
    makefile_input = input()
    # Check path exists
    if os.path.exists(makefile_input):
        print('File located, beginning scan')
        file_exists = False
    else:
        print('Invalid file location. Try again.')
        file_exists = True

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


