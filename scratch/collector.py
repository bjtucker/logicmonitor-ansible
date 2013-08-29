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
import platform
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
            info = self._create()
        #end if
        self.id     = info["id"]
        self.isdown = info["isDown"]
        if not os.path.exists(installdir):
            os.makedir(installdir)
        #end if
        self.installdir    = installdir
        self.installertype = platform.system()
        self.is_64bits     = sys.maxsize > 2**32
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
        return self.installdir
    #end getinstalldir
    
    def setinstalldir(self, newinstalldir):
        """Verifies that the directory specified exists.
        sets as the LogicMonitor collector installation location"""
        if not os.path.exists(newinstalldir):
            os.makedirs(newinstalldir)
        #end if
        self.installdir = newinstalldir
    #end setinstalldir

    def getinstallerbin(self):
        """Download the LogicMonitor collector installer binary"""
        arch = 32
        if self.is_64bits:
            arch = 64
        #end
        if self.installertype == "Linux" and self.id is not None:
            installfilepath = self.installdir + "/logicmonitorsetup" + str(self.id) + "_" + str(arch) + ".bin"
            print installfilepath
            if not os.path.isfile(installfilepath):             #else create the installer file and return the file object
                with open(installfilepath, "w") as f:
                    installer = self.do("logicmonitorsetup", {"id": self.id, "arch": arch})
		    f.write(installer)
                f.closed
                #end with
            #end if not
            return installfilepath
        elif self.installertype == "Windows" and self.id is not None:
            pass
        elif self.id is None:
            print "Error: There is currently no collector associated with this device. To download the installer, first create a collector for this device."
            return None
        elif self.installertype != "Linux" and self.installertype != "Windows":
             print "Error: LogicMonitor Collector must be installed on either a Linux or Windows device."
             return None
        else:
            print "Error: Something went wrong. We were unable to retrieve the installer from the server"
            return None
        #end if
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

    def _create(self):
        """Create a new collector in the LogicMonitor account associated with this device"""
        create_json = json.loads(self.rpc("addAgent", {"autogen": True, "description": self.fqdn}))
        if create_json["status"] is 200:
            return create_json["data"]
        else:
            print "Error: Unable to create a new collector"
            print json.dumps(create_json)
            print "Exiting"
            sys.exit(1)
        #end if
    #end _create

    def _get(self):
        """Returns a JSON object representing the collector"""
        collector_list = self._getcollectors()
        if collector_list is not None:
            for collector in collector_list:
                if collector["description"] == self.fqdn:
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
