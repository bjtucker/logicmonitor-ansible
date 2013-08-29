#!/usr/bin/python
#
# collector.py
# Purpose:
#   Allow for the use of logicmonitor collector management functions
#
# Parameters:
#
# Author: Ethan Culler-Mayeno
#

import json
import sys
import os
from logicmonitor import LogicMonitor

class Collector(LogicMonitor):
    
    ####################################
    #                                  #
    #    create/initialize/destroy     #
    #                                  #
    ####################################
    
    
    def __init__(self, installdir="/usr/local/logicmonitor", credentials_file="/tmp/lm_credentials.txt"):
        """docstring for %s"""
        LogicMonitor.__init__(self, credentials_file)
        info = self._get()
        if info is None:
            self.id     = None
            self.isdown = None
        else:
            self.id     = info["id"]
            self.isdown = info["isDown"]
        #end if
        self.installdir = installdir
    #end __init__
    
    ####################################
    #                                  #
    #    Public API functions          #
    #                                  #
    ####################################
    
    
    def getid(self):
        """docstring for get_collectors"""
        return self.id
    #end get_collector

    def getinstalldir(self):
        """Return path of the directory for installation of the LogicMonitor collector"""
        pass
    #end getinstalldir

    def getinstallerbin(self, installdir):
        """Download the LogicMonitor collector installer binary"""
        pass
    #end getinstallerbin
    
    def install(self, installdir):
        """Execute the LogicMonitor installer"""
        pass
    #end install

    def uninstall(self, installdir):
        """docstring for install"""
        pass
    #end uninstall
    
    def start(self):
        """Start the LogicMonitor collector"""
        pass
    #end start
    
    def restart(self):
        """Restart the LogicMonitor collector"""
        pass
    #end restart
    
    def stop(self):
        """Stop the LogicMonitor collector"""
        pass
    #end stop
    

    ####################################
    #                                  #
    #    internal utility functions    #
    #                                  #
    ####################################

    def _get(self):
        """Returns a JSON object representing the collector"""
        collector_list = self._getcollectors()
        if collector_list is not None:
            for collector in collector_list:
                if collector["description"] is self.fqdn:
                    return collector
                #end if
            #end for
        #end if
        return None
    #end _get
    

    def _getcollectors(self):
        """Returns a JSON object containing a list of LogicMonitor collectors"""
        resp = self.rpc("getAgents", {})
        resp_json = json.loads(resp)
        if resp_json["status"] is 200:
            return resp_json["data"]
        else:
            print "Error: Unable to retrieve the list of collectors from the server"
            print "Exiting"
            sys.exit(1)
        #end if
    #end _getcollectors
        

#end Collector

# testing

c = Collector()