from engine import *
from multiprocessing import Pool
from sheet import *
import sys
# from client_partner_details import *
# import pathos.multiprocessing as mp

# P = Pool(processes=8)
userid = '3417039'
username = 'ross.corry'
password = 'QPP2015b'
# username = 'cristeta.locara'
# password = 'qppsoa2016'
config = [ 'expense',
		'asset',
		'liability',
		'dependent',
		'income'
		]
worksheet_list = []
engine = XPLANEngine (username=username,
	                      password=password)
engine.run()
init_json('test2.json')
for x in config:
	engine.fetch(x, userid)
# jobs = [(x, userid) for x in config]	
# P = Pool(processes=4) 
# P.map(engine.fetch, jobs)

engine.logout()

P = Pool(processes=8)
jobs = get_json_key_val('test2.json')
jobs = jobs[1]
key = "1M3qsO6IkPoVFBHYkqVgDlC18KQmeP9RaU3TbGuFEqk0"
sheet = access_sheet(key)

filename = 'record'
create_file(filename)

jobs = [(sheet, worksheet) for worksheet in jobs]
P.map(update_sheet, jobs)

remove_file(filename)
	
