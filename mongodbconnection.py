
############################
# Connection to MongoDB
############################
import pymongo
from pymongo import MongoClient
import random
from time import sleep
import streamlit as st

# st.title("MongoDB Connection")
# Conexion con Mongodb Atlas in PC windows and  in cloud streamlit

# cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")

cluster = pymongo.MongoClient("mongodb://localhost:27017/")

db = cluster["peruviansunrise"]
collection = db["activities"]
collection.insert_one({"_id":12, "user_name":"Fidel"})




