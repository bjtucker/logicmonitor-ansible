#!/usr/bin/python
#
# basic_api_call.py
# Purpose:
#   Add abstraction and simplify the building of URL's,
#   making HTTPS requests (specifically RPC calls to LogicMonitor's API)
#
# Parameters:
#   Authentication - 
#      (String) c = companyname
#      (String) u = username
#      (String) p = password
#   (String) call -
#      The RPC to invoke
#   (Dictionary) params -
#      A dictionary of the parameters to be used in the API call
#      e.g {"property1": "value1", "integerProperty": 12345}
#
#
# Author: Ethan Culler-Mayeno
#

import urllib
import urlparse
import sys
import json
import os
import shlex

args_file = sys.argv[1]
args_data = file(args_file).read()


def rpc(action, params):
    """Make a call to the LogicMonitor RPC library and return the response"""
    print "Calling action: %s" % action
    print "Parameters: %s" % str(params)
    param_str = urllib.urlencode(params)
    creds = urllib.urlencode({"c": company, "u": user, "p": password})
    if param_str:
        param_str = param_str + "&"
    param_str = param_str + creds
    try:
        f = urllib.urlopen("https://{0}.logicmonitor.com/santaba/rpc/{1}?{2}".format(company, action, param_str))
        return f.read()
    except IOError as ioe:
        print ioe
    #end try
#end rpc

arguments = shlex.split(args_data)
for arg in arguments:
    if arg.find("=") != -1:
        (key, value) = arg.split("=")
        if key == "action":
            response = json.loads(rpc(value, {"hostGroupId": 1}))
            if response['status'] == 200:
                print json.dumps(response)
            else:
                print json.dumps({
                    "failed" : True,
                    "msg"    : "failed requesting %s" % value
                })
                sys.exit(1)




