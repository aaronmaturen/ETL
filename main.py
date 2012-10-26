#!/usr/bin/python
#aaron maturen
#empty fields are "" not None

import os
import sys
from time import strftime, localtime
import pyodbc, sqlalchemy, urllib
import inspect
from itertools import count
import re

class clsField():
	def __init__(self):
		self.legacyName = ""
		self.DWName = ""
		self.ordinalPositionInExtractFile = None
		self.businessRules = []

class clsTable():
	def __init__(self):
		fields = {}
		tableName = ""
		Keys = ""
		isShadowed = False
		loadOrder = 0

class clsBusinessRule():
	def __init__(self):
		self.legacyValue = ''
		self.DWValue = ''

gStrDirPath = 'data'
gStrLogPath = 'logs'
gStrLogFile = ''

gDictTables = {}
gDictFields = {}

#database stuffs
ip = '127.0.0.1'
port = '3306'
username = 'root'
password = 'windows'
database = 'ETL'
gStrConnection = 'mysql://{}:{}@{}:{}/{}?charset=utf8'.format(username,password,ip,port,database)

#some fixes for keeping some VB stuffs
vbCrLf = "\r\n"
vbTab = '\t'

def createLogFile():
	global gStrLogFile
	if(not os.path.exists(gStrLogPath) or not os.path.isdir(gStrLogPath)):
		print("FATAL ERROR!")
		print("Could not access log directory: " + gStrLogPath + vbCrLf)
		sys.exit()
	else:
		gStrLogFile = gStrLogPath + "/" + strftime("%m%d%y%H%M%S", localtime()) + ".txt"
		print "Logfile: " + gStrLogFile
		f = open(gStrLogFile, 'a')
		f.write("ETL Started on " + strftime("%c", localtime()) + vbCrLf)
		f.close()

def logWrite(someText):
	f = open(gStrLogFile, 'a')
	f.write(someText)
	print someText,
	f.close()

def updateTablesAndFieldsArrays( strDWTableName, strDWFieldName):
	global gDictTables
	aTable = clsTable
	aConn = sqlalchemy.create_engine(gStrConnection)
	strSQLCmd = ""
	if strDWTableName not in gDictTables:
		#this means it's a new table and we have to initialize all the table info
		logWrite(vbCrLf + "Creating new table instance for '" + strDWTableName + "'..." + vbCrLf)
				
		aTable = clsTable()
		aTable.TableName = strDWTableName
		aTable.fields = {}
		try:
			aConn.connect()
		except Exception, e:
			logWrite(e)
			aConn.close()
		strSQLCmd = "SELECT * FROM `TABLES_TABLE` WHERE `TABLE_NAME` = '" + strDWTableName + "'"
		aDataReader = aConn.execute(strSQLCmd)
		
		#SQLALCHEMY Didn't want to play nice
		keys = aDataReader.keys()
		
		results = []
		for result in aDataReader:
			dictResults = {}
			for i in range(len(keys)):
				dictResults[keys[i]] = result[i]
			results.append(dictResults)
		if len(results)	> 0:
			for result in results:
				if result["Is_Shadowed"].upper() == 'Y':
					aTable.isShadowed = True
				else:
					aTable.isShadowed = False
				aTable.loadOrder = long(result["Load_Order"])
				aTable.keys = result["Keys"]
				gDictTables[strDWTableName] = aTable
		else:
			logWrite(vbCrLf + "Couldn't Find info on: " + strDWTableName + vbCrLf)
		try:
			del aConn
		except Exception, e:
			logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS")
			logWrite(str(e))
		logWrite("Using key(s): " + str(aTable.keys.encode('ascii').split('+'))+ " on " + strDWTableName + vbCrLf)
	else:
		#table exisits... just need to insert it
		aTable = gDictTables[strDWTableName]
	if strDWFieldName not in aTable.fields:
		aTable.fields[strDWFieldName] = gDictFields[strDWFieldName]
		logWrite("Added Field '" + strDWFieldName + "' to '" + strDWTableName + "' " + vbCrLf)

