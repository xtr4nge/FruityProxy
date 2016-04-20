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

import os

try:
    from mitmproxy import controller, proxy # mitmproxy 0.17
    from mitmproxy.proxy.server import ProxyServer # mitmproxy 0.17
    from mitmproxy.models import decoded # mitmproxy 0.17
except:
    from libmproxy import controller, proxy # mitmproxy 0.15
    from libmproxy.proxy.server import ProxyServer # mitmproxy 0.15
    from libmproxy.models import decoded # mitmproxy 0.15

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

logger = logging.getLogger("fruityproxy")

class DNSspoof(Plugin):
    name = "DNSspoof"
    version = "1.1"
    
    def request(self, flow):
        
        request_pretty_host = flow.request.pretty_host
        request_host = flow.request.host
        
        for item, v in self.config[self.name]['domains'].iteritems():
            domainRedirect = v.split("|")
            wild_card = ""
            
            if len(domainRedirect[0]) > 1:
                wild_card = domainRedirect[0].split(".")[0]
                wild_domain = domainRedirect[0].replace("*.","").replace("*","")
            
            if domainRedirect[0] == "*":
                flow.request.host = domainRedirect[1]
                logger.debug("["+self.name+"] " + request_pretty_host + " to " + domainRedirect[1])
                break
                '''
                elif flow.request.pretty_host.endswith(wild_domain) and wild_card == "*":
                    flow.request.host = domainRedirect[1]
                    logger.debug("["+self.name+"] " + request_pretty_host + " to " + domainRedirect[1])
                    break
                '''
            
            elif flow.request.pretty_host.endswith(domainRedirect[0]):
                #elif flow.request.pretty_host(hostheader=True).endswith(domainRedirect[0]): # mitmproxy 0.15 [remove]
                flow.request.host = domainRedirect[1]
                #print flow.request.path
                logger.debug("["+self.name+"] " + request_pretty_host + " to " + domainRedirect[1])
                #flow.request.update_host_header() # mitmproxy 0.15 [remove]
                break
    
    def response(self, flow):
        pass
    