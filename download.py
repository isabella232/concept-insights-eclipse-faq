#  Copyright 2016 IBM Corp. All Rights Reserved.
# 
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#!/usr/bin/env python
import csv
import subprocess
import shlex
import sys
import getopt

CSV_FILE=''
OUT_FOLDER=''
DEBUG=False
VERBOSE=''

def usage():
    print ('download.py -c <csv file> -o <output folder> -d [enable debug output for script] -v [enable verbose output for curl]')

try:
    opts, args = getopt.getopt(sys.argv[1:],"hdv:c:o:",["in_csvfile=","outputfolder="])
except getopt.GetoptError as err:
    print str(err)
    print usage()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ("-c", "--inputcsvfile"):
        CSV_FILE = arg
    elif opt in ("-o", "--outputfolder"):
        OUT_FOLDER = arg
    elif opt == '-d':
        DEBUG = True
    elif opt == '-v':
        VERBOSE = '-v'

if not CSV_FILE or not OUT_FOLDER:
    print ('Required argument missing.')
    usage()
    sys.exit(2)

print("Input csv file is %s" % (CSV_FILE))
print("Output folder is %s" % (OUT_FOLDER))

with open(CSV_FILE, 'rb') as in_csvfile:
    input_csv = csv.reader(in_csvfile)
    
    print ('Downloading Official Eclipse FAQ HTMLs...')
    
    for row in input_csv:
        if len(row) == 0:
            continue

        docid = row[0]
        title = row[2]
        url = row[3]
        print('Processing %s: %s' % (docid, title))
        
        htmlfilename = '%s/%s.html' % (OUT_FOLDER, docid)
        curl_cmd = 'curl -k -s %s -o %s %s' % (VERBOSE, htmlfilename, url)
        if DEBUG:
            print (curl_cmd)
        subprocess.Popen(shlex.split(curl_cmd), stdout=subprocess.PIPE)

    print ('Downloading HTMLs complete.')
            