def translateHeader(strFilename):
	logWrite("Translating header of " + strFilename + vbCrLf)
	global gDictFields
	global gStrFilenameCompanyCode
	gStrFilenameCompanyCode = strFilename[4:7]
	
	strTextLine = ''
	varFileFields = ()
	blnSuccess = True
	aConn = sqlalchemy.create_engine(gStrConnection)
	
	strSQLCmd = ''
	aNewField = clsField()
	lngPosition = 0
	gsrReader = open(subdir+"/"+strFilename,"r")
	logWrite("Conversion of legacy fields in " + strFilename + " to DW field Names started... " + vbCrLf)
	try:
		strTextLine = gsrReader.readline().upper()
	except Exception, e:
		logWrite("***ERROR on opening data file***"+vbCrLf+"in translateHeader" + vbCrLf)
		logWrite(str(e))
	
	varFileFields = strTextLine.split()
	
	try:
		aConn = sqlalchemy.create_engine(gStrConnection)
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open()***"+vbCrLf+"in translateHeader" + vbCrLf)
		logWrite(str(e))
	
	lngPosition = 0
	for strLegacyName in varFileFields:
		strSQLCmd = "SELECT * FROM `EXTRACT_FILE_TRANSLATION_TABLE` WHERE `Subsidiary_Number` = '" + gStrFilenameCompanyCode + "' AND `LEGACY_FIELDNAME` = '" + strLegacyName + "'"
		try:
			aDataReader = aConn.execute(strSQLCmd)
		except Exception, e:
				logWrite(vbCrLf + vbCrLf + vbCrLf)
				logWrite("oops... could not execute query in " + sys._getframe().f_code.co_name + vbCrLf)
				logWrite("statement: " + strSQLCmd + vbCrLf)
				logWrite("error: " + str(e) + vbCrLf)

		aNewField = clsField()
		aNewField.legacyName = strLegacyName
		aNewField.ordinalPositionInExtractFile = lngPosition
		aNewField.DWName = None
		
		for result in aDataReader:
			if aNewField.DWName is None:
				aNewField.DWName = result[2]
			aNewField.businessRules = []
			gDictFields[result[2]] = aNewField
			updateTablesAndFieldsArrays(result[3],result[2])
		lngPosition += 1
	
	try:
		del aConn
	except Exception, e:
		logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS")
		logWrite(str(e))
	logWrite("Finished processing header of " + strFilename)
	return blnSuccess

def printOutInsertNames():
	strCommaSpace = ", "
	strNames = ''
	
	logWrite(vbCrLf + vbCrLf)
	logWrite("-------------------------------------------------------------------------------")
	logWrite(vbCrLf + "...Successfully completed processing files..." + vbCrLf)
	logWrite("-------------------------------------------------------------------------------")
	logWrite(vbCrLf + vbCrLf)
	logWrite("the following table entities were generated:" + vbCrLf)
	for aKey in gDictTables.keys():
		logWrite("Table: " + aKey + vbCrLf)
		logWrite("Keys: " + str(gDictTables[aKey].keys.encode('ascii').split('+')) + vbCrLf)
		logWrite("Fields: " + vbCrLf)
		strNames = ''
		for aKey2 in gDictTables[aKey].fields.keys():
			strNames += gDictFields[aKey2].DWName + strCommaSpace
		logWrite(strNames[0:-2] + vbCrLf + vbCrLf + vbCrLf)


