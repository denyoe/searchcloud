import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import cloudsearchbe.tools.parser2 as p
import cloudsearchbe.tools.elementary as el


# Create your views here.
def home(request):
    print("Welcome page")
    context = {}  # Nothing to send
    return render(request, 'cloudsearchbe/first.html', context)


def welcome(request):
    return HttpResponse(json.dumps({'message':'Welcome to the Search Cloud API. Are you sure you should be here !?'}), content_type="application/json")

@csrf_exempt
def find_keywords(request):
    text = request.POST.get('text')
    kw = el.find_keywords(text)
    context = {"keywords": kw}
    return HttpResponse(json.dumps(context), content_type="application/json")


# @csrf_exempt
# def get_search_fetch(request):
#     kws = json.loads(request.POST.get('keywords')) # a list of keywords
#     #query = " ".join(kw for kw in kws) # a string of keywords
#     ln_info = p.get_search_fetch(kws) # a list of jsons
#     context = {"content": kws,
#                "links": ln_info
#     }
#     return HttpResponse(json.dumps(context), content_type="application/json")
#
#
#
@csrf_exempt
def get_search_fetch(request):
    kws = json.loads(request.POST.get('keywords')) # a list of keywords

    context = p.get_search_fetch(kws)
    return HttpResponse(context, content_type="application/json")


@csrf_exempt
def get_res_by_types(request):
    kws_with_types = json.loads(request.POST.get('keywords'))
    context = p.get_search_fetch_by_types(kws_with_types)
    return HttpResponse(json.dumps(context), content_type="application/json")



def get_engines(request):
    #engines = t.get_engines() # TODO update? function to call
    engines = ["dummy1", "dummy2"]
    context = {'engines': engines}
    return HttpResponse(json.dumps(context), content_type="application/json")


