from django.shortcuts import render
import json
from django.http import HttpResponse
from datetime import datetime
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import requests
from math import *
import math
from collections import Counter,OrderedDict
from django.http import JsonResponse
from .firebaseApp import *
# Create your views here.


def getProducts(request):
    if request.method == "GET":
        try:
            category = request.GET.dict()
            getAllData()
            return JsonResponse({"result":products,"status":200})
        except:
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getCategoryData(request):
    if request.method == "GET":
        try:
            category = request.GET.dict()
            category = category["category"]
            result = getCategory(category)
            return JsonResponse({"result":result,"status":200})
        except:
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getSearchResults(request):
    if request.method == "GET":
        try:
            data = request.GET.dict()
            keyword = data["keyword"].lower()
            result = []
            for key in products.keys():
                #print(keyword,products[key]["name"])
                if keyword in products[key]["name"].lower() or keyword in products[key]["category"].lower():
                    temp = products[key]
                    temp["key"] = key
                    result.append(temp)
            return JsonResponse({"result":result,"status":200})
        except:
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getProduct(request):
    if request.method == "GET":
        try:
            data = request.GET.dict()
            id = data["id"]
            result = products[id]

            return JsonResponse({"result":result,"status":200})
        except:
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})