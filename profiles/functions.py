from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse

from companies.models import Company, Member, Admin
from django.contrib.auth.models import User, Group

import urllib2
import json

from string import ascii_uppercase
# Google Sheets API Dependencies
# from oauth2client.client import OAuth2WebServerFlow
# from oauth2client.tools import run
# from oauth2client.file import Storage

# def get_oauth2_token(request):
#     CLIENT_ID = '926398386913-osgjnrb1p57m28rtqmrc0oeru2jmm2u2.apps.googleusercontent.com'
#     CLIENT_SECRET = 'nhB0NqaKQd8N4jmUP4wEihGB'

#     flow = OAuth2WebServerFlow(
#         client_id = CLIENT_ID,
#         client_secret = CLIENT_SECRET,
#         scope = 'https://spreadsheets.google.com/feeds https://docs.google.com/feeds',
#         redirect_uri = 'http://localhost:8000/'
#         )
#     storage = Storage('creds.data')
#     credentials = run(flow, storage)
#     print "access_token: %s" % credentials.access_token

# Function to make sure user has access to the company and profile they are trying to access
def memberAuth(request, company_name, member_name):
    # make sure group exists
    company = get_object_or_404(Company, name=company_name)

    if request.user.is_authenticated() and member_name == request.user.username:
        # make sure user is a part of the group they are trying to access
        if request.user.groups.filter(name=company_name).exists():
            return Member.objects.get(username=member_name)
    return None

def adminAuth(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    if request.user.is_authenticated() and member_name == request.user.username:
        # make sure user is an admin of the company they are trying to access
        if Admin.objects.filter(member__username=member_name, company=company).exists():
            return Admin.objects.get(member__username=member_name, company=company)
    
    return None

def get_json(format, calID, day):
    #Adsf
    url = 'https://spreadsheets.google.com/feeds/%s/%s/%d/public/basic?prettyprint=true&alt=json' % (format, calID, day);
    response = urllib2.urlopen(url)
    html = response.read()
    return json.loads(html)

def get_col_headers(html):
    COL_MAX = 'J'
    ROW_MAX = '31'
    columns = ascii_uppercase.split(chr(ord(COL_MAX)+1))[0]

    format = []
    for entry in html['feed']['entry']:
        # print entry['title']['$t'].encode('utf-8').strip()
        if len(entry['title']['$t'].encode('utf-8').strip()) == 2 and entry['title']['$t'].encode('utf-8').strip().endswith('1'):
            format.append(entry['content']['$t'].encode('utf-8').strip())

    return format

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

# -----------------------------------------
@login_required
def profileAuth(request, company_name, member_name):
    company = get_object_or_404(Company, name=company_name)

    # user must come from profile page to get here... don't need to reauthenticate
    if request.user.is_authenticated() and member_name == request.user.username:
        try:
            member = company.member_set.get(netid=member_name)
        except (KeyError, Member.DoesNotExist):
            return redirect('profiles:profile', company_name, member_name,)
        else:
            pass
    else:
        return redirect('profiles:profile', company_name, member_name,)
