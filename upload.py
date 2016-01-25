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
import random
import datetime
import string

DOCCNV_BASEURL='https://gateway.watsonplatform.net/concept-insights/api'
DOCCNV_CREDS='username:password'

CSV_FILE=''
DEBUG=False
VERBOSE=''
ACCOUNT_ID=''

def usage():
    print ('upload.py -u <username:password> -a <account id> -c <csv file> -i <input folder> -d [enable debug output for script] -v [ enable verbose output for curl]')

def generateUnid(amount = 8, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(amount))

try:
    opts, args = getopt.getopt(sys.argv[1:],"hdvu:a:c:i:",["user=","accountid=","in_csvfile=","inputfolder="])
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
    elif opt in ("-a", "--accountid"):
        ACCOUNT_ID = arg
    elif opt == '-d':
        DEBUG = True
    elif opt == '-v':
        VERBOSE = '-v'

print("Input folder is %s" % (IN_FOLDER))
print("Account id is %s" % (ACCOUNT_ID))

DOCCNV_CNVURL = '%s/v2/corpora/%s/eclipseFAQCorpus/documents/' % (DOCCNV_BASEURL, ACCOUNT_ID)

with open(CSV_FILE, 'rb') as in_csvfile:
    input_csv = csv.reader(in_csvfile)
    print ('Uploading Official Eclipse FAQ data...')
    for row in input_csv:
        if len(row) == 0:
            continue

        docid = row[0]
        title = row[2]
        url = row[3]
        bodyfilename = '%s/%s.body.txt' % (IN_FOLDER, docid)
        titlefilename = '%s/%s.title.txt' % (IN_FOLDER, docid)

        with open(bodyfilename, "r") as bodyfile:
            data = [dataPt.rstrip('\n') for dataPt in bodyfile]
        body=" " .join(data)

        body = body.replace('"', '')
        body = body.replace("'", "" )

        with open(titlefilename, "r") as titlefile:
            data = [dataPt.rstrip('\n') for dataPt in titlefile]
        title=" " .join(data)
        title = title.replace('"', '')
        title = title.replace("'", "" )        
        
        URL = DOCCNV_CNVURL + generateUnid()
        DOC_JSON = '{"label":"' + title + '","parts":[{"data":"' + body + '","name":"Text part","content-type":"text/plain"}]}'
        curl_cmd = 'curl -k -s -u %s -X PUT "%s" -d ' % (DOCCNV_CREDS, URL)
        curl_cmd = curl_cmd + "'" + DOC_JSON + "'"
        
        if DEBUG:
            print (curl_cmd)

        subprocess.Popen(shlex.split(curl_cmd), stdout=subprocess.PIPE)
          
    print ('Uploading data complete.')
            

