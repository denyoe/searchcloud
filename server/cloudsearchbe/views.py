import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import cloudsearchbe.tools.parser as p


# Create your views here.
def home(request):
    print("Welcome page")
    context = {}  # Nothing to send
    return render(request, 'cloudsearchbe/first.html', context)


@csrf_exempt
def find_keywords(request):
    text = request.POST.get('text')
    #kw = t.find_keywords(text) # TODO update? function to call
    kw = ["dummy1", "dummy2", text]
    context = {"keywords": kw}
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def get_search_fetch(request):
    kws = json.loads(request.POST.get('keywords')) # a list of keywords
    query = " ".join(kw for kw in kws) # a string of keywords
    ln_info = p.google_to_json(query) # a list of jsons
    context = {"content": query,
               "links": ln_info
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_engines(request):
    #engines = t.get_engines() # TODO update? function to call
    engines = ["dummy1", "dummy2"]
    context = {'engines': engines}
    return HttpResponse(json.dumps(context), content_type="application/json")


