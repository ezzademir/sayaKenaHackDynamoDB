#!/bin/bash
# Project:  sayaKenaHack.com
# 
# file:     run.sh
# function: Load the data into DynamoDB
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
    --keyID) #Amazon KeyID for IAM account with access to DynamoDB
    KEYID="$2"
    shift # past argument
    ;;
    --keySecret)
    KEYSECRET="$2" #Secret Key
    shift # past argument
    ;;
    --endpoint)
    ENDPOINT="$2" #encryption/decryption key for zip file
    shift # past argument
    ;;
    --test) #Encryption key for the file
    TESTPARAMETER="$2"
    shift # past argument
    ;;
    *)
    # unknown option
    ;;
esac
shift # past argument or value
done

if [ -z "$KEYID" ] || [ -z "$KEYSECRET" ]; then #Check for keyID and Secret
    echo "ERROR: Please provide the keyID & Secretkey"
    echo "USAGE: ./run.sh -keyID <keyID> --keySecret <secretKey>"
    exit 0
else
    echo "GOOD: key ID and Secret provided"
fi

if [ -z "$ENDPOINT" ]; then #Check Endpoint
    ENDPOINT=https://dynamodb.ap-southeast-1.amazonaws.com
    echo "INFO: End point not provided, using $ENDPOINT"
else
    echo "INFO: Using $ENDPOINT as Endpoint"
fi

if [ -z "$TESTPARAMETER" ]; then #Check Endpoint
    echo "INFO: No test parameter supplied, using customConfig Settings"
else
    echo "INFO: --test supplied, we're going ALL the way!! "
    TEST="-t FALSE"
fi


######### COMMAND LINE PARAMETERS END ##########

######### WRITE TO TABLE             ###########

#python3 $UPDATETABLESCRIPT -k $KEYID -s $KEYSECRET -e $ENDPOINT -w 800 -t pwnTable

for FILENAME in $DATADIR/*.csv;
    do echo "INFO: Extracting File $FILENAME"
    echo "Executing Load"
    python3 $LOADCRIPT -f $FILENAME -k $KEYID -s $KEYSECRET -e $ENDPOINT $TEST;
done

######### CLEAN UP                   ###########

#python3 $UPDATETABLESCRIPT -k $KEYID -s $KEYSECRET -e $ENDPOINT -t pwnTable

#rm -r $DATADIR

######### END                       ###########

