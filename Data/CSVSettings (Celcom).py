import re

################################################################
#Section 0: API Version
pwnVersion = "1.1"

################################################################
#Section 1: CSV Variables

#csv file name
csv_file_name = "../Data/CelcomPostpaid.csv"

#Header Row of CSV File
header_row =  ['NAME','ICNUM','ADDRESS', \
               'BLANK1','BLANK2','BLANK3', \
               'MOBILE_NUMBER','BLANK4','BLANK5', \
               'BLANK6','BLANK7','BLANK8', \
               'BLANK9','BLANK10']

#Which column is the ic-num
ic_num_col = "ICNUM"

delimiter = ","

noHeader = True #TRUE = no header.

testing = True

################################################################
#Section 2: Breach Variables

pwnTitle = "myTelcoBreach2017"
pwnName = "Malaysian Telco Breach 2017"
subName = "Celcom"


#Custom Functions#############################################
def getPwn(row, counter, csvFileName):

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
                   "sourceFile" : csvFileName, \
                   "rowID" : str(counter), \
                   "version": pwnVersion }

            return pwn

    except TypeError:
        return None
    

def getUserData(row):

    if row['MOBILE_NUMBER'] :
        tel = row['MOBILE_NUMBER']
        if tel[:1] == "0":
            userData = ( tel[:3] + "*" * ( len(tel) - 5) + tel[-2:] )
            userDataDescription = "Phone Number"
        else:
            userData = ( "0" + tel[:2] + "*" * ( len(tel) - 4) + tel[-2:] )
            userDataDescription = "Phone Number"
    else :
        userData = "n.a"
        userDataDescription = "n.a"
    pwnID = pwnTitle + subName + userData
    return [userData,userDataDescription,pwnID]

def getDataClasses(row):
	
    DataClasses = ["IC Number"]

    if row['MOBILE_NUMBER'] :
        DataClasses.append("Mobile Number")

    if row['ADDRESS']:
        DataClasses.append("Address")
        
    return DataClasses


