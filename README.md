# FruityProxy
<br>- FruityProxy allows MITM attacks. 
<br>- MITMproxy inline scripts can be imported. 
<br>- It is possible to set it in upstream mode. 
<br>- FruityProxy is part of FruityWifi project. 
<br>- It provides a RESTful API.


<br>Usage: FruityProxy <options>
<br>
<br>Options:
<br>`-l <port>,   --listen=<port>         Port to listen on (default 8080).`
<br>`-a <port>,   --listenapi=<port>      Port to listen on [API] (default 8081).`
<br>`-s <server>, --upstreamserver        Upstream proxy mode (server)`
<br>`-p <port>,   --upstreamport          Upstream proxy mode (port)`
<br>`-m <mode>,   --mode                  Proxy mode (default transparent)`
<br>`-h                                   Print help message.`
<br>
<br>FruityWifi: http://www.fruitywifi.com
<br>libmproxy:  https://mitmproxy.org/doc/scripting/libmproxy.html

#### Note: mitmproxy v0.15 or above is required


# FruityProxy and MITMf in upstream mode

<br>`./mitmf.py -i eth0 {+options}`
<br>`./fruityproxy.py -s 127.0.0.1 -p 10000`
<br>
<br>Then, redirect the traffic to port 8080 (FruityProxy default port).
<br>
<br>`Request <-> FruityProxy <-> MITMf <-> Response`
<br>
<br>
