# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Author - Naresh Ganatra
# http://youtube.com/c/NareshGanatra


from __future__ import print_function
# from future.standard_library import install_aliases
# install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask, jsonify
from flask import request
from flask import make_response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Prescient") # Open the spreadhseet

sheet_1 = client.open("Prescient").sheet1  # Open the spreadhseet
data_1= sheet_1.get_all_records() 
sheet_2 = sheet.get_worksheet(1)
# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = (req)
    
    if req['queryResult']['action'] == "savename":
        response = makeWebhookResult(res)
        r = jsonify(response)
        r.headers['Content-Type'] = 'application/json'
        return r
    

def makeWebhookResult(res):
 # Get a list of all records
    name = res["queryResult"]['parameters']['person']['name']
    email = res["queryResult"]['parameters']['email']
    phone = res["queryResult"]['parameters']['phone-number']
    insertRow = [name, email, phone]
    sheet_1.insert_row(insertRow, 2)
    


    speech_1 = "Okay {}. We will contact you on either {} or {}.".format(name, email, phone)

    # Naresh
    return {

        "fulfillmentText": speech_1
        
    }


@app.route('/test', methods=['GET'])
def test():
    return "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message = "this is the message"

    my_result = {

        "fulfillmentText": string,
        "source": string
    }

    res = json.dumps(my_result, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')