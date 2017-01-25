from bs4 import BeautifulSoup
import re, csv
from datetime import datetime
from tabulate import tabulate
import codecs
time_table = []

page = codecs.open('timetable.html', encoding='utf8').read()
#page = open("timetable.html").read()
soup = BeautifulSoup(page,'html.parser')
rows = soup.find('table',{'id':'ctl00_ContentMain_gvTimetable'}).findAll('tr')
for row in rows:
		print(row)
		cols = [re.sub('\s+', ' ', ele.text.strip()).encode('ascii', 'ignore') for ele in row.findAll('td')]
		if cols: time_table.append([ele for ele in cols])
[r.pop(-1) for r in time_table] and [r.pop(0) for r in time_table]
for row in time_table:
	for x in range(len(row)): row[x] = str(row[x].decode('ascii'))
	row[0] = str(datetime.strptime(row[0],'%d %B %Y').strftime('%d/%m/%Y'))
	row[3] = str(row[3] + " (" + row[4] + ")")
	row[5] = str(row[5].replace(", ","/"))
[r.pop(4) for r in time_table]
print(tabulate(time_table,headers =['Date','Start','End','Module','Location','Type']))
with codecs.open('timetable.csv', 'wb', encoding = 'utf8') as myfile:
 myfile.write("Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private")
 for row in time_table: myfile.write("\""+row[3]+"\","+row[0]+","+row[1]+","+row[0]+","+row[2]+",False,"+row[5]+","+row[4]+",True\n")
