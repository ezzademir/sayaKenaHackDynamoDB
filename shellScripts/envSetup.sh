#!/bin/bash
# Project:  sayaKenaHack.com
# 
# file:     envSetup.sh
# function: Download Dependencies for setting up environment
#
# Author: Keith Rozario <keith@keithrozario.com>
#
# This work is licensed under the
# Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit 
# http://creativecommons.org/licenses/by/4.0/ or 
# send a letter to 
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
#
# 

######### BEGIN INSTALLATION          ##########

apt-get update
apt-get install -y python3-pip
pip3 install boto3

######### END INSTALLATION           ###########
