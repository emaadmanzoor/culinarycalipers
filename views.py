from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.files import File
import urllib2
import json
import re
import time

def index(request):
    return render_to_response('index.html', locals())

def diff(request):
    restaurants = [0, 0, 0]
    ratings = [-1, -1, -1]
    loaded = False
    for k, v in request.GET.iteritems():
        index = re.search("\d+", k).group(0)
        if not "rest" in k:
            ratings[int(index) - 1] = v
            loaded = True
        else:
            url = "https://api.zomato.com/v1/restaurant.json/" + v
            request = urllib2.Request(url, None, {"X-Zomato-API-Key": "4eb0bc1d9f8015870256524eb0bc1d9f"})
            response = urllib2.urlopen(request)
            data = response.read()
            restaurants[int(index) - 1] = json.loads(data)
        
    return render_to_response('diff.html', {"data": zip(restaurants, ratings), "loaded": loaded})
    
def get_permalink(request):
    ids = [0, 0, 0]
    ratings = [-1, -1, -1]
    
    for k, v in request.GET.iteritems():
        index = re.search("\d+", k).group(0)
        if "rest" in k:
            ids[int(index) - 1] = v
        else:
            ratings[int(index) - 1] = v
    
    timestamp = str(int(time.time()))
    rankdata = {}
    rankdata[timestamp] = {}
    for id, rating in zip(ids, ratings):
        rankdata[timestamp][id] = rating
    
    rankfile = File(open('data/ranking.dat', 'a'))
    rankfile.write(json.dumps(rankdata) + "\n")
    rankfile.close()
    
    params = request.GET.urlencode()
    permalink = "http://localhost:8000/diff/?" + params
    return render_to_response('permalink.html', {"permalink" : permalink})