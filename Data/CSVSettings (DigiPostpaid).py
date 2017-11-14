import re

################################################################
#Section 0: API Version
pwnVersion = "1.0"

################################################################
#Section 1: CSV Variables

#csv file name
csv_file_name = "../Data/Digi Postpaid.csv"

#Header Row of CSV File
header_row =  ['LN_SUBS_ID','MSISDN','SIM_SR_NUM','IMSI_ID',\
               'RT_PLN','IDENTITY_NUM','INVD_NAME',\
               'PHONE_BRAND','PHONE_MODEL','IMEI_NUM']

#Which column is the ic-num
ic_num_col = "IDENTITY_NUM"

delimiter = "\t" 

################################################################
#Section 2: Breach Variables

pwnTitle = "myTelcoBreach2017"
pwnName = "Malaysian Telco Breach 2017"
subName = "Digi Postpaid"


#Custom Functions#############################################
def getPwn(row):

    try:
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

    except TypeError:
        return None
    

def getUserData(row):
    tel = row['MSISDN']
    userData = ( tel[:4] + "*" * ( len(tel) - 6) + tel[-2:] )
    userDataDescription = "Phone Number"
    pwnID = pwnTitle + subName + userData
    return [userData,userDataDescription,pwnID]

def getDataClasses(row):
	
    DataClasses = ["IC Number","Mobile Number"]

    if row['INVD_NAME'] :
        DataClasses.append("Name")

    if row['IMSI_ID']:
        DataClasses.append("IMSI")

            
    if row['IMEI_NUM']:
        DataClasses.append("IMEI")

    if row['SIM_SR_NUM']:
        DataClasses.append("SIM Number")
        
    return DataClasses


