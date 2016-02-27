#!/usr/bin/python

import sys
sys.path.append('/etc/lib')

import os
from os import listdir
import sys
import re
import mechanize
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
from multiprocessing import Pool
import gspread

dir = os.getcwd()
dir = dir.strip()
lib = '/etc/lib'

# os.chdir('/etc/lib/')
# import imp
# imp.load_source('sheet', '/etc/lib/')
from sheet import *
# os.chdir(dir)

def return_DOB_age(string):
	string = " ".join(string.split())
	string = string.split(' ')
	DOB = string[0]
	Age = string[1]
	Age = Age.replace('(', '')
	Age = Age.replace(')', '')
	return DOB, Age
# def logout(br):
# 	url = "https://xplan.mlc.com.au/home/logoff?"
# 	br.open(url)
def c_p_details(myRec):
	key = [ 'XPLAN Entity ID',
		'Title',
		'Surname',
		'Second Name',
		'Maiden Name',
		'Preferred Name',
		'Initials',
		'Gender',
		'Date of Birth',
		'Date of Death',
		'Marital Status',
		'Nationality',
		'Native Language',
		'Tax File Number',
		'Occupation',
		'Employer',
		'Employment Income',
		'Health',
		'Smoker',
		'Will Exists',
		'Power of Attorney',
		'Last reviewed',
		'Address Line 1',
		'Address Line 2']
	cPersonalDetails = {'worksheet': 'cPersonalDetails'}
	pPersonalDetails = {'worksheet': 'pPersonalDetails'}
	all_ = {} 
	for i in key:
		try:
			data = myRec[i]
			index1 = data[0]
			index2 = data[1]
			if not index1:
				index1 = ''
			if not index2:
				index2 = ''
			if i == 'Date of Birth':
				DOB1, age1 = return_DOB_age(index1)
				DOB2, age2 = return_DOB_age(index2)	
				cPersonalDetails[i] = DOB1
				pPersonalDetails[i] = DOB2	
				cPersonalDetails['Age'] = age1
				pPersonalDetails['Age'] = age2	
			else:
				cPersonalDetails[i] = index1
				pPersonalDetails[i] = index2
		except:
			# if null temporary put it as none
			cPersonalDetails[i] = ''
			pPersonalDetails[i] = ''
	# worksheet_list = [cPersonalDetails, pPersonalDetails]
	# for i in xrange(len(worksheet_list)):
	# 	all_[i] = worksheet_list[i]
		# print all_
	# write_json('test2.json', cPersonalDetails)
	# write_json('test2.json', ',')
	# write_json('test2.json', pPersonalDetails)
	update_json('test2.json', cPersonalDetails)
	update_json('test2.json', pPersonalDetails)
	# print cPersonalDetails
	# print pPersonalDetails
