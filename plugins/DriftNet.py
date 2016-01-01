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

import os, time
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from cStringIO import StringIO
from PIL import Image, ImageFile

import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

from datetime import datetime

logger = logging.getLogger("fruityproxy")

class DriftNet(Plugin):
    name = "DriftNet"
    version = "1.1"
    
    def request(self, flow):
        pass
    
    def response(self, flow):
        pass
        
        if os.path.isdir("logs/" + self.name) == False:
                self.createDir("logs/" + self.name)
    
        try:
            if "image" in flow.response.headers['Content-Type']:
                self.imageType = flow.response.headers['Content-Type'].split('/')[1].upper()
                isImage = True
            else:
                isImage = False
                
                
            #if isImage and self.imageType in ["GIF", "JPG", "JPEG", "PNG"]:
            if isImage:
                try:
                    
                    client_conn = str(flow.client_conn)
                    server_conn = str(flow.server_conn)
                    
                    client = flow.client_conn.address()[0]
                    
                    thePath = flow.request.path
                    theUrl = flow.request.url
                    theHost = flow.request.host
                    
                    temp = thePath.split("/")
                    temp = temp[len(temp) - 1]
                    temp = temp.split("?")[0]			
                    theFile = temp.split(".")
                                        
                    fileName = theFile[0] + "." + self.imageType.lower()
                    
                    data =  flow.response.content
                    
                    millis = int(round(time.time() * 1000))
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%S_%s")
                    
                    pathDir = "logs/" + self.name + "/" + client + "/" + theHost + "/"
                    if os.path.isdir(pathDir) == False:
                        self.createDir(pathDir)
                    
                    f = open(pathDir + str(timestamp) + "_" + fileName,'w')
                    f.write(data)
                    f.close()
                    
                    logger.debug("[" + self.name + "] " + client + " saved image " + self.imageType)
                except Exception as e:
                    logger.error("[" + self.name + "] " + client + " error: {} " + self.imageType)
                    print e
        except Exception as e:
            pass
            #print e
            
    def createDir(self, path):
        try:
            os.makedirs(path)
        except OSError:
            pass
