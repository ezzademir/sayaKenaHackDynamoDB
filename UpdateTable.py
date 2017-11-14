from __future__ import print_function # Python 2/3 compatibility
import logging
import os
import boto3
import sys
import argparse
import time

from botocore.exceptions import ClientError

def update_table(dynamoClient,tableName,readCapacity,writeCapacity):

    try:
        response = dynamoClient.update_table(
                TableName=tableName,
                ProvisionedThroughput=
                {
                'WriteCapacityUnits': writeCapacity,
                'ReadCapacityUnits' : readCapacity
            })
    except ClientError:
        logger.info("WARNING: Unable to Update Table")
        return 0

    logger.info("GOOD: Table " + response['TableDescription']['TableName'] + " updated")
    logger.info("INFO: Table info -- ")
    
        
def table_exist(dynamoClient,tablename):
    response = dynamoClient.list_tables()
      
    if tableName in response['TableNames']:
        return True
    else:
        return False

def get_table_data(dynamoClient,table_name):
    response = dynamoClient.describe_table( TableName=table_name )
    logger.info("Read  Units: " + str(response['Table']['ProvisionedThroughput']['ReadCapacityUnits']))
    logger.info("Write Units: " + str(response['Table']['ProvisionedThroughput']['WriteCapacityUnits']))

def get_read_units(dynamoClient,table_name):
    response = dynamoClient.describe_table( TableName=table_name )
    return (response['Table']['ProvisionedThroughput']['ReadCapacityUnits'])
    
########################################################################################################################
#     MAIN                                                                                                             #
########################################################################################################################

if __name__ == "__main__":

    testing = False #set to True when testing

    LogFileName = ('log.txt')
    LogLevel = logging.INFO
    LogFileMode = 'a'
    LogMsgFormat = '%(asctime)s %(message)s'
    LogDateFormat = '%m/%d/%Y %I:%M:%S %p'

    #Logging setup
    logging.basicConfig(filename=LogFileName, filemode=LogFileMode, level=LogLevel, format=LogMsgFormat, datefmt=LogDateFormat)
    logger = logging.getLogger(__name__)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)


    #Table setup -- check if user supplied PROD data (test data is in customConfig.py)
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-k", "--aws_keyID", help= "AWS Access Key, must have sufficient IAM privilege", \
                    required = True)
    parser.add_argument("-s", "--aws_secret", help= "AWS Secret Key", \
                    required = True)
    parser.add_argument("-e", "--aws_endpoint", help= "dynamoDB endpoint", \
                    required = False,  default = "https://dynamodb.ap-southeast-1.amazonaws.com")
    parser.add_argument("-g", "--aws_region", help= "AWS region", \
                    required = False,  default = "ap-southeast-1")
    parser.add_argument("-t", "--aws_tablename", help= "dynamoDB tablename", \
                    required = True)
    parser.add_argument("-w", "--aws_writecapacityunits", help= "provisioned write units", \
                    required = False, default = 1)

    args = parser.parse_args()

    #Table setup
    dynamodb = boto3.resource('dynamodb', region_name=args.aws_region,\
			      endpoint_url=args.aws_endpoint, \
    			      aws_access_key_id=args.aws_keyID,\
                              aws_secret_access_key=args.aws_secret)

    tableName = args.aws_tablename
    dynamoClient = dynamodb.meta.client

    if args.aws_writecapacityunits is None:
        writeCapacityUnits = 1
    else:
        writeCapacityUnits = int(args.aws_writecapacityunits)

    if not table_exist(dynamoClient,args.aws_tablename):
        print ("Exiting, table not found")
        exit

    currentReadUnits = get_read_units(dynamoClient,args.aws_tablename)

    logger.info("BEFORE WRITE: --")
    get_table_data(dynamoClient,args.aws_tablename)
    update_table(dynamoClient,args.aws_tablename,currentReadUnits,writeCapacityUnits)
    time.sleep(10)
    logger.info("\nAFTER WRITE: --")
    get_table_data(dynamoClient,args.aws_tablename)