#def parse(br, URL):
def parse(parameter):
	# br, URL = parameter
	myRec2 = {}
	URL = parameter
	not_incl = ['Min.', 'Target', 'Max.', 'N/A', 'Other (Category)', 'Defensive', 'Growth']
	f = lambda x: x and x.startswith(('fieldhide_'))
	soup=br.open(URL)
	soup=str(BeautifulSoup(soup))
	soup = BeautifulSoup(soup)
	# print soup
	allList=[]
	all_percent = []
	sub_percent = []
	all_data =[]
	Entities = [] #{'worksheet':'Entities'}
	#################
	# print URL
	# sys.exit()
	#################
	for element in soup.find_all(id=f):
		# print element.text
		keydetails = {'Type of Fund':'Superfund', 'Trust Type':'Trust', 'Company Type': 'Company'}
		flag = False
		try:

			i=(element.get_text(strip=False))
			i=i.split('\n')
			i=[x.strip(' ') for x in i]
			i=[item.replace(u'\xa0', u'') for item in i]
			i=[item.replace(u'\xc2', u'') for item in i]
			i=filter(None, i)
			if i:
				# print i
				# raw_input('hello')
				if len(i) > 100:
					# print len(i)
					flag = False
					cnt = 0
					# inc = 0
					for z in i:
						# print z
						if re.search('CDATA', z):
							break
						# elif re.search('Class', z):
						# 	flag = True
						if z not in not_incl:
							if re.search('%', z):
								# print z
								z = z.replace('%', '')
								z = float(z)
								# inc += 1
								# print inc
								sub_percent.append(z)
								cnt += 1
								if cnt == 3:
									cnt = 0
								# 	print sub_percent
									all_percent.append(sub_percent)
									# print sub_percent
									# raw_input()
									sub_percent = []
							else:
								# print z
								excl = ['Class', 'Agreed Asset Allocations']
								if z not in excl:
									all_data.append(z)
							# if re.search('.', z):
							# 	# print z
							# 	# raw_input()
							# 	sub_percent.append(z)
							# 	inc += 1
							# 	if inc == 3:
							# 		inc = 0
							# 		all_percent.append(sub_percent)
							# 		sub_percent = []
							# else:
							# 	# print z
							# 	all_data.append(z)
				if len(i) > 0 and len(i) == 2:
					i.append('')
					if i not in allList and not re.search('Partner', i[1]):
						allList.append(i) 
						if not re.search('Comments', i[0]):
							# data = {[i[0]]:[i[1], i[2]]}
							myRec2[i[0]] = [i[1], i[2]]
							Entities.append(i[1])
				elif len(i) > 0 and len(i) == 3:
					if i not in allList:
						allList.append(i) 
						if not re.search('Comments', i[0]):
							# data = {[i[0]]:[i[1], i[2]]}
							myRec2[i[0]] = [i[1], i[2]]
				else: pass
								# print i
				for z in keydetails.keys():
					if re.search(z, str(i)):
						flag = True
						break
				if flag:
					# key = 'Type' + keydetails[z]
					myRec2['Type'] = [keydetails[z], '']
					# Entities.append(key)
					break

			else: pass
		except:
			pass
	# print Entities
	myL = len(all_data) 
	inc = 0
	flag = 0
	AssetsTbl = {'worksheet':'AssetsTbl'}
	AssetsTbl_Entity1 = {'worksheet':'AssetsTbl_Entity1'}
	AssetsTbl_Entity2 = {'worksheet':'AssetsTbl_Entity2'}
	AssetsTbl_Entity3 = {'worksheet':'AssetsTbl_Entity3'}
	AssetsTbl_Entity4 = {'worksheet':'AssetsTbl_Entity4'}
	AssetsTbl_Entity5 = {'worksheet':'AssetsTbl_Entity5'}
	AssetTBL_all = []
	for i in  all_percent:
		i = list(set(i))
		if len(i) > 1:
			value = str(i[1])
			if flag == 0:
				AssetsTbl['Equity'] = all_data[inc]
				AssetsTbl['Percentage'] = value 
				AssetsTbl['Legend'] = ''
				AssetTBL_all.append(AssetsTbl)
				update_json('test2.json', AssetsTbl)
				AssetsTbl = {'worksheet':'AssetsTbl'}
			if flag == 1:
				AssetsTbl_Entity1['Equity'] = all_data[inc]
				AssetsTbl_Entity1['Percentage'] = value 
				AssetsTbl_Entity1['Legend'] = ''
				AssetTBL_all.append(AssetsTbl_Entity1)
				update_json('test2.json', AssetsTbl_Entity1)
				AssetsTbl_Entity1 = {'worksheet':'AssetsTbl_Entity1'}
			elif flag == 2:
				AssetsTbl_Entity2['Equity'] = all_data[inc]
				AssetsTbl_Entity2['Percentage'] = value
				AssetsTbl_Entity2['Legend'] = ''
				AssetTBL_all.append(AssetsTbl_Entity2)
				update_json('test2.json', AssetsTbl_Entity2)
				AssetsTbl_Entity2 = {'worksheet':'AssetsTbl_Entity2'}				
				# print all_data[inc], i[1			elif flag == 1:
			elif flag == 3:
				AssetsTbl_Entity3['Equity'] = all_data[inc]
				AssetsTbl_Entity3['Percentage'] = value 
				AssetsTbl_Entity3['Legend'] = ''
				AssetTBL_all.append(AssetsTbl_Entity3)
				update_json('test2.json', AssetsTbl_Entity3)
				AssetsTbl_Entity3 = {'worksheet':'AssetsTbl_Entity3'}
			elif flag == 4:
				AssetsTbl_Entity4['Equity'] = all_data[inc]
				AssetsTbl_Entity4['Percentage'] = value 
				AssetsTbl_Entity4['Legend'] = ''
				AssetTBL_all.append(AssetsTbl_Entity4)
				update_json('test2.json', AssetsTbl_Entity4)
				AssetsTbl_Entity4 = {'worksheet':'AssetsTbl_Entity4'}
			elif flag == 5:
				AssetsTbl_Entity5['Equity'] = all_data[inc]
				AssetsTbl_Entity5['Percentage'] = value
				AssetsTbl_Entity5['Legend'] = ''
				AssetTBL_all.append(AssetsTbl_Entity5)
				update_json('test2.json', AssetsTbl_Entity5)
				AssetsTbl_Entity4 = {'worksheet':'AssetsTbl_Entity5'}		
		inc += 1
		if inc == myL:
			flag += 1
			inc = 0
	# return AssetTBL_all
	# key = "1M3qsO6IkPoVFBHYkqVgDlC18KQmeP9RaU3TbGuFEqk0"
	# sheet = access_sheet(key)
	# jobs = []
	# pp = Pool(processes=4)
	if AssetTBL_all:
		update_json('test2.json', AssetTBL_all)
		pass
	if myRec2:
		update_json('client_partner.json', myRec2)
		len_ = get_json_key_val('client_partner.json')
		if len(len_[0]) == 3:
			data_ = {}
			for x in len_[1]:
				data_.update(x)
			c_p_details(data_)
			remove_file('client_partner.json')
		pass
	# return myRec2

