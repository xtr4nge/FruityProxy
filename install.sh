#!/bin/bash

echo "installing FruityProxy..."

apt-get -y install python-pip

apt-get -y install build-essential python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev

pip install --upgrade six

#https://pypi.python.org/packages/source/u/urwid/urwid-1.3.0.tar.gz # if error, install urwid manually first. (http://urwid.org/)

pip install mitmproxy

echo "..DONE.."
exit
