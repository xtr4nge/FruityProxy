#!/usr/bin/env python

# Copyright (C) 2015 xtr4nge [_AT_] gmail.com
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

import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

fruityproxy_logger = logging.getLogger("fruityproxy")

class Survey(Plugin):
    name = "Survey"
    
    def request(self, flow):
        pass
    
        theUrl = flow.request.url
        theHost = flow.request.host
        thePath = flow.request.path
        theHeaders = flow.request.headers
        
        temp = thePath.split("/")
        temp = temp[len(temp) - 1]
        temp = temp.split("?")[0]
        theFile = temp.split(".")
        
        #if theFile[-1].lower() in ["gif","jpg","png","ico","js","php","asp","jsp","doc","docm","docx","xls","xlsx","xlsm"]:
        if theFile[-1].lower() in self.config[self.name]['extensions'].split("|"):
            #print "+ " + temp + " | " + theHost
            fruityproxy_logger.debug("["+self.name+"] " + theHost + " | " + temp)

    def response(self, response):
        pass
    
