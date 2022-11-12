
############################
# Connection to MongoDB
############################
import pymongo
from pymongo import MongoClient
import pandas as pd
import random
from time import sleep

# Conexion con Mongodb Atlas
cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")
# db = client.get_database("divisas")
db = cluster["peruviansunrise"]
collection = db["activities"]
collection.insert_one({"_id":5, "user_name":"Soumi"})
collection.insert_one({"_id":500, "user_name":"Ravi"})




