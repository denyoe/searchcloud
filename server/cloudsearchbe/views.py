import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Use processing functions from tools. as t TODO


# Create your views here.
def home(request):
    print("Welcome page")
    context = {}  # Nothing to send
    return render(request, 'cloudsearchbe/first.html', context)

    
def find_keywords(request):
    text = request.POST.get('text')
    kw = t.find_keywords(text) # TODO update? function to call
    context = {"keywords": kw}
    return HttpResponse(json.dumps(context), content_type="application/json")


def search_fetch(request):
    text = request.POST.get('keywords')
    context = t.search_fetch(text) # TODO update? function to call
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_engines(request):
    engines = t.get_engines() # TODO update? function to call
    context = {'engines': engines}
    return HttpResponse(json.dumps(context), content_type="application/json")


