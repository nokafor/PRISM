'''
@desc Parse Google Drive spreadsheet data via python
@author Misha M.-Kupriyanov https://plus.google.com/104512463398531242371/
@link https://gist.github.com/3969255
'''
# Spreadsheet https://docs.google.com/spreadsheet/pub?key=0Akgh73WhU1qHdFg4UmRhaThfUFNBaFR3N3BMVW9uZmc&output=html

import urllib2
import json

from string import ascii_uppercase

def getRowValue(row, format, column_name):
    # change column name to match name in json representation
    column_name = column_name.lower().replace(' ', '')
    
    if str(column_name) == '':
        raise ValueError('column_name must not empty')
        
    begin = row.find('%s:' % column_name)
           
    if begin == -1:
        return ''

    # get the beginning index for the resulting value
    begin = begin + len(column_name) + 1
    
    # get the ending index for the resulting value
    end = -1
    split_line = row.split(column_name)
    end_val = split_line[1].split(",", 1) 
    end += len(end_val[0])

    if end == -1:
        end = len(row)
    else:
        end = end + begin
        
    value = row[begin: end].strip()    

    return value


# get format list
for day in range(1,8):
    url = 'https://spreadsheets.google.com/feeds/cells/1lxsJV8fJdumBzN4fDn0Vwr80pwy-kGpJn1jcZpkRc2s/%d/public/basic?prettyprint=true&alt=json' % day;
    response = urllib2.urlopen(url)
    html = response.read()
    html = json.loads(html)

    COL_MAX = 'J'
    ROW_MAX = '31'
    columns = ascii_uppercase.split(chr(ord(COL_MAX)+1))[0]

    format = []
    for entry in html['feed']['entry']:
        # print entry['title']['$t'].encode('utf-8').strip()
        if len(entry['title']['$t'].encode('utf-8').strip()) == 2 and entry['title']['$t'].encode('utf-8').strip().endswith('1'):
            format.append(entry['content']['$t'].encode('utf-8').strip())


    # JSON Representation to get data
    url = 'https://spreadsheets.google.com/feeds/list/1lxsJV8fJdumBzN4fDn0Vwr80pwy-kGpJn1jcZpkRc2s/%d/public/basic?prettyprint=true&alt=json' % day;

    response = urllib2.urlopen(url)
    html = response.read()
    html = json.loads(html)

    # format = ['Bloomberg', 'Whitman', 'Wilcox', 'MPR', 'GFR', 'Dance Studio', 'Martial Arts', 'New South', 'Hagan']  

    dow = html['feed']['title']['$t'].encode('utf-8').strip()
    print dow
    print '========================='
    last_company = {}
    for name in format:
        last_company[name] = ''

    for entry in html['feed']['entry']:
        row = entry['content']['$t'].encode('utf-8').strip()
        time = entry['title']['$t'].encode('utf-8').strip()

        for name in format:
            company = getRowValue(row, format, name)
            # print "%s, %s:%s" % (time, name, company)
            # print company
            # print company, last_company[name]
            if company != last_company[name]:
                print "Time:%s %s:%s" % (time, name, company)
                last_company[name] = company



