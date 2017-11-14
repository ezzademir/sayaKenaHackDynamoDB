import re
################################################################
#Section 0: API Version
pwnVersion = "1.0"

################################################################
#Section 1: CSV Variables

#csv file name
csv_file_name = "Data/pre_list_5.csv"

#Header Row of CSV File
header_row =  ["type","customer_name","billing_address1","billing_address2", \
               "billing_address3","billing_address4","billing_zip","billing_city", \
               "billing_state","msisdn","sim","imsi",\
               "handset_model","served_imei","ic"]

#Which column is the ic-num
ic_num_col = "ic"

delimiter = ","

testing = False

################################################################
#Section 2: Breach Variables

pwnTitle = "myTelcoBreach2017"
pwnName = "Malaysian Telco Breach 2017"
subName = "Maxis Prepaid"


#Test entries to read after insertion
test_ICs = ["881024115244","510407035089"]


#Custom Functions#############################################
def getPwn(row):

    #strip ic of all non-alpha and uppercase the remainder...
    icClean = (re.sub('[^A-Za-z0-9]+', '', row[ic_num_col]))
    icCleanUpper = icClean.upper()

    if not icCleanUpper:
        return None

    else:
        userDataArray = getUserData(row)
        dataClasses = getDataClasses(row)
        userData = userDataArray[0]
        userDataDescription = userDataArray[1]
        pwnID = userDataArray[2]
                
        pwn = {"icNum" : icCleanUpper, \
               "pwnID" : pwnID, 
               "name": pwnName, \
               "subName": subName, \
               "dataClasses" : dataClasses, \
               "userData" : userData, \
               "userDataDescription": userDataDescription, \
               "version": pwnVersion }

        return pwn

def getUserData(row):
    tel = row['msisdn']

    sampleData = ( tel[:4] + "*" * ( len(tel) - 6) + tel[-2:] )
    sampleDataDescription = "Phone Number"
    pwnID = pwnTitle + subName + sampleData
    
    return [sampleData,sampleDataDescription,pwnID]

def getDataClasses(row):

    DataClasses = ["IC Number"]

    if row['customer_name'] :
        DataClasses.append("Name")

    if row['billing_address1']:
        DataClasses.append("Billing Address")
        
    if row['imsi']:
        DataClasses.append("IMSI")

            
    if row['served_imei']:
        DataClasses.append("IMEI")

    if row['sim']:
        DataClasses.append("SIM Number")


    if row['msisdn']:
        DataClasses.append("Mobile Number")
        
    return DataClasses


