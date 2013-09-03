#!/usr/bin/python
#
# host.py
# Purpose:
#   Allow for the use of host management functions
#
# Parameters:
#
# Author: Ethan Culler-Mayeno
#

import urllib
import urlparse
import sys
import json
import os
import shlex
import logicmonitor

class lm_host(LogicMonitor):
    
    def __init__(self, args):
        args_file = sys.argv[1]
        args_data = file(args_file).read()

    #end __init__

    def __new__(self, args):
        pass
    #end __new__
    
    
    def get_hosts():
        pass
    #end getHosts

    def get_host_by_hostname(hostname, collector):
        pass
    #end get_host_by_hostname

    def get_host_by_displayname(displayname):
        pass
    #end get_host_by_displayname

    def get_host_props(self, host):
        """docstring for get_host_props"""
        pass
    #end get_host_props

    def add_host():
        pass
    #end add_host

    def update_host():
        pass
    #end update_host


#end class lm_host