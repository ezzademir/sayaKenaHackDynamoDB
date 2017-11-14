from __future__ import print_function # Python 2/3 compatibility
import csv
import logging
import os
import customConfig
import boto3
import queryUser
import sys

from botocore.exceptions import ClientError

def delete_table(dynamoClient,tableName):

    response = dynamoClient.list_tables()
      
    if tableName in response['TableNames']:

        response = dynamoClient.describe_table( TableName=tableName )
        
        logger.info("WARNING: Table with name " + tableName + " found. Proceed to delete?")
        logger.info("Name: " + response['Table']['TableName'])
        logger.info("RowCount: " + str(response['Table']['ItemCount']))
        logger.info("CreationDate: " + str(response['Table']['CreationDateTime']))

        if queryUser.query_user("Are you Sure you want to delete?", "no"):
            if queryUser.query_user("Seriously this is a non-reversible thing?","no"):
                response = dynamoClient.delete_table(TableName=tableName)
                logger.info("INFO: Table " + response['TableDescription']['TableName'] + " with " +\
                            str(response['TableDescription']['ItemCount']) + " entries deleted")
            else:
                logger.info("Ending program")
                sys.exit()
        else:
            logger.info("Ending program")
            sys.exit()
    else:
        table_found = False
        logger.info("INFO: Table Not Found")

def create_table(dynamoClient,tableName,keyHash,keyHashType,keyRange,keyRangeType):

    response = dynamoClient.create_table(
        AttributeDefinitions=[
        {
            'AttributeName': keyHash,
            'AttributeType': keyHashType
            
        },
        {
            'AttributeName': keyRange,
            'AttributeType': keyRangeType
            
        }
        
    ],
        TableName=tableName,
        KeySchema=[
        {
            'AttributeName': keyHash,
            'KeyType': 'HASH'
        },
        {
            'AttributeName': keyRange,
            'KeyType': 'RANGE'
        }
    ],
        ProvisionedThroughput=
        {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10,
    })

    logger.info("GOOD: Table " + response['TableDescription']['TableName'] + " created on " +\
                str(response['TableDescription']['CreationDateTime']) + \
                "\n" + str(response['TableDescription']['KeySchema']))
        
def initialize_table(dynamoDB,tableName,keyHash,keyHashType,keyRange,keyRangeType):

    dynamoClient = dynamoDB.meta.client
    delete_table(dynamoClient,tableName)
    create_table(dynamoClient,tableName,keyHash,keyHashType,keyRange,keyRangeType)
    

########################################################################################################################
#     MAIN                                                                                                             #
########################################################################################################################

if __name__ == "__main__":

    testing = False #set to True when testing

    LogFileName = customConfig.LogFileName
    LogLevel = customConfig.LogLevel
    LogFileMode = customConfig.LogFileMode
    LogMsgFormat = customConfig.LogMsgFormat
    LogDateFormat = customConfig.LogDateFormat

    #Logging setup
    logging.basicConfig(filename=LogFileName, filemode=LogFileMode, level=customConfig.LogLevel, format=LogMsgFormat, datefmt=LogDateFormat)
    logger = logging.getLogger(__name__)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)

    #Table setup
    dynamodb = boto3.resource('dynamodb', region_name=customConfig.region_name,\
			      endpoint_url=customConfig.endpoint_url, \
    			      aws_access_key_id=customConfig.aws_access_key_id,\
                              aws_secret_access_key=customConfig.aws_secret_access_key)

    tableName = customConfig.table_name
    keyHash = customConfig.keyHash
    keyHashType = customConfig.keyHashType
    keyRange = customConfig.keyRange
    keyRangeType = customConfig.keyRangeType

    #WARNING: initDB will delete any old DB's
    initialize_table(dynamodb,tableName,keyHash,keyHashType,keyRange,keyRangeType) 
