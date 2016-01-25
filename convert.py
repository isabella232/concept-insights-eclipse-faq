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
import json
import shlex
import os
import sys
import getopt
import urllib

DOCCNV_BASEURL='https://gateway.watsonplatform.net/document-conversion/api'
DOCCNV_CREDS='username:password'
DOCCNV_CNVURL = '%s/v1/convert_document?version=2015-12-15' % (DOCCNV_BASEURL)

CSV_FILE=''
OUT_FOLDER=''
DEBUG=False
VERBOSE=''

def usage():
    print ('convert.py -u <username:password> -c <csv file> -i <input folder> -o <output folder> -d [enable debug output for script] -v [ enable verbose output for curl]')

try:
    opts, args = getopt.getopt(sys.argv[1:],"hdvu:c:i:o:",["user=","in_csvfile=","inputfolder=","outputfolder="])
except getopt.GetoptError as err:
    print str(err)
    print usage()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ("-u", "--user"):
        DOCCNV_CREDS = arg
    elif opt in ("-c", "--in_csvfile"):
        CSV_FILE = arg
    elif opt in ("-i", "--inputfolder"):
        IN_FOLDER = arg
    elif opt in ("-o", "--outputfolder"):
        OUT_FOLDER = arg
    elif opt == '-d':
        DEBUG = True
    elif opt == '-v':
        VERBOSE = '-v'

if not CSV_FILE or not IN_FOLDER or not OUT_FOLDER:
    print ('Required argument missing.')
    usage()
    sys.exit(2)

print("Input csv file is %s" % (CSV_FILE))
print("Output folder is %s" % (OUT_FOLDER))

with open(CSV_FILE, 'rb') as in_csvfile:
    input_csv = csv.reader(in_csvfile)
    print ('Converting Official Eclipse FAQ data...')
    for row in input_csv:
        if len(row) == 0:
            continue

        docid = row[0]
        title = row[2]
        url = row[3]
        
        htmlfilename = '%s/%s.html' % (IN_FOLDER, docid)
        jsonfilename = '%s/%s.json' % (OUT_FOLDER, docid)
        titlefilename = '%s/%s.title.txt' % (OUT_FOLDER, docid)
        bodyfilename = '%s/%s.body.txt' % (OUT_FOLDER, docid)
        
        print('Processing %s' % (htmlfilename))
        
        try:
            os.remove(jsonfilename)
        except OSError:
            pass
        
        try:
            os.remove(titlefilename)
        except OSError:
            pass
        
        try:
            os.remove(bodyfilename)
        except OSError:
            pass

        curl_cmd = 'curl -k -s %s -u %s -F "config={\\"conversion_target\\":\\"ANSWER_UNITS\\"}" -F "file=@%s" "%s"' % (VERBOSE, DOCCNV_CREDS, htmlfilename, DOCCNV_CNVURL)
        if DEBUG:
            print (curl_cmd)
        process = subprocess.Popen(shlex.split(curl_cmd), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        with open(jsonfilename, "a") as jsonfile:
            jsonfile.write(output)
        if DEBUG:
            print (output)
        try:
            parsed_json = json.loads(output)
            answer_units = parsed_json['answer_units']
            for answer_unit in answer_units:
                if answer_unit['type'] == 'h1':
                    title = answer_unit['title'].encode('utf8')
                    with open(titlefilename, "w") as titlefile:
                        titlefile.write(title)
                    body = answer_unit['content'][0]['text'].encode('utf8')
                    with open(bodyfilename, "w") as bodyfile:
                        bodyfile.write(body)
        except:
            print ('Command:')
            print (curl_cmd)
            print ('Response:')
            print (output)
            raise    
    print ('Converting data complete.')
            

