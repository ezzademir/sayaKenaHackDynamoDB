#!/bin/bash
# Project:  sayaKenaHack.com
# 
# file:     functions.sh
# function: Common Functions for Shell Scripts
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

FUNCTIONSFILEMESSAGE="INFO: Functions file loaded" #message to load to prove functions.sh was loaded correctly

DATADIR="../Data"
DATAZIP="../Data.tar.gz"
DATAENC="../Data.tar.gz.enc"
LOADCRIPT="../LoadDynamo.py"
UPDATETABLESCRIPT="../UpdateTable.py"
DEFAULTENDPOINT="https://dynamodb.ap-southeast-1.amazonaws.com"


#---------------------------------------------------------------------------------------
# delete file / dir if exist
#---------------------------------------------------------------------------------------
function delFile {
if [ -f $1 ]; then
	echo "WARNING: Found old $1--deleting to prevent conflicts"
	rm $1
else
	echo "GOOD: No previous versions of $1 detected"
fi
}

function delDir {
if [ -d $1 ]; then
	echo "WARNING: Found old $1--deleting to prevent conflicts"
	rm -r $1
else
	echo "GOOD: No previous versions of $1 detected"
fi
}