def generateImportTUID(strFileName, intFileCounter, DTProcessingDateTime):
	aConn = sqlalchemy.create_engine(gStrConnection)
	strImportTUID = strftime("%Y%m%d%H%M%S", DTProcessingDateTime) + str(intFileCounter).zfill(4)
	
	#try to open connection to the database
	try:
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open()***"+vbCrLf+"in generateImportTUID" + vbCrLf)
		logWrite(str(e) + vbCrLf)
	
	strSQLCmd = "INSERT INTO `IMPORT_TABLE`(Import_TUID, Filename, Import_Datetime, Subsidiary_Number) VALUES ('"+strImportTUID+"','"+strFileName+"','"+strftime("%m/%d/%Y", localtime())+"','"+gStrFilenameCompanyCode+"')"
	
	try:
		aConn.execute(strSQLCmd)
		logWrite("Generated Import TUID: " + strImportTUID + vbCrLf)
		logWrite (vbCrLf + vbCrLf)
	except Exception, e:
		logWrite("Error while generating import TUID" + vbCrLf)
		logWrite("statement: " + strSQLCmd + vbCrLf)
		logWrite("description: " + str(e) + vbCrLf)
	
	try:
		del aConn
	except Exception, e:
		logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS")
		logWrite(str(e))
	return strImportTUID

def processData(varDataFields, strImportTUID):
	strTableName = ''
	strWhereClause = ''
	varTableKeys = ()
	lngLoop = 0
	aClsField = clsField()
	strSQLCmd = ''
	aConn = sqlalchemy.create_engine(gStrConnection)
	dictTablesInOrder = {}
	aKey = ''
	aTable = clsTable()
	
	try:
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open() in processData ***" + vbCrLf)
		logWrite(str(e) + vbCrLf)
		
	for aTable in gDictTables.values():
		dictTablesInOrder[aTable.loadOrder] = aTable.TableName
	
	for aKey in dictTablesInOrder.values():
		aTable = gDictTables[aKey]
		strTableName = aTable.TableName
		
		if aTable.keys is not u'':
			varTableKeys = aTable.keys.split("+")
			strWhereClause = "WHERE "
			for key in varTableKeys:
				strWhereClause += key + " = '"
				try:
					aField = gDictFields[key]
				except Exception, e:
					logWrite(vbCrLf + vbCrLf)
					logWrite("**********************************************")
					logWrite(vbCrLf + "FATAL ERROR:")
					logWrite(vbCrLf + "Column not found in data file: " + str(e))
					logWrite(vbCrLf + "Terminating Import at: " + strftime("%c", localtime()) + vbCrLf)
					logWrite("**********************************************")
					logWrite(vbCrLf + vbCrLf)
					sys.exit()
				strWhereClause += varDataFields[aField.ordinalPositionInExtractFile] + "' AND "
			strWhereClause = strWhereClause[:-4]
	
		strSQLCmd = "SELECT count(1) FROM `"+strTableName+"` " + strWhereClause

		try:
			aDataReader = aConn.execute(strSQLCmd)
			if aDataReader.fetchone()[0]	> 0:
				#logWrite(vbCrLf + "Update" + vbCrLf)
				performUpdate(aTable,varDataFields,strWhereClause,strImportTUID)
			else:
				#logWrite(vbCrLf + "Insert" + vbCrLf)
				performInsert(aTable,varDataFields,strWhereClause,strImportTUID)
	
		except Exception, e:
			logWrite(vbCrLf + vbCrLf + vbCrLf)
			logWrite("oops... could not execute query in " + sys._getframe().f_code.co_name + vbCrLf)
			logWrite("statement: " + strSQLCmd + vbCrLf)
			logWrite("error: " + str(e) + vbCrLf)
	
	try:
		del aConn
	except Exception, e:
		logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS" + vbCrLf)
		logWrite(str(e))


