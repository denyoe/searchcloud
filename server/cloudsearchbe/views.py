import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    print("Welcome page")
    context = {}  # Nothing to send
    return render(request, 'cloudsearchbe/first.html', context)