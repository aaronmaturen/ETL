#!/usr/bin/python
#rm -rf /tmp/cis486logs && mkdir /tmp/cis486logs && python main.py && echo ">>> Log Files <<<" && cat /tmp/cis486logs/*.txt
#version two
#aaron maturen
#empty fields are "" not None
#didn't indent part of the for loop
#had to strip out \r along with \n from last field

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
		IsShadowed = False
		loadOrder = 0

gStrDirPath = '/tmp/cis486'
gStrLogPath = '/tmp/cis486logs'
gStrLogFile = ''

gDictTables = {}
gDictFields = {}

#database stuffs
ip = '172.16.218.135'
port = '1433'
username = 'thedw'
password = 'thedw'
database = 'TheDW'
gStrConnection = 'mssql+pyodbc:///?odbc_connect={}'.format(urllib.quote_plus('Driver=/usr/local/lib/libtdsodbc.so;Server={};Port={};TDS_Version=8.0;uid={};pwd={};Database={};'.format(ip,port,username,password,database)))

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
		strSQLCmd = "SELECT * FROM [TABLES_TABLE] WHERE [TABLE_NAME] = '" + strDWTableName + "'"
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
		strSQLCmd = "SELECT * FROM [EXTRACT_FILE_TRANSLATION_TABLE] WHERE [Subsidiary_Number] = '" + gStrFilenameCompanyCode + "' AND [LEGACY_FIELDNAME] = '" + strLegacyName + "'"
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
			aNewField.businessRules = {}
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
	logWrite(vbCrLf + "...Successfully completed header translation" + vbCrLf)
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
	
	strSQLCmd = "INSERT INTO [IMPORT_TABLE](Import_TUID, Filename, Import_Datetime, Subsidiary_Number) VALUES ('"+strImportTUID+"','"+strFileName+"','"+strftime("%m/%d/%Y", localtime())+"','"+gStrFilenameCompanyCode+"')"
	
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
	
		strSQLCmd = "SELECT count(1) FROM ["+strTableName+"] " + strWhereClause

		try:
			aDataReader = aConn.execute(strSQLCmd)
			if aDataReader.fetchone()[0]	> 0:
				logWrite(vbCrLf + "Update" + vbCrLf)
				#performUpdate(aTable,varDataFields,strWhereClause,strImportTUID)
			else:
				logWrite(vbCrLf + "Insert" + vbCrLf)
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
	logWrite("performInsert")
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
			strDataList += varDataFields[aTable.fields[aFieldName].ordinalPositionInExtractFile].rstrip('\n').rstrip('\r') + "', '"
	
	strFieldList += "Import_TUID"
	
	strSQLCmd = "INSERT INTO ["+aTable.TableName+"] (" + strFieldList + ") VALUES (" + strDataList + strImportTUID + "')"
	
	try:
		aConn.connect()
	except Exception, e:
		logWrite("Could not connect to aConn in performInsert" + vbCrLf)
		logWrite(str(e) + vbCrLf)
		aConn.close()
	
	try:
	#	pass
		logWrite(strSQLCmd)
		aConn.execute(strSQLCmd)
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

strImportTUID = ''
intFileCounter = 0
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
				logWrite("-"*80 + vbCrLf)
				f=open(subdir+"/"+strFilename, 'r')
				logWrite("Processing file: " + strFilename + vbCrLf)
				if not translateHeader(strFilename):
					logWrite("*** ETL ERROR ***")
					logWrite("*** Skipping this input file: " + strFilename)
				else:
					strImportTUID = generateImportTUID(strFilename, intFileCounter, DTProcessingDateTime)
					lines=f.readlines()
					for line in lines[1:]:
						processData(line.split('\t'), strImportTUID)
						pass
				f.close()
				intFileCounter += 1
		
		printOutInsertNames()
	logWrite(vbCrLf + '-'*80 + vbCrLf)
	logWrite("ETL Completed on " + strftime("%c", localtime()) + vbCrLf)