def performInsert(aTable, varDataFields, strWhereClause, strImportTUID):
	#logWrite("performInsert")
	try:
		aConn = sqlalchemy.create_engine(gStrConnection)
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open()***"+vbCrLf+"in performInsert" + vbCrLf)
		logWrite(str(e) + vbCrLf)
	
	strFieldList = ""
	strDataList = "'"


	for aFieldName in aTable.fields.keys():
		strFieldList += aFieldName + ","
		if varDataFields[aTable.fields[aFieldName].ordinalPositionInExtractFile] is "":
			strDataList = strDataList[0:-1] + "NULL, '"
		else:
			strDataList += varDataFields[aTable.fields[aFieldName].ordinalPositionInExtractFile].rstrip('\n').rstrip('\r').replace("'", "''") + "', '"
	
	strFieldList += "Import_TUID"
	
	strSQLCmd = "INSERT INTO `"+aTable.TableName+"` (" + strFieldList + ") VALUES (" + strDataList + strImportTUID + "')"
	
	try:
		aConn.connect()
	except Exception, e:
		logWrite("Could not connect to aConn in performInsert" + vbCrLf)
		logWrite(str(e) + vbCrLf)
		aConn.close()
	
	try:
		aConn.execute(strSQLCmd)
		logWrite("Generated Update Command: " + strSQLCmd + vbCrLf + vbCrLf)
	except Exception, e:
		logWrite(vbCrLf + vbCrLf + vbCrLf)
		logWrite("oops... could not execute insert query in performInsert" + vbCrLf)
		logWrite("statement: " + strSQLCmd + vbCrLf)
		logWrite("error: " + "".join(re.findall("\[FreeTDS\]\[SQL Server\][^0-9]+\([0-9]+\)",str(e))) + vbCrLf)
	
	try:
		#aConn.close()
		del aConn
	except Exception, e:
		logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS")
		logWrite(str(e))

def performUpdate(aTable, varDataFields,strWhereClause,strImportTUID):
	#logWrite("performUpdate")
	try:
		aConn = sqlalchemy.create_engine(gStrConnection)
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open()***"+vbCrLf+"in performInsert" + vbCrLf)
		logWrite(str(e) + vbCrLf)
	
	strDataList = ""
	if aTable.isShadowed:
		shadowRecord(aTable.TableName, strWhereClause)
	
	strSQLCmd = "UPDATE `" + aTable.TableName + "` SET "
	for aFieldName in aTable.fields.keys():
		strDataList += aFieldName
		if varDataFields[aTable.fields[aFieldName].ordinalPositionInExtractFile] is "":
			strDataList += " = NULL,"
		else:
			strDataList += " = '" + varDataFields[aTable.fields[aFieldName].ordinalPositionInExtractFile].rstrip('\n').rstrip('\r').replace("'", "''") + "',"	
	
	strDataList += "Import_TUID = '" + strImportTUID + "' "
	
	#mash it all together
	strSQLCmd += strDataList + strWhereClause
	
	try:
		aConn.execute(strSQLCmd)
		logWrite("Generated Update Command: " + strSQLCmd + vbCrLf + vbCrLf)
	except Exception, e:
		logWrite(vbCrLf + vbCrLf + vbCrLf)
		logWrite("oops... could not execute query in " + sys._getframe().f_code.co_name + vbCrLf)
		logWrite("statement: " + strSQLCmd + vbCrLf)
		logWrite("error: " + str(e) + vbCrLf)
	
def shadowRecord(strTableName,strWhereClause):
	strShadowsTableName = strTableName[:strTableName.index("_Table")]+"_Shadows_Table"
	try:
		aConn = sqlalchemy.create_engine(gStrConnection)
		aConn.connect().execution_options(enable_rowcount=True)
	except Exception, e:
		logWrite("***ERROR on aConn.open()***"+vbCrLf+"in performInsert" + vbCrLf)
		logWrite(str(e) + vbCrLf)
		
	strSQLCmd = "INSERT INTO `" + strShadowsTableName + "` SELECT * FROM `" + strTableName + "` " + strWhereClause
	
	try:
		aConn.execute(strSQLCmd)
		#logWrite("Generated shadow Command: " + strSQLCmd + vbCrLf + vbCrLf)
	except Exception, e:
		logWrite(vbCrLf + vbCrLf + vbCrLf)
		logWrite("oops... could not execute query in " + sys._getframe().f_code.co_name + vbCrLf)
		logWrite("statement: " + strSQLCmd + vbCrLf)
		logWrite("error: " + str(e) + vbCrLf)
	
