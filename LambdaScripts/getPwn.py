import boto3
import json
import re
import datetime

from boto3.dynamodb.conditions import Key, Attr

now = datetime.datetime.now()
cutOff = datetime.datetime(2017, 11, 19, 15, 55 , 0, 0)
forumLink = "<a href=\"https://forum.lowyat.net/index.php?showtopic=4460339\">Click Here </a>"

pwn = [{"version": "1.1", "dataClasses": ["Agent ID", "Name", "Car Number Plate"], "subName": "MI6", "userData": forumLink}]


def get(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pwnTable')
    
    if now > cutOff:
        if "icNum" in event['queryStringParameters']:
            if event['queryStringParameters']['icNum'] == "007":
                return {'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*' },
                'body': json.dumps(pwn)}
            else:
                return {'statusCode': 451,
                'headers': {'Access-Control-Allow-Origin': '*' },
                'body': 'API ini tidak dapat diakses di Malaysia -- sebab SKMM'}
        else:
            return {'statusCode': 451,
            'headers': {'Access-Control-Allow-Origin': '*' },
            'body': 'API ini tidak dapat diakses di Malaysia -- sebab SKMM'}
    
    if "icNum" not in event['queryStringParameters']:
        result = ''
        statusCode = 400
    else:
        #result = event['queryStringParameters']['icNum']
        try:
            icNum = event['queryStringParameters']['icNum']
            icClean = (re.sub('[^A-Za-z0-9]+', '', icNum))
            icCleanUpper = icClean.upper()
            response = table.query( KeyConditionExpression=Key('icNum').eq(icCleanUpper),  \
                        ProjectionExpression="version, subName, userData, dataClasses, userDataDescription")
            
            if len(response['Items']) > 0:
                statusCode = 200
                result = json.dumps(response['Items'])
            else:
                statusCode = 404
                result = ''
            
        except:
            statusCode = 404
            result = ''
    
    return {'statusCode': statusCode,
            'headers': { 
            'Access-Control-Allow-Origin': '*'
            },
            'body': result}
