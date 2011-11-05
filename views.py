from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
import urllib2
import json

def index(request):
    return render_to_response('index.html', locals())

def diff(request):
    restaurants = []
    for k, v in request.GET.iteritems():
        url = "https://api.zomato.com/v1/restaurant.json/" + v
        request = urllib2.Request(url, None, {"X-Zomato-API-Key": "4eb0bc1d9f8015870256524eb0bc1d9f"})
        response = urllib2.urlopen(request)
        data = response.read()
        restaurants.append(json.loads(data))
        
    return render_to_response('diff.html', {"data": restaurants})