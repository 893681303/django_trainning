from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import humanize
import datetime
# Create your views here.


# Create your views here.
def index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
def home(request):
    now = datetime.datetime.now()
    return render_to_response('home.html', locals(), context_instance=RequestContext(request))


