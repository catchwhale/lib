import sys
import os
sys.path.append('/etc/lib')

dir = os.getcwd()
dir = dir.strip()
lib = '/etc/lib'

import json
import gspread #sudo pip install gspread
from multiprocessing import Pool
import re
import time
import codecs
import stat
os.chdir('/etc/lib/')
from oauth2client.client import SignedJwtAssertionCredentials #sudo pip install python-gflags oauth2client
os.chdir(dir)
# Remove file
def remove_file(filename):
	if os.path.exists(filename):
		os.remove(filename)
	else:
		print filename, 'does not exists.'
# Create a file 
def create_file(filename):
	os.chdir(lib)
	return open(filename, 'w')
	os.chdir(dir)
# Write file into local directory
def write_append(filename, word):
	os.chdir(lib)
	with open(filename, "a") as myfile:
	    myfile.write(word + '\n')
	# myfile.close()
	os.chdir(dir)
# Read file into local directory and return the content
def read_file(filename):
	os.chdir(lib)
	data = open(filename, "r")
	return data.readlines()
	os.chdir(dir)
# Parse data and split ':' to return list
def return_list(data):
	lst = []
	for i in data:
		i = i.strip()
		if i:
			if re.search(':', i):
				i = i.split(':')
				i0 = i[0]
				i1 = i[-1]
				i1 = i1.strip()
				i = (i0, i1)
				lst.append(i)
	return lst


# Column i.e A1, B1, C1, A2..A3
def updateSheet_by_column(sheet, worksheetName, column, text):
	try:
		worksheet = sheet.worksheet(worksheetName)
		worksheet.update_acell(column, text)
	except:
		pass
# Row x to Col y
def updateSheet_x_y(sheet, worksheetName, row, col, text):
	try:
		worksheet = sheet.worksheet(worksheetName)
		worksheet.update_cell(row, col, text)
	except:
		pass
def updateSheet_x_y2(parameter):
	sheet, worksheetName, row, col, text = parameter
	try:
		worksheet = sheet.worksheet(worksheetName)
		worksheet.update_cell(row, col, text)
	except:
		pass
# Delete worksheet
# Not verified, need to configure permission access
def del_worksheet(sheet, worksheetName):
	sheet.del_worksheet(worksheetName)
# Add new worksheet
# tested
def add_worksheet(sheet, worksheetName, rows, cols):
	sheet.add_worksheet(worksheetName, rows, cols)

# Select worksheet by name
# test if found or not
# tested
def sel_wrksht_by_name(sheet, worksheetName):
	try: # make a try-catch to filter worksheet if not found
		worksheet = sheet.worksheet(worksheetName)
		return worksheet
	except:
		print 'Work sheet', worksheetName, 'not found.'
# Get list of worksheet name
# Tested
def get_all_worksheet_list(sheet):
	lst = sheet.worksheets() # resturn all class values of worksheet
	myL = []
	for i in lst:
		i=str(i) # convert to string
		i=i.split("'") # separate the data into single quote "'"
		wrksht_name = i[1] # Get the data at index 1
		if wrksht_name: # If not empty
			myL.append(wrksht_name) # Append worksheet name into list myL
	return myL
# Get cell value by Column ie. A1, B1, C1, A2, A3....
def get_cel_value_by_col(sheet, worksheetName,column):
	worksheet = sheet.worksheet(worksheetName)
	worksheet = worksheet.acell(column).value
	return worksheet # Return the data value
# Get cell value by Coordinates
# Tested
def get_cel_value_by_coord(sheet, worksheetName,column, row):
	worksheet = sheet.worksheet(worksheetName)
	worksheet = worksheet.cell(row, column).value
	return worksheet # Return the data value

#Get all values under column specified in variable number i.e headers 
# Tested
def get_column_data(sheet, worksheetName, number):
	worksheet = sheet.worksheet(worksheetName)
	worksheet = worksheet.row_values(number)
	if not worksheet[0]: # test if index zero is null
		worksheet = set(worksheet)
	return worksheet

# Get Permission from the G-Spreadsheet
# Tested
def access_sheet(key):
	json_key = json.load(open('API Project-4af8ab99186b.json'))
	sheet = ['https://spreadsheets.google.com/feeds']
	sheet = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], sheet)
	sheet = gspread.authorize(sheet)
	sheet = sheet.open_by_key(key)
	return sheet

# looking for an empty row to update the new data
def find_empty_row(sheet, worksheetName):
	cnt = 1
	while True:
		headers =  get_column_data(sheet, worksheetName, cnt)
		if len(headers) == 1:
			return cnt
			break
		cnt += 1
