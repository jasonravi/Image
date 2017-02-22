import csv
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import os
import json
import urllib
import pprint

fields='fields=og_object{id,description,title,type,url,site_name,image,is_scraped,updated_time,audio,video,locale},id,share'

ACCESS_TOKEN = 'EAACEdEose0cBAOfrGJQiGQwyCgaAaRZBYPZCKgQXRGS931O2U3ZBYZBeLMG2ZCQySD2lLP3QMC8WcBQ7qJelMtwBRgeyrwOhSrrHUBuwQLbTiFi1DvZCGrzru5dwhIm1aqxhk5gkhSfSyCyFl6QLxuS8EEZA2mUZBbY0bXofAgoPUuJn2TZBLNWB820Xa80yc2kYZD'
host = "https://graph.facebook.com/v2.3"
pathoffilename = '/home/knappily/a.csv'
params = urllib.urlencode({"access_token": ACCESS_TOKEN})
with open(pathoffilename, 'rb') as csvfile:
    url_data = []
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        path = "id=" + row[0]
        #print path
        url = "{host}?{path}&{params}".format(host=host,path=path, params=params)
        #url = facebook_host + "?scrape=true&id=%s" %(row[0])
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
with open('output.csv', 'wb') as csvfile:
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=export.csv'
    spamwriter = csv.writer(csvfile, response)
    for i in range(len(url_data)):
        spamwriter.writerow([url_data[i]['url'],url_data[i]['title'],url_data[i]['image']])
    #return response
