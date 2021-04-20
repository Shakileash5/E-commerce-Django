from firebase import Firebase
import json

#https://pypi.org/project/firebase/
fileName = "data.json"
config = {
  "apiKey": "AIzaSyCOQJSl3zPjB2v1KIRh_eubuyKd461mnuU",
  "authDomain": "web-fx-da8ba.firebaseio.com/",
  "databaseURL": "https://web-fx-da8ba-default-rtdb.firebaseio.com/",
  "projectId": "web-fx-da8ba",
  "storageBucket": "https://web-fx-da8ba.com/",
}

firebase = Firebase(config)
db = firebase.database()
products = {}


def getAllData():
  global products
  products = db.child("Product").get()
  products = dict(products.val())
  return

def setData():
  with open(fileName, "r") as read_file:
          data = json.load(read_file)
  result = db.child("Product").set(data)
  return

def getData(id):
  global products
  result = {}
  for key in products.keys():
    #print(key)
    if key == id:
      return products[key]

  return {}

def getCategory(category):
  global products
  if products == {}:
    getAllData()
  result = []
  for key in products.keys():
    #print(products[key]["category"],category)
    if products[key]["category"] == category:
      result.append(products[key])
      #print("here")
  #print(result,"u",products)
  return result


def updateProduct(id,val):
  
  db.child("Product").child(id).update({"quantity": val})
  getAllData()
  
  return


getAllData()

def getCartData(id):
  data = db.child("userDetails").child(id).child("cart").get()
  print(data)
  return data.val()

def setCartData(id,data):
  db.child("userDetails").child(str(id)).child("cart").set(data)

def getOrderData():
  data = db.child("Orders").child("Requests").get()
  print(data.val())
  return data.val()

def getUserOrderData(id):
  data = db.child("userDetails").child(id).child("orders").get()
  print(data.val())
  return data.val()

def getOrderId():
  data = db.child("orderId").get().val()
  return data

def setOrderId(val):
  db.child("orderId").set(val)

def getOrders():
  data = db.child("Orders").child("Requests").get()
  return data.val()

def setOrderData(data):
  db.child("Orders").child("Requests").set(data)

def setUserOrderData(id,data):
  data = db.child("userDetails").child(id).child("orders").set(data)
  
def setUserDetails(id,data):
  db.child("userDetails").child(id).set(data)

#setCartData()

  #for key in data.key()
#Update
#db.child("users").child("Joe").update({"name": "Joe W Tilsed"})

#remove
#db.child("users").child("Joe").remove()

#get
#db.child("users").get()