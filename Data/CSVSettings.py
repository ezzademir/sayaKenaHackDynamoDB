import re

################################################################
#Section 0: API Version
pwnVersion = "1.1"

################################################################
#Section 1: CSV Variables

#csv file name
csv_file_name = "../Data/UMobile.csv"

#Header Row of CSV File
header_row =  None

#Which column is the ic-num
ic_num_col = None #have to implement custom logic

delimiter = ","

noHeader = False #TRUE = no header.

testing = True

################################################################
#Section 2: Breach Variables

pwnTitle = "myTelcoBreach2017"
pwnName = "Malaysian Telco Breach 2017"
subName = "UMOBILE"


#Custom Functions#############################################
def getPwn(row, counter, csvFileName):

    try:

        if row["NRID"] :
            icRaw =  row['NRID']
        else:
            if row ['OTHER_ID'] :
                icRaw = row['OTHER_ID']
            else:
                return None
        

        #strip ic of all non-alpha and uppercase the remainder...
        icClean = (re.sub('[^A-Za-z0-9]+', '', icRaw))
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
                   "sourceFile" : csvFileName, \
                   "rowID" : str(counter), \
                   "version": pwnVersion }

            return pwn

    except TypeError:
        return None
    

def getUserData(row):

    if row['MSISDN'] :
        tel = row['MSISDN']
        userData = ( tel[:4] + "*" * ( len(tel) - 5) + tel[-2:] )
        userDataDescription = "Phone Number"
    else :
        userData = "n.a"
        userDataDescription = "n.a"
        
    pwnID = pwnTitle + subName + userData
    return [userData,userDataDescription,pwnID]

def getDataClasses(row):
	
    DataClasses = ["IC Number"]

    if row['NAME'] :
        DataClasses.append("Name")

    if row['ADDRESS_1'] :
        DataClasses.append("Address")

    if row['MSISDN'] :
        DataClasses.append("Mobile Number")

    if row['IMEI']:
        DataClasses.append("IMEI")

    if row['IMSI']:
        DataClasses.append("IMSI")

    if row['SIM_CARD']:
        DataClasses.append("SIM_CARD")
    
    return DataClasses


