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

import os, sys, getopt
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer

from core.ProxyHandler import ProxyHandler
import logging
import threading
from configobj import ConfigObj
from flask import Flask
import json

from plugins.plugin import Plugin

# ------------------------------------
# LOGS (setup)
# ------------------------------------
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logFormatter = logging.Formatter("%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
fruityproxy_logger = logging.getLogger('fruityproxy')
fileHandler = logging.FileHandler("./logs/fruityproxy.log")
fileHandler.setFormatter(logFormatter)
fruityproxy_logger.addHandler(fileHandler)

# ------------------------------------
# HELP
# ------------------------------------
gVersion = "1.0"

def usage():
    print "\nFruityProxy " + gVersion + " by @xtr4nge"
    
    print "Usage: FruityProxy <options>\n"
    print "Options:"
    print "-l <port>, --listen=<port>         Port to listen on (default 8080)."
    print "-a <port>, --listenapi=<port>      Port to listen on [API] (default 8081)."
    print "-s <server>, --upstreamserver      Upstream proxy mode (server)"
    print "-p <port>, --upstreamport          Upstream proxy mode (port)"
    print "-h                                 Print this help message."
    print ""
    print "FruityWifi: http://www.fruitywifi.com"
    print "libmproxy:  https://mitmproxy.org/doc/scripting/libmproxy.html"
    print ""

def parseOptions(argv):
    listenPort     = 8080
    listenPortApi  = 8081
    upStreamServer = False
    upStreamPort   = False
    
    try:                                
        opts, args = getopt.getopt(argv, "hl:a:s:p:", 
                                   ["help","listen=","apiport=","upstreamserver=", "upstreamport="])
        
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            elif opt in ("-l", "--listen"):
                listenPort = arg
            elif opt in ("-s", "--upstreamserver"):
                upStreamServer = arg
            elif opt in ("-p", "--upstreamport"):
                upStreamPort = arg
            elif opt in ("-a", "--listenapi"):
                listenPortApi = arg

        return (listenPort, listenPortApi, upStreamServer, upStreamPort)
                    
    except getopt.GetoptError:
        usage()
        sys.exit(2)

(listenPort, listenPortApi, upStreamServer, upStreamPort) = parseOptions(sys.argv[1:])

# ------------------------------------
# FruityProxy (setup)
# ------------------------------------
if upStreamServer == False or upStreamPort == False:
    config = proxy.ProxyConfig(port=listenPort)
    start_msg = "FruityProxy running on port " +  str(listenPort)
else:
    config = proxy.ProxyConfig(port=listenPort, mode="upstream",upstream_server=[False, False, upStreamServer, int(upStreamPort)])
    start_msg = "FruityProxy running on port " +  str(listenPort) + ", upstream proxy: " + str(upStreamServer) + ":" + str(upStreamPort)
    
server = ProxyServer(config)
m = ProxyHandler(server)

def startProxy():
    try:
        m.run()
    except:
        pass
    

# ------------------------------------
# API
# ------------------------------------
app = Flask(__name__)

@app.route("/getTest")
def getTest():
    return json.dumps(m.getTest())

@app.route("/getConfig")
def getConfig():
    return json.dumps(m.getConfig())

@app.route("/getModulesStatus/<plugin>")
def getModulesStatus(plugin):
    return json.dumps(m.getModulesStatus(plugin))

@app.route("/setModulesStatus/<module>/<status>")
def setModulesStatus(module, status):
    if status == "1":
        output = "enabled"
    else:
        output = "disabled"
    logging.debug("[Module]["+module+"] " + output )
    return json.dumps(m.setModulesStatus(module, status))

@app.route("/getModulesList")
def getModulesList():
    print json.dumps(m.getModulesList())
    return json.dumps(m.getModulesList())

@app.route("/getModulesStatusAll")
def getModulesStatusAll():
    return json.dumps(m.getModulesStatusAll())


def startFlask():
    app.run(host='127.0.0.1', port=listenPortApi)



if __name__ == "__main__":
    try:
        pool = {}
        print "Starting FruityProxy..."
        fruityproxy_logger.debug(start_msg)
        t = threading.Thread(name="Proxy", target=startProxy)
        t.setDaemon(True)
        t.start()
        
        print "Starting FruityProxy [API]..."
        a = threading.Thread(name="Api", target=startFlask)
        a.setDaemon(True)
        a.start()
    
        while True:
            pass
    
    except KeyboardInterrupt:
        pass
        print
        print "Shutting down fruitywifi-proxy..."
        print "Shutting down fruitywifi-api..."
        server.socket.close()
    except Exception as e:
        pass
        server.socket.close()
        fruityproxy_logger.error(e)
    finally:
        print "bye ;)"