def loadBusinessRules():
	aConn = sqlalchemy.create_engine(gStrConnection)
	aBusinessRule = clsBusinessRule()
	Subsidiary_Number = 0
	DW_Fieldname = 1
	Legacy_Value = 2
	DW_Value = 3
	
	try:
		aConn.connect()
	except Exception, e:
		logWrite("Could not connect to aConn in loadBusinessRules" + vbCrLf)
		logWrite(str(e) + vbCrLf)
		aConn.close()
	
	logWrite("Beginning Business Rule Load for subsidiary " + gStrCompanyCode + "..." + vbCrLf)
	for aField in gDictFields:
		strSQLCmd = "SELECT * FROM `BUSINESS_RULES_TABLE` WHERE `SUBSIDIARY_NUMBER` = '" + gStrCompanyCode + "' AND `DW_FIELDNAME` = '" + gDictFields[aField].DWName + "'"
		
		try:
			#logWrite(strSQLCmd + vbCrLf)
			rows = aConn.execute(strSQLCmd)
			for row in rows:
				logWrite(str(row) + vbCrLf)
				aBusinessRule = clsBusinessRule()
				if (row[Legacy_Value] is 'Null'):
					aBusinessRule.legacyValue = ""
				else:
					aBusinessRule.legacyValue = row[Legacy_Value]
				
				aBusinessRule.DWValue = row[DW_Value]
				gDictFields[aField].businessRules.append(aBusinessRule)
		except Exception, e:
			logWrite(vbCrLf + vbCrLf + vbCrLf)
			logWrite("oops... could not select business rules in loadBusinessRules()" + vbCrLf)
			logWrite("statement: " + strSQLCmd + vbCrLf)
			logWrite("error: " + "".join(re.findall("\[FreeTDS\]\[SQL Server\][^0-9]+\([0-9]+\)",str(e))) + vbCrLf)

		#try:
		#	#aConn.close()
		#	del aConn
		#except Exception, e:
		#	logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS" + vbCrLf)
		#	logWrite(str(e) + vbCrLf + vbCrLf)
			
	logWrite("Business Rules Loading Complete" + vbCrLf)

def dispatchVerify(strTableAndField, strValueToVerify):
	TABLE_FIELD_SEPERATOR = "."
	blnResult = False
	strSQLCmd = ''
	strTableName = ''
	strFieldName = ''
	lngPos = strTableAndField.index(TABLE_FIELD_SEPERATOR)
	aConn = sqlalchemy.create_engine(gStrConnection)
		
	if lngPos < 0:
		#couldn't find TABLE_FIELD_SEPERATOR
		logWrite("Couldn't Parse VRFY Business Rule " + strTableAndField + vbCrLf)
	else:
		#logWrite("Attempting to apply VRFY Business Rule '" + strTableAndField + "'" + vbCrLf)
		strTableName = strTableAndField[:lngPos]
		strFieldName = strTableAndField[lngPos+1:]
		
		try:
			aConn.connect()
		except Exception, e:
			logWrite("Could not connect to aConn in dispatchVerify" + vbCrLf)
			logWrite(str(e) + vbCrLf)
			aConn.close()
			
		strSQLCmd = "SELECT * FROM `" + strTableName + "` WHERE `" + strFieldName + "` = '" + strValueToVerify.rstrip() + "'"
		try:
			aDataReader = aConn.execute(strSQLCmd)
		except Exception, e:
				logWrite(vbCrLf + vbCrLf + vbCrLf)
				logWrite("oops... could not execute query in " + sys._getframe().f_code.co_name + vbCrLf)
				logWrite("statement: " + strSQLCmd + vbCrLf)
				logWrite("error: " + str(e) + vbCrLf)
		
		try:
			for row in aDataReader:
				return True
				aDataReader.close()
		except Exception, e:
			pass
			
		logWrite(strSQLCmd + vbCrLf)
			
		try:
			#aConn.close()
			del aConn
		except Exception, e:
			logWrite("ETL ERRORS... COULD NOT CLOSE DB CONNECTIONS" + vbCrLf)
			logWrite(str(e) + vbCrLf + vbCrLf)

	return blnResult

