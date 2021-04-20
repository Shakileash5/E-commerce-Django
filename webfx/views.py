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
from datetime import date
# Create your views here.

@csrf_exempt
def setDetails(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data["userId"]
            dataDict = {
                "email":data["email"],
                "phoneNo":data["phoneNo"],
                "orders": [],
                "cart": [],
            }
            result = setUserDetails(id,dataDict)
            return JsonResponse({"result":"Successfull","status":200})
        except:
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

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
                    temp["key"] = str(key)
                    #print(key)
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

@csrf_exempt
def addProduct(request):
    if request.method == "POST":
        try:
            data = request.POST.dict()
            data = json.loads(request.body.decode('utf-8'))
            #print(data,data["userId"])
            cartData = getCartData(data["userId"])
            
            #print("cartData",cartData)
            if type(data["data"])==type({}):
                if cartData == None:
                    setCartData(data["userId"],[data["data"]])
                else:
                    flag = 0
                    for val in cartData:
                        #print("fefe",val,data["data"])
                        if val["key"] == data["data"]["key"]:
                            flag = 1

                    if flag == 0:
                        cartData.append(data["data"])
                        setCartData(data["userId"],cartData)
            else:
                #print("here",len(data["data"]),data["userId"])
                setCartData(data["userId"],data["data"])
            #id = data["id"]
            #result = products[id]

            return JsonResponse({"result":"result","status":200})
        except Exception as e:
           print(e)
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getCartProducts(request):
    if request.method == "GET":
        try:
            data = request.GET.dict()
            #data = request.body.decode('utf-8')
            #print(data,"fytguhij")
            if data != None:
                #data = json.loads(data)
                #print(data,data["uid"])
                cartData = getCartData(data["uid"])
                uid = data["uid"]
                
                result = getCartData(uid)

                return JsonResponse({"result":result,"status":200})
            return JsonResponse({"result":result,"status":200})
        except Exception as e:
           print(e)
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getUserOrders(request):
    if request.method == "GET":
        try:
            data = request.GET.dict()
            #print(data,"orderProduct")
            uid = data["uid"]
              
            #cartData = getCartData(uid)
            orderData = getUserOrderData(uid)
            print(orderData,"cartData")
            return JsonResponse({"result":orderData,"status":200})
        except Exception as e:
           print(e)
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

@csrf_exempt
def orderProduct(request):
    if request.method == "POST":
        try:
            data = request.POST.dict()
            data = json.loads(request.body.decode('utf-8'))
            print(data,data["userId"])
            cartData = getCartData(data["userId"])
            orderData = getOrderData()
            userOrderData = getUserOrderData(data["userId"])
            lastOrderId = int(getOrderId())
            if type(cartData)==type({}):
                cartData = [cartData]
            if type(cartData)==type([]):
                for cartItem in cartData:
                    cartItem["orderDate"] = str(date.today())
                    cartItem["orderId"] = lastOrderId+1
                    cartItem["status"] = 0
                    cartItem["userId"] = data["userId"]
                    
                    lastOrderId+=1
            #print("cartData",cartData)
            if type(cartData)==type([]):
                if userOrderData == None:
                    setUserOrderData(data["userId"],cartData)
                    setCartData(data["userId"],None)
                    if orderData == None:
                        setOrderData(cartData)
                    else:
                        for cartItem in cartData:
                            orderData.insert(0,cartItem)
                        setOrderData(orderData)
                else:
                    
                    for cartItem in cartData:
                        userOrderData.insert(0,cartItem)
                    setUserOrderData(data["userId"],userOrderData)
                    setCartData(data["userId"],None)

                    if orderData == None:
                        setOrderData(cartData)
                    else:
                        for cartItem in cartData:
                            orderData.insert(0,cartItem)
                        setOrderData(orderData)
            else:
                print("here",len(data["data"]),data["userId"])
                #setCartData(data["userId"],data["data"])
            #id = data["id"]
            #result = products[id]
            setOrderId(lastOrderId)
            return JsonResponse({"result":userOrderData,"status":200})
        except Exception as e:
           print(e)
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})

def getAllOrders(request):
    if request.method == "GET":
        try:
            data = request.GET.dict()
            #print(data,"orderProduct")
              
            #cartData = getCartData(uid)
            orderData = getOrders()
            print(orderData,"orderData")
            return JsonResponse({"result":orderData,"status":200})
        except Exception as e:
           print(e)
           return JsonResponse({"status":500}) 
    return JsonResponse({"status":400})