def login(parameter):
	uname, password, URLs = parameter
	# password = 'qppsoa2016'
	global br
	br = mechanize.Browser()
	br.set_handle_robots(False)   # no robots
	br.set_handle_refresh(False)  # can sometimes hang without this
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	br.open("https://xplan.mlc.com.au/home")	   #Url that contains signin form
	br.select_form(nr=0)
	br['userid'] = uname	#see what is the name of txt input in form
	br['passwd'] = password
	br.submit()
	P = Pool(processes=8)
	P.map(parse, URLs)
	return br


def ret_c_p_details(parameter):
	global myRec
	myRec = {}
	P = Pool(processes=8)
	jobs = []
	URLs = []
	# userids, uname, password = parameter
	userids, uname, password = parameter
	for userid in userids:
		userid = str(userid)
		URLs_= [ "https://xplan.mlc.com.au/factfind/view/%s?role=client&page=main" % (userid),
				"https://xplan.mlc.com.au/factfind/view/%s?role=client&page=estate" % (userid),
				"https://xplan.mlc.com.au/factfind/view/%s?role=client&page=personal_habits" % (userid),
				"https://xplan.mlc.com.au/factfind/view/%s?role=client&page=investment" % (userid)
				]
		for i in URLs_:
			URLs.append(i)
	url = "https://xplan.mlc.com.au/home/logoff?"
 
	parameter = uname, password, URLs
	br = login(parameter)
	br.open(url)
	# return c_p_details(myRec)


# userids = '6689208' #'6280313' #'6280276' #'6702033' #'6689208' #'3417039' #6689208
userids = sys.argv[1]
userids = re.findall("\d+", userids)

uname = "ross.corry"
password = 'QPP2015b'
parameter = userids, uname, password
# init_json('test2.json')
# init_json('client_partner.json')
# ret_c_p_details(parameter)


# #Writing to gsheet

P = Pool(processes=8)
# jobs = read_json('test2.json')
jobs = get_json_key_val('test2.json')
jobs = jobs[1]
global nako
nako = []
hello = []
try:
	for i in jobs:
		if i['worksheet'] not in hello:
			hello.append(i['worksheet'])
		else:
			nako.append(i[worksheet])
except:
	pass
print nako
sys.exit()
key = "1M3qsO6IkPoVFBHYkqVgDlC18KQmeP9RaU3TbGuFEqk0"
sheet = access_sheet(key)

filename = 'record'
create_file(filename)

jobs = [(sheet, worksheet) for worksheet in jobs]
P.map(update_sheet, jobs)

remove_file(filename)


#sudo kill -9 `ps -fA | grep helloflask | awk '{print $2}'`