def dispatchMap(strLegacyValue,strDWValue,strValue):
	if strValue == strLegacyValue:
		#logWrite("Attempting to map " + strLegacyValue + " to " + strDWValue + vbCrLf)
		return strDWValue
	return strValue

def dispatchTruncateLeft(size,strValueToTruncate):
	size = int(size)
	try:
		#logWrite("Attempting to truncate " + strValueToTruncate + " to " + strValueToTruncate[:size] + vbCrLf)
		return strValueToTruncate[:size]
	except Exception, e:
		logWrite("Unable to truncate " + strValueToTruncate + vbCrLf)
		return strValueToTruncate

def dispatchMask(strMask,strValueToShape):
	blnResult = False
	#logWrite("Attempting to Mask " + strValueToShape + " with the mask " + strMask)
	
	if(strValueToShape == ""):
		return True
	
	strPreFixed = ""
	strMask = strMask.lower()
	if(strMask == "mm/dd/yyyy"):
		#mask is a date
		try:
			if(strValueToShape == re.split('[0123]?/d[/\-.][0123]?/d[/\-.](/d{4}|/d{2})',strValueToShape)[0]):
				tempDate = re.split('[/\-.]',strValueToShape)
				if(len(tempDate[0]) == 1):
					tempDate[0] = '0' + tempDate[0]
				if(int(tempDate[0]) < 1):
					tempDate[0] = '01'
				if(len(tempDate[1]) == 1):
						tempDate[1] = '0' + tempDate[1]
				if(int(tempDate[1]) < 1):
					tempDate[1] = '01'
				if(len(tempDate[2]) == 2):
					#if the year would be in the future... assume its supposed to be in the 1900s
					if int(tempDate[2]) <= int(strftime("%y", localtime())):
						tempDate[2] = '20' + tempDate[2]
					else:
						tempDate[2] = '19' + tempDate[2]
				if(int(tempDate[2]) <= 1900):
					tempDate[2] = '1901'
				#logWrite(" results in: " + '/'.join(tempDate) + vbCrLf)
				return '/'.join(tempDate)
			
			else:
				logWrite("Attempting to Mask " + strValueToShape + " with the mask " + strMask)
				logWrite(" failed." + vbCrLf)
				return False
		except Exception, e:
			logWrite("The Attempt to Mask " + strValueToShape + " with the mask " + strMask)
			logWrite(" failed for subsidiary " + gStrCompanyCode + vbCrLf)
			logWrite(str(e) + vbCrLf + vbCrLf)
	else:
		#it's some other mask
		try:
			safeValue = strValueToShape
			onlyNumbers = ''.join(re.split('\D+',strValueToShape))
			numberMask = re.findall('.',strMask)
			strValueToShape = ""
			i = 0
			if(len(onlyNumbers) == len(''.join(re.split('\D+',strMask)))):
				for char in numberMask:
					if(not char.isdigit()):
						strValueToShape += char
					else:
						strValueToShape += onlyNumbers[i:i+1]
						i+=1
				#logWrite(" results in: " + strValueToShape + vbCrLf)
				return strValueToShape
		except Exception, e:
			logWrite("The Attempt to Mask " + strValueToShape + " with the mask " + strMask)
			logWrite(" failed for subsidiary " + gStrCompanyCode + vbCrLf)
			logWrite(str(e) + vbCrLf + vbCrLf)
	logWrite("Attempting to Mask " + strValueToShape + " with the mask " + strMask)
	logWrite(" failed." + vbCrLf)
	return False

