#!/usr/bin/env python

# Copyright (C) 2015-2016 xtr4nge [_AT_] gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os, sys

try:
    from mitmproxy import controller, proxy # mitmproxy 0.17
    from mitmproxy.proxy.server import ProxyServer # mitmproxy 0.17
except:
    from libmproxy import controller, proxy # mitmproxy 0.15
    from libmproxy.proxy.server import ProxyServer # mitmproxy 0.15

from plugins import *

from configobj import ConfigObj
import json

class ProxyHandler(controller.Master):
    
    context = []
    
    plugin_classes = plugin.Plugin.__subclasses__()
    plugins = []
    for p in plugin_classes:
        plugins.append(p())
            
    def __init__(self, opts, server):
        controller.Master.__init__(self, opts, server)
        self.stickyhosts = {}
        self.config = ConfigObj("fruityproxy.conf")

    def getStatus(self, name):
        self.config = ConfigObj("fruityproxy.conf")
        if self.config[name]['status'] == "enabled":            
            return True
        else:
            return False

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()    

    def handle_request(self, flow):
        
        '''
        print "-- request --"
        print flow.__dict__
        print flow.request.__dict__
        print flow.request.headers.__dict__
        print "--------------"
        print
        '''
        
        #flow.request.host = flow.request.headers["host"][0] # mitmproxy 0.15 [remove]
        flow.request.host = flow.request.headers["host"]
        #flow.request.update_host_header() # mitmproxy 0.15 [remove]
        
        for p in self.plugins:
            try:
                if self.getStatus(p.name):
                    p.request(flow)
            except Exception as e:
                print "error..."
                print e
        
        #flow.request.update_host_header() # mitmproxy 0.15 [remove]
        flow.reply()

    def handle_response(self, flow):
        
        '''
        print
        print "-- response --"
        print flow.__dict__
        print flow.response.__dict__
        print flow.response.headers.__dict__
        print "--------------"
        print
        '''
        for p in self.plugins:
            try:
                if self.getStatus(p.name):
                    p.response(flow)
            except Exception as e:
                print "error..."
                print e
        
        flow.reply()
    
    # RESTful API getter|setter

    def getConfig(self):
        data = {}
        return data
        
    def getModulesStatus(self, plugin):
        data = {}
        data[plugin] = self.config[plugin]['status']
        return data

    def setModulesStatus(self, plugin, status):
        if status == "1":
            self.config[plugin]['status'] = "enabled"
            self.config.write()
        elif status == "0":
            self.config[plugin]['status'] = "disabled"
            self.config.write()
        return self.getModulesStatus(plugin)
            
    def getModulesList(self):
        data = []
        for item in self.config.inline_comments:
            data.append(item)
        return data
    
    def getModulesStatusAll(self):
        data = {}
        for item in self.config.inline_comments:
            data[item] = self.config[item]["status"] 
        return data
    
