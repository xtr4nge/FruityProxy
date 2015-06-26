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
from cStringIO import StringIO
from PIL import Image, ImageFile

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

fruityproxy_logger = logging.getLogger("fruityproxy")

class Upsidedown(Plugin):
    name = "Upsidedown"
    
    def request(self, request):
        pass
    
    def response(self, flow):
        pass
        try: 
            if "image" in flow.response.headers['Content-Type'][0]:
                #print " ++ " + str(flow.response.headers['Content-Type'])
                self.imageType = flow.response.headers['Content-Type'][0].split('/')[1].upper()
                isImage = True
            else:
                isImage = False
                
                
            if isImage and self.imageType in ["GIF", "JPG", "JPEG", "PNG"]:
                try:
                    data = flow.response.content
                    p = ImageFile.Parser()
                    p.feed(data)
                    im = p.close()
                    im = im.transpose(Image.ROTATE_180)
                    output = StringIO()
                    im.save(output, format=self.imageType)
                    data = output.getvalue()
                    flow.response.content = data
                    output.close()
                    fruityproxy_logger.debug("[" + self.name + "] " + "Flipped image " + self.imageType)
                except Exception as e:
                    fruityproxy_logger.error("[" + self.name + "] " + "Error: {} " + self.imageType)
                    print e
        except Exception as e:
            print e