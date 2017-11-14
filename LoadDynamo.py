from __future__ import print_function # Python 2/3 compatibility

import csv
import logging
import json
import decimal
import argparse
import time 

#Custom Scripts
import customConfig

#Boto3 imports
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


########################################################################################################################
#     Helper Classes                                                                                                   #
########################################################################################################################

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


########################################################################################################################
#     Writing data to DB                                                                                               #
########################################################################################################################

def read_rows_from_table(icNum,table):
    response = table.query( KeyConditionExpression=Key('icNum').eq(icNum) )

    elementData = []
    
    for element in response['Items']:
        elementData.append(element)

    return elementData

def get_table_data(dynamoClient,table_name):
    response = dynamoClient.describe_table( TableName=table_name )
    
    logger.info("Name: " + response['Table']['TableName'])
    logger.info("RowCount: " + str(response['Table']['ItemCount']))
    logger.info("*Size: " + str(response['Table']['TableSizeBytes']))
    logger.info("CreationDate: " + str(response['Table']['CreationDateTime']))
    logger.info("*Size is updated every 6 hours, might not be reflective of real-time data")
    logger.info("CreationDate: " + str(response['Table']['KeySchema']))
    

########################################################################################################################
#     MAIN                                                                                                             #
########################################################################################################################

if __name__ == "__main__":

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

    #Table setup -- check if user supplied PROD data (test data is in customConfig.py)
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-k", "--aws_keyID", help= "AWS Access Key, must have sufficient IAM privilege", \
                    required = False, default = customConfig.aws_secret_access_key)
    parser.add_argument("-s", "--aws_secret", help= "AWS Secret Key", \
                    required = False, default = customConfig.aws_secret_access_key)
    parser.add_argument("-e", "--aws_endpoint", help= "dynamoDB endpoint", \
                    required = False)
    parser.add_argument("-f", "--filename", help= "filename", \
                    required = False)
    parser.add_argument("-n", "--startNum", help= "Row to start at", \
                    required = False)
    parser.add_argument("-t", "--test", help= "Testing Configuration, set to false for full run", \
                    required = False)

    args = parser.parse_args()

    #Take either command line arguments or from customConfig
    if args.filename is None:
        csvFileName = customConfig.csv_file_name
    else:
        csvFileName = args.filename

    if args.test is None:
        testingMode = customConfig.testing
    else:
        testingMode = False #Production

    if args.startNum is None:
        startNum = 0
    else:
        startNum = int(args.startNum)
    
    if args.aws_keyID is None or args.aws_secret is None or args.aws_endpoint is None:
        aws_keyID = customConfig.aws_access_key_id
        aws_secret = customConfig.aws_secret_access_key
        aws_endpoint = customConfig.endpoint_url
    else:
        aws_keyID = args.aws_keyID
        aws_secret = args.aws_secret
        aws_endpoint = args.aws_endpoint
   
    #Setup dynamodb table values        
    dynamodb = boto3.resource('dynamodb', region_name=customConfig.region_name,\
			      endpoint_url=aws_endpoint, \
    			      aws_access_key_id=aws_keyID,\
                              aws_secret_access_key= aws_secret)
    dynamoClient = dynamodb.meta.client
    table = dynamodb.Table(customConfig.table_name)

    #Open CSV File to read
    logger.info("State of table BEFORE write")
    get_table_data(dynamoClient,customConfig.table_name)
    logger.info(csvFileName + ": Loading File")

    with open(csvFileName, 'r', newline='', errors='ignore', encoding="utf8") as csvfile:

        readerDict = csv.DictReader(csvfile, fieldnames=customConfig.header_row , delimiter=customConfig.delimiter)
        counter = 0
        interval = 0
        testICs = {}

        with table.batch_writer(overwrite_by_pkeys=['icNum', 'pwnID']) as batch:
            for row in readerDict:
                counter += 1
                                
                if (counter > startNum or startNum == 0) :
                    pwn = customConfig.getPwn(row, counter, csvFileName)

                    if testingMode and counter > customConfig.testing_limit:
                        break      
                    
                    if pwn is not None:
                        batch.put_item(Item=pwn)
                        if counter in customConfig.testRowNumbers:
                            if pwn['userData']:
                                testICs[pwn['icNum']] = pwn['userData']
                    
                    interval += 1
                    if interval >= customConfig.report_interval:
                        logger.info("FILE Row: " + str(counter) + " written to batch-put")
                        interval = 0
                    
    logger.info("\n\nTotal rows processes: " + str(counter-1))
    logger.info("State of table AFTER write")
    get_table_data(dynamoClient,customConfig.table_name)
    logger.info(csvFileName + ": Job Complete")
    logger.info("\n\n#########################\nBEGIN TESTING")

    for record in testICs:
        #checking icNums
        rows = read_rows_from_table(record,table)

        for row in rows:
                
            if testICs[record] in row['userData']:
                logger.info("PASS: " + record + " \t " + testICs[record] + "," + row['subName'] + "," + str(row['dataClasses']))
            else:
                logger.info("MISS: " + record + " \t " + testICs[record] + " \t " + row['pwnID'])
    logger.info("Test Complete")
        
    
    
