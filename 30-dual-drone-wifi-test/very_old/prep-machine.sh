#!/bin/bash

cd 

sudo apt-get update

# generic & handy
sudo apt-get install -y nano htop vim code python3-pip python3-venv 
sudo pip3 install Flask

# pymavlink w/ python3 
sudo apt-get install -y gcc python3-dev libxml2-dev libxslt-dev
sudo apt-get install -y python3-numpy python3-pytest
sudo DISABLE_MAVNATIVE=True python -m pip install --upgrade pymavlink

# mavproxy w/ python3
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
pip3 install PyYAML mavproxy --user
echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc

# download mavlink-router
cd 

git clone --recurse-submodules https://github.com/mavlink-router/mavlink-router.git
sudo apt install -y python-future python3-future libtool autoconf


# set python3 as default
sudo rm /usr/bin/python
sudo ln -s /usr/bin/python3 /usr/bin/python

# ..
cd
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
git clone https://github.com/brunoolivieri/quadpi.git
