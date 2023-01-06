
# ############################
# # Connection to MongoDB
# ############################
# import pymongo
# from pymongo import MongoClient
# import random
# from time import sleep
# import streamlit as st

# # st.title("MongoDB Connection")
# # Conexion con Mongodb Atlas in PC windows and  in cloud streamlit

# # cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")

# cluster = pymongo.MongoClient("mongodb://localhost:27017/")

# db = cluster["peruviansunrise"]
# collection = db["activities"]
# collection.insert_one({"_id":12, "user_name":"Fidel"})





############################
# insertar todas los lugares en la base de datos mongo db
# incluir una imagen en blanco para evitar errores
############################
# import streamlit as st
import pymongo
from pymongo import MongoClient
import random
from time import sleep



# st.title("MongoDB Connection")
# Conexion con Mongodb Atlas in PC windows and  in cloud streamlit

# cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")

cluster = pymongo.MongoClient("mongodb://localhost:27017/")

db = cluster["peruviansunrise"]
collection = db["locations"]

data = [ "Abancay (Peru)", "Abra Malaga (Peru)","Aguas Calientes/ Machu Picchu (Peru)","Aguas Calientes Train Station (Peru)","Amantani Island (Peru)","Amaru (Peru)","Ananta (Peru)","Ancash (Peru)","Andamarca ayacucho (Peru)","Apurimac (Peru)","Arequipa (Peru)","Arequipa Airport (AQP)  (Peru)","Arequipa Bus Station (Peru)","Arequipa & Colca Canyon (Peru)","Ausangate Lake (Peru)","Ausangate Trek (Peru)","Ayacucho (Peru)","Ayaviri (Peru)","Ballestas (Peru)","Bambu Lodge (Peru)","Barranco (Peru)","Cabanaconde (Peru)","Caicay (Peru)","Cajamarca (Peru)","Calca (Peru)","Camaná (Peru)","Canocota (Peru)","Caral (Peru)","Caraz (Peru)","Casa Matshiguenka (Peru)","Casma (Peru)","Chacco Huayllasca (Peru)","Chachapoyas (Peru)","Challacancha (Peru)","Chaparri (Peru)","Chaquicocha (Peru)","Chaullay (Peru)","Chazuta (Peru)","Checacupe (Peru)","Chicama (Peru)","Chiclayo (Peru)","Chiclayo Int. Airport (CIX) (Peru)","Chikiska (Peru)","Chillca (Peru)","Chincha (Peru)","Chinchero (Peru)","Chivay (Peru)","Choquequirao (Peru)","Choquetecarpo (Peru)","Chucuito (Peru)","Cocachimba (Peru)","Colca (Peru)","Colca Canyon (Peru)","Colcapampa (Peru)","Colcapampa (Peru)","Corao (Peru)","Corral Pampa (Peru)","Corto Maltes Lodge (Peru)","Cotahuasi (Peru)","Cruz Del Sur Bus Station (Paracas) (Peru)","Cuispes (Peru)","Cuncani (Peru)","Cusco (Peru)","Cusco Airport (CUZ) (Peru)","Cusco Bus Station (Peru)","Cutatambo (Peru)","Cuzco Int. Airport (CUZ) (Peru)","Delete (Peru)","Fure (Peru)","Guayaquil (Peru)","Heliconia Lodge  (Peru)","Huacachina (Peru)","Huacahuasi (Peru)","Huamanmarca (Peru)","Huancacalle (Peru)","Huancas (Peru)","Huancavelica (Peru)","Huancaya (Peru)","Huancayo (Peru)","Huaraz (Peru)","Huaraz Bus station (Peru)","Huaripampa (Peru)","Huascaran National Park (Peru)","Huayhuash (Peru)","Huayllabamba (Peru)","Huayopata (Peru)","Huchuy Qosqo (Peru)","Huilloc (Peru)","Hummingbird Lodge (Peru)","Ica (Peru)","Ica Bus Station (Peru)","Inca Trail (Peru)","Inkaterra Hacienda Concepcion (Peru)","Inti Cocha (Peru)","Ipsayccasa Lagoon (Peru)","Iquitos (Peru)","Iquitos Airport (IQT) (Peru)","Iquitos City (Peru)","Jaen (Peru)","Jaen Airport (Peru)","Jampa (Peru)","Jatun Pucacocha (Peru)","Jorge Chavez International Airport (LIM) (Peru)","Juliaca (Peru)","Juliaca Airport (JUL) (Peru)","Kuelap (Peru)","Laguna Huamantay (Peru)","Laguna Jauacocha (Peru)","Lake Titicaca (Peru)","Lamay (Peru)","Lamay Lodge (Peru)","Lampa (Peru)","Lamud (Peru)","La Playa (Peru)","Laraos (Peru)","Lares Hot Springs (Peru)","Leymebamba (Peru)","Lima (Peru)","Lima Bus Station (Peru)","Lima Int. Airport (LIM) (Peru)","Llachon  (Peru)","Llactapata (Peru)","Llahuar (Peru)","Llama Corral (Peru)","Llulluchapampa (Peru)","Loreto (Peru)","Los Organos (Peru)","Lucmabamba (Peru)","Lunahuana (Peru)","Luquina (Peru)","Luya (Peru)","Machu Picchu (Peru)","Maizal (Peru)","Mancora (Peru)","Manu National Park (Peru)","Maquisapayoj Lodge (Peru)","Maras (Peru)","Millpu (Peru)","Miraflores (Peru)","Mollepata (Peru)","Moquegua (Peru)","Moray (Peru)","Moyobamba (Peru)","Nasca (Peru)","Nasca Bus Station (Peru)","Nazca (Peru)","Nazca Lines (Peru)","Northern Peru (Peru)","Nuevo Tingo (Peru)","Ollantaytambo (Peru)","Ollantaytambo Train Station (Peru)","Oxapampa (Peru)","Pacaymayo (Peru)","Paccha (Peru)","Pacchanta (Peru)","Pacchapampa (Peru)","Pachar (Peru)","Pacllón (Peru)","Pampa cangallo (Peru)","Pampachiri (Peru)","Paracas (Peru)","Paracas Bus Station (Peru)","Paron Lake (Peru)","Patabamba (Peru)","Patacancha (Peru)","Patria (Peru)","Paucartambo (Peru)","Phuyupatamarca (Peru)","Pilco (Peru)","Pisac (Peru)","Pisco (Peru)","Piskacucho (Peru)","Pispitayoc (Peru)","Piura (Peru)","Piura Airport (PIU) (Peru)","Playa Campsite or Cola de Mono (Peru)","Poroy Train Station (Peru)","Pucallpa (Peru)","Pucara (Peru)","Puerto inca (Peru)","Puerto Maldonado (Peru)","Puerto Maldonado Int. Airport (PEM) (Peru)","Puno (Peru)","Puno Bus Station (Peru)","Puno Train Station (Peru)","Punta Sal (Peru)","Quehue (Peru)","Quishuarani (Peru)","Quito (Peru)","Rainbow Mountain (Peru)","Raqchi (Peru)","Rayampata (Peru)","Refugio Amazonas Lodge (Peru)","Reserva Amazonica (Peru)","Rioja (Peru)","Rocoto (Peru)","Sacred Valley (Peru)","Salkantay Trek  (Peru)","Sangalle (Peru)","San Roque de Cumbaza (Peru)","Santa Cruz (Peru)","Santa Maria (Peru)","Santa Teresa (Peru)","Sondor  (Peru)","Soraypampa (Peru)","Southern Peru (Peru)","Soyrococha (Peru)","Soyrococha (Peru)","Suasi (Peru)","Tacna  (Peru)","Tahuayo Tamshiyacu (Peru)","Talara (Peru)","Tambopata (Peru)","Tambopata Research Center (Peru)","Tambopata y Manu (Peru)","Taquile Island (Peru)","Tarapoto (Peru)","Tarma (Peru)","Taullipampa (Peru)","The Amazon (Peru)","The Andes (Peru)","Tingana (Peru)","Trujillo (Peru)","Trujillo Airport (TRU) (Peru)","Tucume (Peru)","Tumbes (Peru)","Upis (Peru)","Urquillos (Peru)","Urubamba (Peru)","Viacha (Peru)","Vichayito (Peru)","Waqrapukara (Peru)","Wiñayhuayna (Peru)","Yanapaccha (Peru)","Yanque (Peru)","Yuncachimpa (Peru)"]


for  location in data:
    
# blank.jpg is the image that will be used as the background, it's any image saved in s3 aws.
    record = {
    "Name_en": location, # ingles
    "Name_de": location, # aleman
    "Name_es": location, # español
    "Country": "Peru",
    "Description_en": "",
    "Description_de": "",
    "Description_es": "",
    "Images": "blank.jpg",
    }
    collection.insert_one(record)


