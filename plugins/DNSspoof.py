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
from libmproxy.protocol.http import decoded

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

logger = logging.getLogger("fruityproxy")

class DNSspoof(Plugin):
    name = "DNSspoof"
    version = "1.0"
    
    def request(self, flow):
        for item, v in self.config[self.name]['domains'].iteritems():
            domainRedirect= v.split("|")
            if domainRedirect[0] == "*":
                flow.request.host = domainRedirect[1]
                logger.debug("["+self.name+"] " + domainRedirect[0] + " to " + domainRedirect[1])
                flow.request.update_host_header()
            elif flow.request.pretty_host(hostheader=True).endswith(domainRedirect[0]):
                flow.request.host = domainRedirect[1]
                print flow.request.path
                logger.debug("["+self.name+"] " + domainRedirect[0] + " to " + domainRedirect[1])
                flow.request.update_host_header()
    
    def response(self, flow):
        pass
    