import logging
import Data.CSVSettings as csvSpecific
from Data.CSVSettings import getPwn

##################################################################
#Section 1: CSV Variables
##################################################################

csv_file_name = csvSpecific.csv_file_name

if csvSpecific.noHeader :
	header_row = csvSpecific.header_row 
else:
	header_row = None

ic_num_col = csvSpecific.ic_num_col
delimiter = csvSpecific.delimiter

################################################################
#Section 2: Breach Variables

################################################################
#Section 3: DynamoDB Variables
#Production keys sprovided at runtime via command line args

aws_access_key_id = "Access Key"
aws_secret_access_key="secret key"
endpoint_url = "http://localhost:8000"

region_name = "ap-southeast-1"
table_name = "pwnTable"

keyHash = "icNum" #mixture of BreachID + key of the breach (e.g. phone number)
keyHashType = "S"
keyRange ="pwnID"
keyRangeType = "S"

################################################################
#Section 4: Testing Variables
#rownumbers to test against
testRowNumbers=[1,2,3,4,5,6,7,8,9,10,100,200]
#These only take effect is testing = True
testing = csvSpecific.testing
report_interval = 1000 #how many rows to report on
testing_limit = 10000 #when to stop loading rows in testing mode

################################################################
#Section 5: Logging variables

LogFileName = ('log.txt')
LogLevel = logging.INFO
LogFileMode = 'a'
LogMsgFormat = '%(asctime)s %(message)s'
LogDateFormat = '%m/%d/%Y %I:%M:%S %p'
