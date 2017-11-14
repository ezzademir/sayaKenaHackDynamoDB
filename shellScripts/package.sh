#!/bin/bash
# Project:  sayaKenaHack.com
# 
# file:     Package.sh
# function: Make the Package (zip and encrypt the /Data folder)
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

#-------------------------------------------------------------------------
# Check if seetings and functions file exist
#-------------------------------------------------------------------------
FUNCTIONSFILE=functions.sh
if [ -f $FUNCTIONSFILE ]; then
	echo "INFO: Loading $FUNCTIONSFILE"
	source $FUNCTIONSFILE #file exist, load variables
	echo $FUNCTIONSFILEMESSAGE
else 
	echo "ERROR: Unable to find $FUNCTIONSFILE, please run setup.sh for first time"
    	exit 0
fi

######### COMMAND LINE PARAMETERS BEGIN #########

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    --enckey) #Encryption key for the file
    ENCKEY="$2"
    shift # past argument
    ;;
    *)
    # unknown option
    ;;
esac
shift # past argument or value
done

######### COMMAND LINE PARAMETERS END #########

######### UNPACKAGE THE APP           #########

if [ -z "$ENCKEY" ]; then #Check for Encryption Key
    echo "ERROR: Please provide an encryption key"
    echo "USAGE: ./run.sh --enckey <encryptionKey>"
    exit 0
else
    echo "GOOD: encryption key provided"
fi

if [ -d $DATADIR ]; then
    tar -zcf $DATAZIP $DATADIR
    echo "Encrypting File"
    openssl enc -aes-256-cbc -in $DATAZIP -out $DATAENC -k $ENCKEY
    rm $DATAZIP
    echo "Done"
else
    echo "BAD: $DATADIR not found -- exiting"
    exit 0
fi

######### UNPACKAGE THE APP           #########





