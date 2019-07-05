#!/bin/bash

# VERY BASIC Script to set Ardupilot SITL simulation in Ubuntu
#
# Tested on version LTS 18.10 on 2019-06-18 | NOT SUPPORTED by Dev team
#
# Full documentation on http://ardupilot.org/dev/docs/setting-up-sitl-on-linux.html#setting-up-sitl-on-linux


# Updating until this date -----------------------------------------------
sudo apt-get update -y
sudo apt-get upgrade -y

# Creates a folder to organize stuff -------------------------------------
cd ..

# Downloads full Ardupilot repository ------------------------------------
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive

# Reuses Build environment to install Ubuntu and Pythonpackages ----------
./Tools/environment_install/install-prereqs-ubuntu.sh 

# Install mavproxy
pip install --upgrade pymavlink MAVProxy --user

# Fixing small stuff -----------------------------------------------------
echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
source ~/.bashrc

# Adding sites to default locations
echo "AbraDF=-15.839650568136552,-47.92712785889222,1042,30" >> ./Tools/autotest/locations.txt

# Running ----------------------------------------------------------------
cd ArduCopter/
../Tools/autotest/sim_vehicle.py -L AbraDF --console --map

# Hint/Tip to reuse ------------------------------------------------------
echo " "
echo " "
echo " To run the simulator again: "
echo " cd ardupilot/ArduCopter/"
echo " ../Tools/autotest/sim_vehicle.py --console --map"