# def update_sheet(sheet, worksheetName, listWorksheet_val):
# def update_sheet(sheet, listWorksheet_val):
def update_sheet(parameter):
	# sheet, worksheetName, listWorksheet_val = parameter
	# delay, sheet, listWorksheet_val = parameter
	# time.sleep(delay)
	liquidate = []
	# listWorksheet_val = parameter
	sheet, listWorksheet_val = parameter
	# key = "1M3qsO6IkPoVFBHYkqVgDlC18KQmeP9RaU3TbGuFEqk0"
	# sheet = access_sheet(key)

	mySheet = listWorksheet_val['worksheet'] # Get the worksheet 'cPersonalDetails'
	# headers =  get_column_data(sheet, worksheetName, 1)
	headers =  get_column_data(sheet, mySheet, 1)
	x = find_empty_row(sheet, mySheet) # Find rows that are vacant/empty cells
	
	liquidate = read_file('record')
	try:
		liquidate = return_list(liquidate)
	except:
		pass
	tup = mySheet + ':' + str(x)
	tup_ = (mySheet, str(x))
	cnt = 0
	for i in liquidate:
		if i == tup_:
			cnt += 1
	tup = mySheet + ':' + str(x)
	write_append('record', tup)
	if cnt != 0:
		x += cnt
	y = 1 # initial column 1
	for i in headers: # iterate headers 
		text = listWorksheet_val[i] # write the value
		# print type(text)
		if re.search('str', str(type(text))) or re.search('unicode', str(type(text))): # if text type is string
			updateSheet_x_y(sheet, mySheet, x, y, text) #start to update at worksheet cPersonalDetails
		else:
			cnt = 0
			for z in text:
				newX = x + cnt
				cnt += 1
				updateSheet_x_y(sheet, mySheet, newX, y, z) #start to update at worksheet cPersonalDetails
		y += 1
def div_data(parameter):
	data = []
	data2 = []
	data3 = []
	cnt = 0
	for i in parameter:
		if cnt % 2 == 0:
			data2.append(i)
		elif cnt % 3 == 0:
			data3.append(i)
		else:
			data.append(i)
		cnt += 1
	return [ data, data2, data3 ]
def to(parameter):
	P = Pool(processes=8)
	sheet, data = parameter
	jobs = [(sheet, worksheet) for worksheet in data]
	P.map(update_sheet, jobs)
# Get current time at the server
# Return the current time: hr-min-sec, hr	
def mytime():
	from datetime import datetime
	getCurTime = datetime.now().strftime('%H:%M:%S')
	getCurTime = getCurTime.strip()
	mytime = getCurTime.split(':')
	return getCurTime, mytime[0] + ':' + mytime[1]
	# return getCurTime, mytime[0]
# Given the hr:min:sec then return hr:min
def getTime_w_o_sec(time):
	time = str(time)
	time = time.strip()
	time = time.split(':')
	time_sec = time[1]
	time = time[0]
	return time + ':' + time_sec
	# return time
# Given the hr:min then return hr
def getHr(time):
	time = str(time)
	time = time.strip()
	time = time.split(':')
	# time_sec = time[1]
	time = time[0]
	return time
# Get current Day at the server
def getDay():
	import datetime
	today = datetime.date.today()
	# today = today.strip()
	return today
# Get the current day and the expiration date
def calc_duration(number):
	import datetime
	today = getDay()
	duration = datetime.timedelta(days=number)
	END = today + duration
	return END

# Update Json file but not sure if this can be use now 
def write_json(filename, data):
	os.chdir(lib)
	import codecs
	with codecs.open(filename, 'a', 'utf8') as f:
		f.write(json.dumps(data, f, sort_keys = True, ensure_ascii=False))
		f.close()
	os.chdir(dir)
# Read Json file and return as list
def read_json(filename):
	os.chdir(lib)
	with open(filename) as json_file:
		json_data = json.load(json_file)
	return list(json_data)
	os.chdir(dir)
# Initial file and make it writable
def init_json(filename):
	os.chdir(lib)
	open(filename, 'w').close() 
	st = os.stat(filename)
	os.chmod(filename, st.st_mode | 0o111)
	os.chdir(dir)

# Reading JSON file and append/update attribute accordingly
def update_json(filename, attribute):
	# data={}
	try:
		with open(filename, "r") as jsonFile:
			data = json.load(jsonFile)
	except:
		data = {}
	len_ = str(len(data.keys()))
	data[len_] = attribute
	print data
	with open(filename, "w") as jsonFile:
		jsonFile.write(json.dumps(data))
# Reading JSON file and return keys and values accordingly
def get_json_key_val(filename):
	with open(filename, "r") as jsonFile:
		data = json.load(jsonFile)
	return data.keys(), data.values()


