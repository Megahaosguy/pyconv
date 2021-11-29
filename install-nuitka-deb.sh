#!/bin/bash

CODENAME=`grep UBUNTU_CODENAME /etc/os-release | cut -d= -f2`
if [ -z "$CODENAME" ]
then
   CODENAME=`lsb_release -c -s`
fi;
wget -O - http://nuitka.net/deb/archive.key.gpg | apt-key add -
echo >/etc/apt/sources.list.d/nuitka.list "deb http://nuitka.net/deb/stable/$CODENAME $CODENAME main"
apt-get update
apt-get install nuitka
