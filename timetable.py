#!/usr/bin/env python
from bs4 import BeautifulSoup
import re, csv, codecs, requests, os
from datetime import datetime
from tabulate import tabulate
from requests_ntlm import HttpNtlmAuth
from robobrowser import RoboBrowser

def write_to_csv(output_file_name,q):
	time_table = []
	for i in range(1,4):
		with open('timetable_temp_'+str(i)+'.html', 'r', encoding="utf-8") as f:
			page = f.read()
		soup = BeautifulSoup(page,'html.parser')
		rows = soup.find('table',{'id':'ctl00_ContentMain_gvTimetable'}).findAll('tr')
		for row in rows:
				cols = [re.sub('\s+', ' ', ele.text.strip()) for ele in row.findAll('td')]
				if cols: time_table.append([ele for ele in cols])
	[r.pop(-1) for r in time_table] and [r.pop(0) for r in time_table]
	for row in time_table:
		for x in range(len(row)): row[x] = str(row[x])
		row[0] = str(datetime.strptime(row[0],'%d %B %Y').strftime('%d/%m/%Y'))
		row[3] = str(row[3] + " (" + row[4] + ")")
		row[5] = str(row[5].replace(", ","/"))
	[r.pop(4) for r in time_table]
	time_table.sort(key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'))
	if q == 0: print(tabulate(time_table,headers =['Date','Start','End','Module','Location','Type']))
	with codecs.open(output_file_name, 'wb', encoding = 'utf-8') as myfile:
		if q == 0: print("writing all events to "+output_file_name)
		myfile.write("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private\n")
		for row in time_table: myfile.write("\""+row[3]+"\","+row[0]+","+row[1]+","+row[0]+","+row[2]+",False,"+row[5]+","+row[4]+",True\n")
		
def scrape_calendar(u,p,q):
	username = u
	password = p
	s = requests.Session()
	s.auth = HttpNtlmAuth(u, p, s)
	browser = RoboBrowser(session=s,parser = 'html.parser')
	#push through the auth, redirs to a timeout page otherwise
	s.get('https://www.essex.ac.uk/timetables/default.aspx')
	x = browser.open('https://www.essex.ac.uk/timetables/nojstimetable.aspx?nojs=1')
	form = browser.get_forms()[1]
	for i in range(1,4): 
		form['ctl00$ContentMain$DrpDownTermChoose'].value = form['ctl00$ContentMain$DrpDownTermChoose'].options[i]
		browser.submit_form(form)
		with codecs.open("timetable_temp_"+str(i)+".html", 'w', encoding = 'utf-8') as myfile:
			myfile.write(str(browser.parsed).strip())
			if q == 0: 
				daterange = [datetime.strptime(x,'%d/%m/%Y %H:%M:%S').strftime('%d/%m/%Y') for x in form['ctl00$ContentMain$DrpDownTermChoose'].options[i].split('#')]
				print("writing date range "+daterange[0]+" -- "+daterange[1]+" to file: timetable_temp_"+str(i)+".html")
		browser.back

def remove_temp_files():
	for i in range(1,4): os.remove('timetable_temp_'+str(i)+'.html')
		
quiet = 0 # 0 for verbatim and 1 for quiet
scrape_calendar('username@essex.ac.uk','password',quiet)
write_to_csv('timetable_test.csv',quiet)
remove_temp_files()
