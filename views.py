from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html', locals())

def diff(request):
    rest_1 = request.GET.get('rest_1', '')
    rest_2 = request.GET.get('rest_2', '')
    rest_3 = request.GET.get('rest_3', '')
    return render_to_response('diff.html', locals())