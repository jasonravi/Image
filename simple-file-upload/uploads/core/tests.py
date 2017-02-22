from django.test import TestCase

# Create your tests here.

from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import csv

import os
import json
import urllib
import pprint

fields='fields=og_object{id,description,title,type,url,site_name,image,is_scraped,updated_time,audio,video,locale},id,share'

ACCESS_TOKEN = 'EAACEdEose0cBAJMcpfDXhMHtAT6drrgHhSCpezcF2MGWN9uJaBfNuQQr1tmh9XSi2ZBmGt00LwPbaQRTGJna06ZCMNxvP7A56Wb7KZAZAkBSK2tdYqDO6jIomNwzkrikCKZBqFVmyhync99KWi6QtZANZAZCfZB1OQZCFZBXiTQVH2EAKvYQLHQAngZC5ZAemzvgbi4gZD'
host = "https://graph.facebook.com/v2.3"
pathoffilename = '/home/knappily/a.csv'
params = urllib.urlencode({"access_token": ACCESS_TOKEN})
def func(request):
    with open(pathoffilename, 'rb') as csvfile:
        url_data = []
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            path = "id=" + row[0]
            #print path
            url = "{host}?{path}&{params}".format(host=host,path=path, params=params)
            #print url
            try:
                resp = urllib.urlopen(url).read()
                data = json.loads(resp)
                #print data
                path = "id=" + data['og_object']['id']
                #print path
                url = "{host}?{path}&{params}".format(host=host,path=path, params=params)
                #print url
                try:
                    resp = urllib.urlopen(url).read()
                    data = json.loads(resp)
                    d = {}
                    d['url'] = row[0]
                    d['title'] = data['title']
                    d['image'] = data['image'][0]['url']
                    url_data.append(d) 
                except Exception as e:
                    print 'error 1 is:',e

            except Exception as e:
                print 'error is',e  
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    spamwriter = csv.writer(response)
    for i in range(len(url_data)):
    	print url_data[i]['url'],url_data[i]['title'],url_data[i]['image']
    	spamwriter.writerow([url_data[i]['url'],url_data[i]['title'],url_data[i]['image']])
    return response
