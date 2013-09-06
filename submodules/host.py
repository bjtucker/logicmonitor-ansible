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

import sys
import json
import os
from logicmonitor import LogicMonitor

class Host(LogicMonitor):
    
    def __init__(self, collector, hostname=None, displayname=None, properties={}, groups=[], alertenable=True, credentials_file="/tmp/lm_credentials.txt"):
        """Initializor for the LogicMonitor host object"""
        LogicMonitor.__init__(self, credentials_file)
        self.collector = collector
        self.hostname = hostname or self.fqdn
        self.displayname = displayname or self.fqnd
            
    #end __init__
    
    ####################################
    #                                  #
    #    Public methods                #
    #                                  #
    ####################################    
    
    
    def getproperties(self, host):
        """Returns a hash of the properties associated with this LogicMonitor host"""
        pass
    #end getproperties

    def setproperties(self, host, propertyhash):
        """update the host to have the properties contained in the property hash"""
        pass
    #end setproperties

    def add(self):
        """Add this device to monitoring in your LogicMonitor account"""
        pass
    #end add_host

    def update(self):
        """This method takes changes made to this host and applies them to the corresponding host in your LogicMonitor account."""
        pass
    #end update_host
    
    def remove(self):
        """remove this host from your LogicMonitor account"""
        pass
    #end remove

    def sdt(self, starttime, duration):
        """create a scheduled down time (maintenance window) for this host"""
        pass
    #end sdt

    ####################################
    #                                  #
    #    internal utility methods      #
    #                                  #
    ####################################    

    def _gethosts():
        pass
    #end getHosts

    def _gethostbyhostname(hostname, collector):
        pass
    #end get_host_by_hostname

    def _gethostbydisplayname(displayname):
        pass
    #end get_host_by_displayname
    

#end class lm_host