def appliedBusinessRules(varDataFields):
	INTRULE_VERB_LENGTH = 4
	INTRULE_DATA_AFTER_VERB = 5
	strValue = ''
	blnResult = True
	
	for aField in gDictFields:
		for aRule in gDictFields[aField].businessRules:
			method = aRule.DWValue.upper()[:INTRULE_VERB_LENGTH]
			if(method == "VRFY"):
				strValue = varDataFields[gDictFields[aField].ordinalPositionInExtractFile]
				if not dispatchVerify(aRule.DWValue[INTRULE_DATA_AFTER_VERB:],strValue):
					blnResult = False
					logWrite("Could not apply " + aRule.DWValue + " on " + strValue + vbCrLf)
				else:
					varDataFields[gDictFields[aField].ordinalPositionInExtractFile] = strValue
			elif(method == "TRUL"):
				strValue = varDataFields[gDictFields[aField].ordinalPositionInExtractFile]
				strValue = dispatchTruncateLeft(aRule.DWValue[INTRULE_DATA_AFTER_VERB:],strValue)
				varDataFields[gDictFields[aField].ordinalPositionInExtractFile] = strValue
			elif(method == "MASK"):
				strValue = varDataFields[gDictFields[aField].ordinalPositionInExtractFile]
				strValue = dispatchMask(aRule.DWValue[INTRULE_DATA_AFTER_VERB:],strValue)
				if strValue:
					varDataFields[gDictFields[aField].ordinalPositionInExtractFile] = strValue
				else:
					blnResult = False
			else:
				strValue = varDataFields[gDictFields[aField].ordinalPositionInExtractFile]
				strValue = dispatchMap(aRule.legacyValue,aRule.DWValue,strValue)
				varDataFields[gDictFields[aField].ordinalPositionInExtractFile] = strValue

	return blnResult
	
strImportTUID = ''
intFileCounter = 0
recordCounter = []
DTProcessingDateTime = localtime()

createLogFile()
if(not os.path.exists(gStrDirPath) or not os.path.isdir(gStrDirPath)):
	logWrite("Could not access extract files directory: " + gStrDirPath + vbCrLf)
	logWrite(vbCrLf + vbCrLf)
else:
	#Files to Process?
	if(len(os.walk(gStrDirPath).next()[2]) < 1):
		logWrite("No Files to Process\r\n")
		logWrite("sad day")
	else:
		#this means we've got some work to do
		DTProcessingDateTime = localtime()
		for subdir, dirs, files in os.walk(gStrDirPath):
			for strFilename in files:
				logWrite(vbCrLf + vbCrLf + "-"*80 + vbCrLf)
				f=open(subdir+"/"+strFilename, 'r')
				logWrite("Processing file: " + strFilename + vbCrLf)
				gStrCompanyCode = strFilename[4:7]
				if not translateHeader(strFilename):
					logWrite("*** ETL ERROR ***")
					logWrite("*** Skipping this input file: " + strFilename)
				else:
					strImportTUID = generateImportTUID(strFilename, intFileCounter, DTProcessingDateTime)
					loadBusinessRules()
					lines=f.readlines()
					logWrite(vbCrLf + vbCrLf + "Processing file records in " + strFilename + "..." + vbCrLf)
					for line in lines[1:]:
						varDataFields = line.split('\t')
						if appliedBusinessRules(varDataFields):
							processData(varDataFields, strImportTUID)
				f.close()
				logWrite(vbCrLf + "*** Processed " + str(len(lines)) + " records in " + strFilename + " ***" + vbCrLf)
				recordCounter.append(len(lines))
				intFileCounter += 1
		
		printOutInsertNames()
	logWrite(vbCrLf + '-'*80 + vbCrLf)
	logWrite("ETL Completed on " + strftime("%c", localtime()) + vbCrLf)
	logWrite(vbCrLf + "Processed " + str(sum(recordCounter)) + " records total.")