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
from libmproxy.protocol.http import decoded # mitmproxy 0.12

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

logger = logging.getLogger("fruityproxy")

class Replace(Plugin):
    name = "Replace"
    version = "1.1"
    
    def response(self, flow):
        pass
    
        if "text/html" in flow.response.headers['Content-Type'][0]:
            with decoded(flow.response):
                for item, v in self.config[self.name]['regex'].iteritems():        
                    #if v.split("||")[0] in flow.request.host and self.theFlag == False:
                    str_search = v.split("||")[0]
                    str_replace = v.split("||")[1]
                    if str_search in flow.response.content:
                        flow.response.content = flow.response.content.replace(str_search, str_replace)
                        logger.debug("["+self.name+"] " + str_search + " to " + str_replace + " in " + flow.request.host)
        
