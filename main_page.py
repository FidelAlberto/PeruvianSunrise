"""

Fidel Alberto Ramos Calachahuin
VittaQuant Technologies.
Peruvian Sunrise App
Cloud Streamlit

"""


# Import libraries to streamlit-pydantic
# https://github.com/gerardrbentley/streamlit-random/blob/main/pdf_merge_and_split.py

from streamlit_extras.mandatory_date_range import date_range_picker
from streamlit_extras.colored_header import colored_header


from datetime import date
from datetime import timedelta
import tempfile
from datetime import datetime
from io import BytesIO
from pathlib import Path
import streamlit as st
import streamlit_pydantic as sp
from typing import Optional, List
from streamlit_pydantic.types import FileContent
from pydantic import BaseModel, Field
from PyPDF2 import PdfFileWriter, PdfFileReader
import base64

#FIN
from s3connection import uploadimageToS3
from s3connection import get_link
from s3connection import delete_s3_file
from s3connection import copy_and_delete_s3_file



from genericpath import exists
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
# extra components
import hydralit_components as hc
import extra_streamlit_components as stx
# fin extra components
import numpy as np
import pandas as pd
import time
from streamlit_lottie import st_lottie
import requests
from PIL import Image

from streamlit_option_menu import option_menu
import random

import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode

# Mongo db connection needs
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import random
from time import sleep
#Define path to wkhtmltopdf.exe
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

#Define path to HTML file
path_to_file = 'sample.html'
# url = 'https://wkhtmltopdf.org/'



# Function to resize images
from PIL import Image
import requests
from io import BytesIO
import base64
def resize_image(image, width=600, height=400):
    url = image
    r = requests.get(url)
    pilImage = Image.open(BytesIO(r.content))
    pilImage = pilImage.resize((width,height), Image.ANTIALIAS)
    
    return pilImage
    
# Fin



onRowDragEnd = JsCode("""
function onRowDragEnd(e) {
    console.log('onRowDragEnd', e);
}
""")

getRowNodeId = JsCode("""
function getRowNodeId(data) {
    return data.id
}
""")

onGridReady = JsCode("""
function onGridReady() {
    immutableStore.forEach(
        function(data, index) {
            data.id = index;
            });
    gridOptions.api.setRowData(immutableStore);
    }
""")

onRowDragMove = JsCode("""
function onRowDragMove(event) {
    var movingNode = event.node;
    var overNode = event.overNode;

    var rowNeedsToMove = movingNode !== overNode;

    if (rowNeedsToMove) {
        var movingData = movingNode.data;
        var overData = overNode.data;

        immutableStore = newStore;

        var fromIndex = immutableStore.indexOf(movingData);
        var toIndex = immutableStore.indexOf(overData);

        var newStore = immutableStore.slice();
        moveInArray(newStore, fromIndex, toIndex);

        immutableStore = newStore;
        gridOptions.api.setRowData(newStore);

        gridOptions.api.clearFocusedCell();
    }

    function moveInArray(arr, fromIndex, toIndex) {
        var element = arr[fromIndex];
        arr.splice(fromIndex, 1);
        arr.splice(toIndex, 0, element);
    }
}
""")
############################
# Connection to MongoDB
############################


# Connection to MongoDB since applicacion in streamlit cloud
cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")
# Connection to MongoDB since applicacion in local
# cluster = pymongo.MongoClient("mongodb://localhost:27017/")
db = cluster["peruviansunrise"]

# FIN

# CREATION OF favicon

st.set_page_config(layout="wide",#"centered", 
    page_icon="🗽",
    page_title="Peruvian Sunrise")

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Roboto', sans-serif;
			}
            MainMenu {
            visibility:hidden;
            }

            footer
            {
                visibility:hidden;
            }
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)


# defining function to load lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# ------------------------------------------
# Initialize the bars and menus
with st.sidebar:
    menu_sidebar = option_menu("Program", ['Create new', "Crear programa", "Templates", "Save this program", "Data"],
        icons=['house', 'folder','save',"pencil-square"], menu_icon="cast", default_index=0)
    

##############################
# Data for Itinerary 
##############################

# Datos de Itinerary para usar en Activities & Transportation
    

destinos = ["Lima","Cusco","Arequipa","Madre de Dios","Ica"]

# Cargar los datos para que se guarden en el cache de sesion_state

if "adultos" not in st.session_state:
    st.session_state.adultos = 0
if "niños" not in st.session_state:
    st.session_state.ninos = 0    

if "contador" not in st.session_state:
    st.session_state['contador'] = 2
if "destino_1" not in st.session_state: 
    st.session_state['destino_1'] = "Lima"
if "destino_2" not in st.session_state: 
    st.session_state['destino_2'] = "Lima"
if "destino_3" not in st.session_state: 
    st.session_state['destino_3'] = "Lima"
if "destino_4" not in st.session_state: 
    st.session_state['destino_4'] = "Lima"
if "destino_5" not in st.session_state: 
    st.session_state['destino_5'] = "Lima"
if "destino_6" not in st.session_state: 
    st.session_state['destino_6'] = "Lima"
    
if "dias_1" not in st.session_state: 
    st.session_state['dias_1'] = 0
if "dias_2" not in st.session_state: 
    st.session_state['dias_2'] = 0
if "dias_3" not in st.session_state: 
    st.session_state['dias_3'] = 0
if "dias_4" not in st.session_state: 
    st.session_state['dias_4'] = 0
if "dias_5" not in st.session_state: 
    st.session_state['dias_5'] = 0
if "dias_6" not in st.session_state: 
    st.session_state['dias_6'] = 0
    
    
    
    
if menu_sidebar == "Create new":
    
    
    # st.info(f"Phase #{val}")
    lenguage = st.sidebar.selectbox("Lenguage", ["English", "Spanish", "Deutsch"], index=0)
    st.sidebar.selectbox("Type",["General", "Program with details"], index=0)
    st.sidebar.subheader("Passengers")
    adultos = st.sidebar.number_input("Personas adultas", min_value=0, max_value=50, value=1, step=1, key="adultos")
    niños = st.sidebar.number_input("Niños(a)", min_value=0, max_value=50, value=0, step=1, key="niños")
    st.sidebar.session_state.adultos = adultos
    st.sidebar.session_state.niños = niños
    
    
    st.sidebar.subheader("Itinerary")
    
    # Creation of table for Itinerary
    df_template = pd.DataFrame(
        '',
        index=range(10),
        columns=["Lugar", "Dias"])
    df_template.loc[-1] = ['Lima', 0]  # adding a row
    df_template.index = df_template.index + 1  # shifting index
    df_template.sort_index(inplace=True)

    with st.sidebar.form('example form') as f:
        
        # lista de las locations
        # Pedir datos de mongo db para  obtener los nombres de las actividades
        collection_location = db["locations"]
        data1 = collection_location.find({},{"Name_en":1})
        
        list_activitiess = []
        for value in data1:
            list_activitiess.append(value["Name_en"])
        # fin


        gb = GridOptionsBuilder.from_dataframe(df_template)
        gb.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = False, rowDragMultiRow=True, editable=True)

        gb.configure_column('Lugar', type=['textColumn'], editable=True,
            cellEditor='agRichSelectCellEditor',
            cellEditorParams={'values':[""]+ list_activitiess },
            cellEditorPopup=True,
            rowDrag = True,
            rowDragEntireRow = True,
            rowDragManaged = True
        )

        gb.configure_grid_options(enableRangeSelection=True, rowDragManaged = True, onRowDragEnd = onRowDragEnd, deltaRowDataMode = True, getRowNodeId = getRowNodeId, onGridReady = onGridReady, animateRows = True, onRowDragMove = onRowDragMove)


        response = AgGrid(
            df_template,
            gridOptions=gb.build(),
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme = "light"  # or ['streamlit', 'light', 'dark', 'blue', 'fresh', 'material']
        )
        
        # response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
        st.form_submit_button("Save")
    


    # st.write(response['data']) 
    df= pd.DataFrame(response['data'])
    # limpiar de valores vacios
    df = df[df['Lugar'].astype(bool)]

        
        
        
    contador = len(df.index)
    st.session_state.contador = contador
    if contador >= 1:
        
        st.session_state.destino_1 = df.iloc[0,0]
        st.session_state.dias_1 = df.iloc[0,1]
    if contador >= 2:
        
        st.session_state.destino_2 = df.iloc[1,0]
        st.session_state.dias_2 = df.iloc[1,1]
    if contador >= 3:
        st.session_state.destino_3 = df.iloc[2,0]
        st.session_state.dias_3 = df.iloc[2,1]
    if contador >= 4:
        st.session_state.destino_4 = df.iloc[3,0]
        st.session_state.dias_4 = df.iloc[3,1]
    if contador >= 5:
        st.session_state.destino_5 = df.iloc[4,0]
        st.session_state.dias_5 = df.iloc[4,1]
    if contador >= 6:
        st.session_state.destino_6 = df.iloc[5,0]
        st.session_state.dias_6 = df.iloc[5,1]
    
    ##############################
    # Data for Activities & Transportation
    ##############################
    # if st.session_state.contador == 2:
    #     st.info("Please complete the Itinerary section")
    #     st.stop()
    st.title("Activities & Transportation")
    # st.write(st.session_state)   
    lugares=[]
    numeros=[]
    for i in range(1, st.session_state.contador+1):
        lugares.append(st.session_state[f"destino_{i}"])
        numeros.append(st.session_state[f"dias_{i}"])
        
    data_act = pd.DataFrame({"Lugar": lugares, "Dias": numeros})
    # st.table(data_act)


    # Cargar los datos para que se guarden en el cache de sesion_state
    destinos = ["Lima","Cusco","Arequipa","Madre de Dios","Ica"]
    #  I use this https://datagy.io/pandas-add-row/#:~:text=Age%2C%20and%20Location.-,Add%20a%20Row%20to%20a%20Pandas%20DataFrame,the%20Pandas%20concat()%20function.
    def creation_dataframe_by_days(df):
        # Inserting a Row at a Specific Index
        # if we have current indices from 0-3 and we want to insert a new row at index 2, we can simply assign it using index 1.5.
        df['Dias'] = df['Dias'].astype(int)
        valores = df["Dias"].sum() 
        df.loc[valores+1, "Dias"] = 1 
        # se aumenta en 1 para que el ultimo dia no se mantenga en 0 y se incluya actividades 
        # el orden del codigo es muy importante
        for x in range(0,valores):
            if df.loc[x,"Dias"] > 1:
                
                df.loc[x+0.5] = [df.loc[x,"Lugar"],int(df.loc[x,"Dias"]-1)]
                df = df.sort_index().reset_index(drop=True)
                df["Dias"].loc[x] = int(1)
            
        return df
    data_limpia= creation_dataframe_by_days(data_act)
    data_limpia['Dias'] = data_limpia['Dias'].astype(int)
    # st.table(data_limpia)

    # with st.form('my_form_2'):

    # st.write(data_limpia.loc[1,"Lugar"])
    # Obtener datos para los dias segun donde este el pasajero
    diccionario={}
    valores = len(data_limpia.index)
    for value in range(0,valores):
        if int(data_limpia.loc[value,"Dias"]) == 0:
            diccionario[value]=[data_limpia.loc[value,"Lugar"],data_limpia.loc[value+1,"Lugar"]]
            
            
            if int(data_limpia.loc[value+1,"Dias"]) == 0:
                diccionario[value] = [data_limpia.loc[value,"Lugar"],data_limpia.loc[value+1,"Lugar"],data_limpia.loc[value+2,"Lugar"]]
        else:
            diccionario[value]=[data_limpia.loc[value,"Lugar"]]

        
        
    # st.write("diccionario")
    # st.write(diccionario)


    #  Se refinan los datos para que no se repitan los lugares
    new_dicc={}
    new_dicc[0]=diccionario[0]
    for value in range(1,len(diccionario)):
        
        if len(diccionario[value-1])==1:
            new_dicc[value]=diccionario[value]
        if len(diccionario[value-1])>=2:
            continue
    # st.write("segundo")
    # st.write(new_dicc)

    # Lista de listas  con los lugares segun los dias que se encuentre el pasajero en cada lugar
    final_data=list(new_dicc.values())
    # Final es la lista de listas completamente limpia, sin repetidos
    final =[]

    for  value in final_data:
        myset = set(value)
        new = list(myset)
        # Before append data we need drop NaN values to avoid errors
        new = [x for x in new if str(x) != 'nan']
        final.append(new)

    # st.write(final)

    # Base de datos para  las actividades y transportes segun el lugar en el que se encuentre el pasajero 

    data_general ={"Cusco" : ["City Tour Cusco", "Tour Valle Sagrado","Transfer Aeropuerto - Cusco"],
                "Lima":["City Tour Lima","Transfer Aeropuerto - Lima"],
                "Arequipa": ["City Tour Arequipa","Tour Colca"],
                "Madre de Dios": [ "City Tour Puerto Maldonado","Tour Tambopata"],
                "Ica": ["City Tour Ica","Transfer Aeropuerto - Ica"]}

    precios_adultos = {
                       "Transfer Aeropuerto - Cusco": [0,50,100,150,200,250],
                       "City Tour Cusco":[0,25,50,75,100,125],
                       "Tour Valle Sagrado" :[0,80,160,240,320,400],
                       "Transfer Aeropuerto - Lima": [0,100,200,300,400,500],
                       "City Tour Lima":[0,120,240,360,480,600],
                       "City Tour Arequipa":[0,45,55,65,75,85],
                       "Tour Colca":[0,80,160,240,320,400],
                       "City Tour Puerto Maldonado":[0,150,300,450,600,750],
                       "Tour Tambopata":[0,200,400,600,800,1000],
                       "City Tour Ica":[0,42,84,126,168,210],
                       "Transfer Aeropuerto - Ica":[0,31,62,93,124,155]
              }
    precios_niños = {
                       "Transfer Aeropuerto - Cusco": [0,50,100,150,200,250],
                       "City Tour Cusco":[0,25,50,75,100,125],
                       "Tour Valle Sagrado" :[0,80,160,240,320,400],
                       "Transfer Aeropuerto - Lima": [0,100,200,300,400,500],
                       "City Tour Lima":[0,120,240,360,480,600],
                       "City Tour Arequipa":[0,45,55,65,75,85],
                       "Tour Colca":[0,80,160,240,320,400],
                       "City Tour Puerto Maldonado":[0,150,300,450,600,750],
                       "Tour Tambopata":[0,200,400,600,800,1000],
                       "City Tour Ica":[0,42,84,126,168,210],
                       "Transfer Aeropuerto - Ica":[0,31,62,93,124,155]
              }

    # The most tiny image in blank.png is 1x1 pixels
    blank_image = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="

    image = {0:"data:image/svg+xml;charset=utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%3E%3C/svg%3E",
            "City Tour Lima":'https://denomades.s3.us-west-2.amazonaws.com/blog/wp-content/uploads/2020/08/30162219/lima-peru-shutterstock_1047718252.jpg',
            "City Tour Cusco":"https://cms.valenciatravelcusco.com/media/images/package/city-tour-cusco_wmMCcD1.jpg",
            "Tour Valle Sagrado":"https://d3tf9yuhsp2bpn.cloudfront.net/tour_valle_sagrado_de_los_incas_tu_experiencia_120190627120604.jpg",
            "City Tour Arequipa":"https://www.inkasdestination.com/wp-content/uploads/2020/04/arequipa-misti.jpg",
            "City Tour Puerto Maldonado":"https://chullostravelperu.com/wp-content/uploads/2020/03/plaza-de-armas-de-puerto-maldonado.jpg",
            "City Tour Ica":"https://perudestinoseguro.com/wp-content/uploads/2021/12/Plaza_de_Armas_Lima-800x600.jpg",
            "Transfer Aeropuerto - Cusco":"https://www.cuscoairporttransport.com/es/wp-content/uploads/2019/10/transfers-cusco.jpg",
            "Transfer Aeropuerto - Lima":"https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1b/4e/e3/55/caption.jpg?w=500&h=400&s=1",
            "Tour Colca":"https://perumistikatravel.com/wp-content/uploads/2015/10/valle-colca.jpg",
            "Tour Tambopata":"https://www.raptravel.org/imagenes/tour-tambopata-peru-2dias.jpg",
            "Transfer Aeropuerto - Ica":"https://live.staticflickr.com/850/42981524855_db834f169f_b.jpg"}
    
    
    
    # "" is the better way to create a blank string in html
    textos = {0:"  ",
            "City Tour Lima":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "City Tour Cusco":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Tour Valle Sagrado":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "City Tour Arequipa":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "City Tour Puerto Maldonado":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "City Tour Ica":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Transfer Aeropuerto - Cusco":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Transfer Aeropuerto - Lima":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Tour Colca":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Tour Tambopata":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas).",
            "Transfer Aeropuerto - Ica":"La ciudad del Cusco fue el centro urbano más importante del Imperio del Tahuantinsuyo, fundada por el Inca Manco Cápac, y conformaba de palacios, templos ycanchas (viviendas)."}


    titulos = {0:"",
            "City Tour Lima":"City Tour Lima",
            "City Tour Cusco":"City Tour Cusco",
            "Tour Valle Sagrado":"Tour Valle Sagrado",
            "City Tour Arequipa":"City Tour Arequipa",
            "City Tour Puerto Maldonado":"City Tour Puerto Maldonado",
            "City Tour Ica":"City Tour Ica",
            "Transfer Aeropuerto - Cusco":"Transfer Aeropuerto - Cusco",
            "Transfer Aeropuerto - Lima":"Transfer Aeropuerto - Lima",
            "Tour Colca":"Tour Colca",
            "Tour Tambopata":"Tour Tambopata",
            "Transfer Aeropuerto - Ica":"Transfer Aeropuerto - Ica"}

    

    # Actualización de la varibla values total
    values_total = len(final)

    # crear los items para elegir las actividades y transportes
    # se han cargado valores para 7 dias de programa como máximo
    col1,col2 =st.columns([1,2])
    act_1 =[]
    act_2 = []
    act_3 = []
    act_4 = []
    act_5 = []
    act_6 = []
    
    if values_total >=1:
        col1.header("Day 1")
        
        if len(final[0]) == 1:
            miau = col1.multiselect("Select the places", destinos, key="miau", default=[final[0][0]])
        if len(final[0]) == 2:
            miau = col1.multiselect("Select the places", destinos, key="miau", default=[final[0][0],final[0][1]])
        if len(final[0]) == 3:
            miau = col1.multiselect("Select the places", destinos, key="miau", default=[final[0][0],final[0][1],final[0][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_1 = st.multiselect("Select", data_general[miau[0]], key="act_1")    
        if cantidad == 2:
            act_1 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_1")
        if cantidad == 3:
            act_1 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_1")
        
        for x in act_1:
            with st.container():
                
                st.subheader(x)
                
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Peruvian Sunrise', width=250)
                
        
        st.markdown("""---""")
        
    col3,col4 =st.columns([1,2])
    if values_total >=2:
        col3.header("Day 2")
        
        if len(final[1]) == 1:
            miau = col3.multiselect("Select the places", destinos, key="miau1", default=[final[1][0]])
        if len(final[1]) == 2:
            miau = col3.multiselect("Select the places", destinos, key="miau1", default=[final[1][0],final[1][1]])
        if len(final[1]) == 3:
            miau = col3.multiselect("Select the places", destinos, key="miau1", default=[final[1][0],final[1][1],final[1][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_2 = st.multiselect("Select", data_general[miau[0]], key="act_2")    
        if cantidad == 2:
            act_2 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_2")
        if cantidad == 3:
            act_2 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_2")
        for x in act_2:
            with st.container():
                
                st.subheader(x)
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Sunrise by the mountains', width=250)

        st.markdown("""---""")
    col5,col6 =st.columns([1,2])
    if values_total >=3:
        col5.header("Day 3")
        
        if len(final[2]) == 1:
            miau = col5.multiselect("Select the places", destinos, key="miau2", default=[final[2][0]])
        if len(final[2]) == 2:
            miau = col5.multiselect("Select the places", destinos, key="miau2", default=[final[2][0],final[2][1]])
        if len(final[2]) == 3:
            miau = col5.multiselect("Select the places", destinos, key="miau2", default=[final[2][0],final[2][1],final[2][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_3 = st.multiselect("Select", data_general[miau[0]], key="act_3")    
        if cantidad == 2:
            act_3 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_3")
        if cantidad == 3:
            act_3 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_3")
        for x in act_3:
            with st.container():
                
                st.subheader(x)
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Sunrise by the mountains', width=250)

        st.markdown("""---""")
    col7,col8 =st.columns([1,2])
    if values_total >=4:
        col7.header("Day 4")
        
        if len(final[3]) == 1:
            miau = col7.multiselect("Select the places", destinos, key="miau3", default=[final[3][0]])
        if len(final[3]) == 2:
            miau = col7.multiselect("Select the places", destinos, key="miau3", default=[final[3][0],final[3][1]])
        if len(final[3]) == 3:
            miau = col7.multiselect("Select the places", destinos, key="miau3", default=[final[3][0],final[3][1],final[3][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_4 = st.multiselect("Select", data_general[miau[0]], key="act_4")    
        if cantidad == 2:
            act_4 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_4")
        if cantidad == 3:
            act_4 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_4")
        for x in act_4:
            with st.container():
                
                st.subheader(x)
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Sunrise by the mountains', width=250)
        st.markdown("""---""")
        
        
    col9,col10 =st.columns([1,2])
    if values_total >=5:
        col9.header("Day 5")
        
        if len(final[4]) == 1:
            miau = col9.multiselect("Select the places", destinos, key="miau4", default=[final[4][0]])
        if len(final[4]) == 2:
            miau = col9.multiselect("Select the places", destinos, key="miau4", default=[final[4][0],final[4][1]])
        if len(final[4]) == 3:
            miau = col9.multiselect("Select the places", destinos, key="miau4", default=[final[4][0],final[4][1],final[4][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_5 = st.multiselect("Select", data_general[miau[0]], key="act_5")    
        if cantidad == 2:
            act_5 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_5")
        if cantidad == 3:
            act_5 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_5")
        for x in act_5:
            with st.container():
                
                st.subheader(x)
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Sunrise by the mountains', width=250)
        st.markdown("""---""")
    
    col11,col12 =st.columns([1,2])
    if values_total >=6:
        col11.header("Day 6")
        
        if len(final[5]) == 1:
            miau = col11.multiselect("Select the places", destinos, key="miau5", default=[final[5][0]])
        if len(final[5]) == 2:
            miau = col11.multiselect("Select the places", destinos, key="miau5", default=[final[5][0],final[5][1]])
        if len(final[5]) == 3:
            miau = col11.multiselect("Select the places", destinos, key="miau5", default=[final[5][0],final[5][1],final[5][2]])
        
        cantidad = len(miau)
        if cantidad == 1:
            act_6 = st.multiselect("Select", data_general[miau[0]], key="act_6")    
        if cantidad == 2:
            act_6 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] , key="act_6")
        if cantidad == 3:
            act_6 = st.multiselect("Select", data_general[miau[0]] + data_general[miau[1]] + data_general[miau[2]] , key="act_6")
        for x in act_6:
            with st.container():
                
                st.subheader(x)
                col_1, col_2 = st.columns([3,2])
                col_1.markdown(f'**{precios_adultos[x][st.session_state.adultos]} USD adultos  -  {int((precios_adultos[x][st.session_state.niños])//2.5)} USD niños**')
                col_1.write("Lima es la ciudad capital de la República del Perú. Se encuentra situada en la costa central del país, a orillas del océano Pacífico, conformando una extensa y populosa área urbana conocida como Lima Metropolitana, flanqueada por el desierto costero y extendida sobre los valles de los ríos Chillón, Rímac y Lurín.")
                col_2.image(image[x], caption='Sunrise by the mountains', width=250)
        st.markdown("""---""")
        
        
    st.title("Accommodations")
    
    st.title("Pricing")
    # 
    
    
    # obtener una lista de los destinos seleccionados [['tour', 'city', 0, 0, 0], ['cusco', 'tour', 0, 0, 0], [0, 0, 0, 0, 0]]
    dias_totales=[act_1,act_2,act_3,act_4,act_5,act_6]
    
    new=[]
    for a in dias_totales:
        a = a + [0]*(4 - len(a))
        new.append(a)
    
    # calcular el precio total
    precio_total = 0
    union_de_precios=act_1+act_2+act_3+act_4+act_5+act_6
    for x in union_de_precios:
        precio_total += precios_adultos[x][st.session_state.adultos] + int((precios_niños[x][st.session_state.niños])//2.5)
    
    
    # obtener las ciudades seleccionadas  unicas
    ciudades = set(df["Lugar"])
    ciudades = list(ciudades)
    # st.write(ciudades)
    
    left, right = st.columns(2)
    
    # form = left.form("template_form")
    student = ciudades
    cantidad = len(student)


    if cantidad > 0:
        a=student[0]
        if cantidad > 1:
            b=student[1]
            if cantidad > 2:
                c=student[2]
                if cantidad > 3:
                    d=student[3]
                    if cantidad > 4:
                        e=student[4]
    
    
    price = left.write(f"**The  price is  {precio_total} USD**")
    markup = left.slider("Markup",20 ,100,20,key = "markup")
    precio_final = round(precio_total + (precio_total*markup)/100,2)
    price_final = left.write(f"**The profit is  {round(precio_final-precio_total,2)} USD**")
    price_final = left.write(f"**The final price is  {precio_final} USD**")
    # submit = form.form_submit_button("Generar")

    




    imagenes ={ "Lima": ["https://www.hajosiewer.de/wp-content/uploads/Paraglider-an-der-K%C3%BCste-von-Lima.jpg","https://d26gc54f207k5x.cloudfront.net/media/public/cache/800x800/2019/02/14/peru-lima-plaza.jpeg","https://d13d0f5of5vzfo.cloudfront.net/images/products/8a0092ff7b3ad211017b720ac8694fab/large_AdobeStock_107539601_lindrik_online_800x600.jpg"],
            "Cusco":["https://www.perurail.com/wp-content/uploads/2020/11/Machu-Picchu-la-Ciudadela-Inca.jpg","https://turismoi.pe/uploads/city/image/20775/large_cusco.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZn0aeL4sYldq2gH0mA7Q_Rn_xVdy23YQRJw&usqp=CAU"],
            "Arequipa":["https://perumin.com/perumin34/assets/uploads/images/4135c-foto-arequipa.jpg","https://thumbs.dreamstime.com/b/stratovolcano-el-misti-arequipa-per%C3%BA-40716272.jpg","https://bananomeridiano.com/wp-content/uploads/2019/06/que-ver-en-arequipa-plaza-de-armas.jpg"],
            "Madre de Dios":["https://cdn.getyourguide.com/img/location/5df35b210202a.jpeg/70.jpg","https://lp-cms-production.imgix.net/2021-04/shutterstockRF_1021961164.jpg","https://www.sandovallake.com/wp-content/uploads/2019/06/canopy-tours-sandoval-lake-reserve-2.jpg"],
            "Ica":["https://turismoi.pe/uploads/photo/photo_file/29473/optimized_1195__5_.jpg","https://viajesica.com/wp-content/uploads/2019/02/nascafoto1.jpg","https://media.tacdn.com/media/attractions-splice-spp-674x446/0a/93/05/49.jpg"]}

    
    
    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    
    ##############################
    #? Creacion de las opciones de portada para la impresion
    ##############################

    with st.sidebar:
        # Make folder for storing user uploads
        
        destination_folder = Path('downloads')
        destination_folder.mkdir(exist_ok=True, parents=True)
        def merge_pdfs(pdf_path):
            #! This is used to pre uploaded pdf to the app 
            with open(pdf_path, "rb") as pdf_file:
                data_2 = base64.b64encode(pdf_file.read())
                return data_2
            #! Fin
        with st.expander("Styling your Program", expanded=True):
            data_2="ok"
            if lenguage=="English":
                
                st.image("imagenes/1a.png", width=200)
                option_1a = st.checkbox("Select", key="1a")
                st.image("imagenes/2a.png", width=200)
                
                option_2a = st.checkbox("Select", key="2a")
                
                if option_1a:
                    data_2 = merge_pdfs("imagenes/1.pdf")
                    
                if option_2a:
                    data_2 = merge_pdfs("imagenes/2.pdf")   
                if data_2==None:
                    st.stop()
            if lenguage=="Spanish":
                
                st.image("imagenes/3a.png", width=200)
                option_3a = st.checkbox("Select", key="3a")
                st.image("imagenes/4a.png", width=200)
                option_4a = st.checkbox("Select", key="4a")
                
                if option_3a:
                    data_2 = merge_pdfs("imagenes/3.pdf")
                    
                if option_4a:
                    data_2 = merge_pdfs("imagenes/4.pdf")  
                if data_2==None:
                    st.stop()
            if lenguage=="Deutsch":
                
                st.image("imagenes/5a.png", width=200)
                option_5a = st.checkbox("Select", key="5a")
                st.image("imagenes/6a.png", width=200)
                
                option_6a = st.checkbox("Select", key="6a")
                
                if option_5a:
                    data_2 = merge_pdfs("imagenes/5.pdf")
                    
                if option_6a:
                    data_2 = merge_pdfs("imagenes/6.pdf")  
                if data_2==None:
                    st.stop()
            if data_2!="ok":
                # Defines what options are in the form
                class PDFMergeRequest(BaseModel):
                    pdf_uploads: Optional[List[FileContent]] = Field(
                        data_2,
                        alias="PDF Files to Merge",
                        description="PDF that needs to be merged",
                    )
                pdf_output = '.pdf'
                output_suffix = '.pdf'
                merge = 'Merge Multiple PDFs into One'
                split = 'Split One PDF into Multiple'
                view_choice = merge 
                if view_choice == merge:
                    # Get the data from the form, stop running if user hasn't submitted pdfs yet
                    data = sp.pydantic_form(key="pdf_merge_form", model=PDFMergeRequest )
                    #! If you want to use the app without the opcion of pre upload pdf, just put the next value this in 2 and not in 1
                    if data is None or data.pdf_uploads is None or len(data.pdf_uploads) < 1:
                        st.warning("Please, upload at least 1 PDFs and press Submit")
                        st.stop()
                    data.pdf_uploads.insert(0,data_2)
                    # st.write(data.pdf_uploads)
                    
                    # Save Uploaded PDFs
                    uploaded_paths = []
                    for pdf_data in data.pdf_uploads:
                        try:
                            input_pdf_path = destination_folder / f"input_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
                            input_pdf_path.write_bytes(pdf_data.as_bytes())
                            uploaded_paths.append(input_pdf_path)
                        #! This is a hack to get around the fact that streamlit_pydantic doesn't support base64 encoded files
                        #! This a piece of code to allow the app to work with a pdf previously uploaded to the app
                        except AttributeError:
                            input_pdf_path.write_bytes(base64.b64decode(pdf_data, validate=True))
                            uploaded_paths.append(input_pdf_path)    
                        #! Fin
                    pdf_writer = PdfFileWriter()
                    for path in uploaded_paths:
                        pdf_reader = PdfFileReader(str(path))
                        for page in range(pdf_reader.getNumPages()):
                            # Add each page to the writer object
                            pdf_writer.addPage(pdf_reader.getPage(page))

                    # Write out the merged PDF
                    output_pdf_path = destination_folder / f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
                    with open(str(output_pdf_path), 'wb') as out:
                        pdf_writer.write(out)
                    output_path = output_pdf_path
                    # Convert to stacked / merged image
                    
                    # Allow download
                    if output_suffix == pdf_output:
                        output_mime = 'application/pdf'
                    st.download_button('Download Merged Document', output_path.read_bytes(), f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}{output_suffix}", mime=output_mime)
    
    st.sidebar.caption("Developed by  [**Fidel Ramos**](https://vittaquant-ai.com)")
    st.sidebar.caption("**VittaQuant Technologies**")
    st.sidebar.markdown('##')  
    #######################
    # FIN
    #######################




    if st.button("Generar"):
        if cantidad == 1:
            template = env.get_template("templates/sample_1.html")
            html = template.render(
                student=student,
                a=a,
                gatitos = content,
                imag_1a = imagenes[a][0],
                imag_2a = imagenes[a][1],
                imag_3a = imagenes[a][2],
                activ_1a = image[new[0][0]],
                activ_2a = image[new[0][1]],
                activ_3a = image[new[0][2]],
                activ_4a = image[new[0][3]],
                activ_5a = image[new[1][0]],
                activ_6a = image[new[1][1]],
                activ_7a = image[new[1][2]],
                activ_8a = image[new[1][3]],
                activ_9a = image[new[2][0]],
                activ_10a = image[new[2][1]],
                activ_11a = image[new[2][2]],
                activ_12a = image[new[2][3]],
                activ_13a = image[new[3][0]],
                activ_14a = image[new[3][1]],
                activ_15a = image[new[3][2]],
                activ_16a = image[new[3][3]],
                activ_17a = image[new[4][0]],
                activ_18a = image[new[4][1]],
                activ_19a = image[new[4][2]],
                activ_20a = image[new[4][3]],
                activ_21a = image[new[5][0]],
                activ_22a = image[new[5][1]],
                activ_23a = image[new[5][2]],
                activ_24a = image[new[5][3]],
                parrafo_1a = textos[new[0][0]],
                parrafo_2a = textos[new[0][1]],
                parrafo_3a = textos[new[0][2]],
                parrafo_4a = textos[new[0][3]],
                parrafo_5a = textos[new[1][0]],
                parrafo_6a = textos[new[1][1]],
                parrafo_7a = textos[new[1][2]],
                parrafo_8a = textos[new[1][3]],
                parrafo_9a = textos[new[2][0]],
                parrafo_10a = textos[new[2][1]],
                parrafo_11a = textos[new[2][2]],
                parrafo_12a = textos[new[2][3]],
                parrafo_13a = textos[new[3][0]],
                parrafo_14a = textos[new[3][1]],
                parrafo_15a = textos[new[3][2]],
                parrafo_16a = textos[new[3][3]],
                parrafo_17a = textos[new[4][0]],
                parrafo_18a = textos[new[4][1]],
                parrafo_19a = textos[new[4][2]],
                parrafo_20a = textos[new[4][3]],
                parrafo_21a = textos[new[5][0]],
                parrafo_22a = textos[new[5][1]],
                parrafo_23a = textos[new[5][2]],
                parrafo_24a = textos[new[5][3]],
                titulo_1a = titulos[new[0][0]],
                titulo_2a = titulos[new[0][1]],
                titulo_3a = titulos[new[0][2]],
                titulo_4a = titulos[new[0][3]],
                titulo_5a = titulos[new[1][0]],
                titulo_6a = titulos[new[1][1]],
                titulo_7a = titulos[new[1][2]],
                titulo_8a = titulos[new[1][3]],
                titulo_9a = titulos[new[2][0]],
                titulo_10a = titulos[new[2][1]],
                titulo_11a = titulos[new[2][2]],
                titulo_12a = titulos[new[2][3]],
                titulo_13a = titulos[new[3][0]],
                titulo_14a = titulos[new[3][1]],
                titulo_15a = titulos[new[3][2]],
                titulo_16a = titulos[new[3][3]],
                titulo_17a = titulos[new[4][0]],
                titulo_18a = titulos[new[4][1]],
                titulo_19a = titulos[new[4][2]],
                titulo_20a = titulos[new[4][3]],
                titulo_21a = titulos[new[5][0]],
                titulo_22a = titulos[new[5][1]],
                titulo_23a = titulos[new[5][2]],
                titulo_24a = titulos[new[5][3]],
                
                date=date.today().strftime("%B %d, %Y"),
                price=f"The total price is {precio_final} USD"
            )
        if cantidad == 2:
            
            template = env.get_template("templates/sample_2.html")
            html = template.render(
                student=student,
                a=a,
                imag_1a = imagenes[a][0],
                imag_2a = imagenes[a][1],
                imag_3a = imagenes[a][2],
                b=b,
                imag_1b = imagenes[b][0],
                imag_2b = imagenes[b][1],
                imag_3b = imagenes[b][2],
                
            
                date=date.today().strftime("%B %d, %Y"),
                price=f"The total price is {precio_final} USD"
            )
        if cantidad == 3:
            template = env.get_template("templates/sample_3.html")
            html = template.render(
                student=student,
                a=a,
                imag_1a = imagenes[a][0],
                imag_2a = imagenes[a][1],
                imag_3a = imagenes[a][2],
                b=b,
                imag_1b = imagenes[b][0],
                imag_2b = imagenes[b][1],
                imag_3b = imagenes[b][2],
                c=c,
                imag_1c = imagenes[c][0],
                imag_2c = imagenes[c][1],
                imag_3c = imagenes[c][2],
                
                
                date=date.today().strftime("%B %d, %Y"),
                price=f"The total price is {precio_final} USD"
            )
        if cantidad == 4:
            template = env.get_template("templates/sample_4.html")
            html = template.render(
                student=student,
                a=a,
                imag_1a = imagenes[a][0],
                imag_2a = imagenes[a][1],
                imag_3a = imagenes[a][2],
                b=b,
                imag_1b = imagenes[b][0],
                imag_2b = imagenes[b][1],
                imag_3b = imagenes[b][2],
                c=c,
                imag_1c = imagenes[c][0],
                imag_2c = imagenes[c][1],
                imag_3c = imagenes[c][2],
                d = d,
                imag_1d = imagenes[d][0],
                imag_2d = imagenes[d][1],
                imag_3d = imagenes[d][2],
                
                
                
                
                
                # grade=f"{grade} soles",#grade=f"{grade}/100",
                date=date.today().strftime("%B %d, %Y"),
                price=f"The total price is {precio_final} USD"
            )
        if cantidad == 5:
            template = env.get_template("templates/sample_5.html")
            html = template.render(
                student=student,
                a=a,
                imag_1a = imagenes[a][0],
                imag_2a = imagenes[a][1],
                imag_3a = imagenes[a][2],
                b=b,
                imag_1b = imagenes[b][0],
                imag_2b = imagenes[b][1],
                imag_3b = imagenes[b][2],
                c=c,
                imag_1c = imagenes[c][0],
                imag_2c = imagenes[c][1],
                imag_3c = imagenes[c][2],
                d = d,
                imag_1d = imagenes[d][0],
                imag_2d = imagenes[d][1],
                imag_3d = imagenes[d][2],
                e = e,
                imag_1e = imagenes[e][0],
                imag_2e = imagenes[e][1],
                imag_3e = imagenes[e][2],
                 
                 
                 
                # grade=f"{grade} soles",#grade=f"{grade}/100",
                date=date.today().strftime("%B %d, %Y"),
                price=f"The total price is {precio_final} USD"
            )
            
            
        # 2 rows  DELETE  to work in Windows-------------------
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdf=pdfkit.from_string(html, False, configuration=config, css='sample.css')
        
        # 1 row  to put the app in cloud ----------------------
        #pdf = pdfkit.from_string(html, False, css='sample.css')
        #Point pdfkit configuration to wkhtmltopdf.exe
        # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        # pdf = pdfkit.from_string(html, False, configuration=config, css='sample.css')
        
        
        
        #Convert HTML file to PDF
        # pdf = pdfkit.from_file(path_to_file, output_path='peruvian.pdf', configuration=config, css='sample.css')

        right.success("El programa se generó exitosamente")
        # st.write(html, unsafe_allow_html=True)
        # st.write("")
        supremo =right.download_button(
                "⬇️ Download PDF",
                data=pdf,
                file_name="Programa.pdf",
                mime="application/octet-stream",
                )
        # obtener el valor de renderes de pdf  y luego  mostrarlo para descargar de forma inmediata dependiendo 
        # del usuario



if menu_sidebar == "Templates":
    st.info("Estamos trabajando en ello")
    
if menu_sidebar == "Save this program":
    st.info("Estamos trabajando en ello")
    
if menu_sidebar == "Data":
    # create menu to edit values
    bucket_name = "peruviansunrise-storage"
    menu = option_menu(None, ["Bundle","Location","Activities","Transportation","Accommodations"], 
        icons=['stack','geo-alt-fill', 'binoculars-fill',"tag-fill" ,"moon-stars-fill"], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#212529", "font-size": "20px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ffc300"},
        }
        )
    
        
    if menu == "Activities":
        
        activities_option = st.sidebar.radio("Option",["Create new","Edit","Delete"], key="activities_options")
        
        if activities_option == "Edit":
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["activities"]
            data = collection.find({},{"Name_en":1, "Operator":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"] + " (" + value["Operator"]+ ")")
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad = st.selectbox("Choose the activity",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            
            
            st.subheader("Edit the activity")
            title = st.text_input("Title in English",complete_data["Name_en"])
            title_de = st.text_input("Title in German",complete_data["Name_de"])
            title_es = st.text_input("Title in Spanish", complete_data["Name_es"])
            
            # lista de las locations
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            
            sep1,sep2, sep3 =st.columns(3)
            operator =sep1.text_input("Operator", complete_data["Operator"])
            email = sep2.text_input("Email", complete_data["Email"])
            locations = sep3.multiselect("Choose the locations",list_activities, default=complete_data["Location"])
            if len(locations)==0:
                st.stop()
            
        
            description = st.text_area("Description in English", complete_data["Description_en"])
            description_de = st.text_area("Description in  German", complete_data["Description_de"])
            description_es = st.text_area("Description in Spanish", complete_data["Description_es"])

            st.subheader("Images")
            c1, c2, c3 = st.columns(3)
        
            bucket_name = "peruviansunrise-storage"
            
            url_1 = get_link(bucket_name, complete_data["Images"]["1"])
            url_2 = get_link(bucket_name, complete_data["Images"]["2"])
            url_3 = get_link(bucket_name, complete_data["Images"]["3"])
            
            # if url_1 is not None:
            #     response = requests.get(url_1)
            # if url_2 is not None:
            #     response = requests.get(url_2)
            # if url_3 is not None:
            #     response = requests.get(url_3)
            

            c1.image(resize_image(url_1))
            c2.image(resize_image(url_2))
            c3.image(resize_image(url_3))
            

            with st.container():
                col1, col2, col3 = st.columns(3)
                file_1 = col1.file_uploader("Replace the image", key="1_change")
                file_2 = col2.file_uploader("Replace the image", key="2_change")
                file_3 = col3.file_uploader("Replace the image", key="3_change")
                
                if file_1 is not None:
                    col1.subheader("The new image")
                    col1.image(file_1, use_column_width="auto")
                    
                
                if file_2 is not None:
                    col2.subheader("The new image")
                    col2.image(file_2, use_column_width="auto")
                    url_2 = file_2
                
                if file_3 is not None:
                    col3.subheader("The new image")
                    col3.image(file_3, use_column_width="auto")
                    url_3 = file_3
                
            
                @st.cache()
                def get_data(filas):
                    incluir = np.arange(1,filas+1)
                    values = [0]*(filas)
                    df = pd.DataFrame(
                        {"Amount of People": incluir,"Price Adults":values,"Price Kids":values}
                    )
                    return df
                
                def get_data_b(filas, adult_prices, kid_prices):
                    
                    incluir = np.arange(1,filas+1)
                    cantidad_filas_data = len(adult_prices)
                    values_1 = adult_prices + [0]*(filas-cantidad_filas_data)
                    values_2 = kid_prices + [0]*(filas-cantidad_filas_data)
                    
                    df = pd.DataFrame(
                        {"Amount of People": incluir,"Price Adults":values_1,"Price Kids":values_2}
                    )
                    return df
                    
                st.subheader("Prices")
                
                
                lista = [complete_data["Fixed_price"],complete_data["Price_kid_and_adult"]]  
                indice=0
                for x in lista:
                    if x!=False:
                        break
                    indice+=1
                    
                elegir_precio = st.radio("Choose the price",["Fixed Price","Adults and Kids"],horizontal=True, index=indice)
                precios_fijos = False
                precios_adultos = False
                precios_kids = False
                
                
                col1,col2 = st.columns([2,1])
                if elegir_precio == "Fixed Price" and complete_data["Fixed_price"]==False:
                    precios_fijos = col1.number_input("Price", key="price_fixed")
                if elegir_precio == "Fixed Price" and complete_data["Fixed_price"]!=False:
                    precios_fijos = col1.number_input("Price", key="price_fixed_1",value=complete_data["Fixed_price"], step=1)
                
                
                
                if elegir_precio == "Adults and Kids" and complete_data["Price_kid_and_adult"]==False:
                    with col1:
                        st.subheader("Prices to adults and kids")
                        numero_filas_k = st.slider("Number of people",1,15,step=1, value=5, key="adults_kids_slider")
                        
                        data_k = get_data(numero_filas_k)
                        gb_k = GridOptionsBuilder.from_dataframe(data_k)
                        #make all columns editable
                        gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                        go_k = gb_k.build()
                        
                        ag_k = AgGrid(
                            data_k, 
                            gridOptions=go_k, 
                            # height=300, 
                            fit_columns_on_grid_load=True,
                            theme= "light" # or "streamlit","light","balham","material"
                        )
                        # st.subheader("Returned Data")
                        # st.dataframe(ag_k['data'])
                        
                        df_prices_kids = ag_k["data"]
                        # st.dataframe(ag['data'])
                        df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                        df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                        df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                        
                        df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                        df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                        df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                        precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                        # st.write(precios_kids)
                        
                if elegir_precio == "Adults and Kids" and complete_data["Price_kid_and_adult"]!=False:
                    with col1:
                        st.subheader("Prices to adults and kids")
                        elementos_data = len(complete_data["Price_kid_and_adult"][1])
                        numero_filas_k = st.slider("Number of people",elementos_data,15,step=1, value=elementos_data, key="adults_kids_slider")
                        
                        data_k = get_data_b(numero_filas_k, complete_data["Price_kid_and_adult"][1], complete_data["Price_kid_and_adult"][2])
                        gb_k = GridOptionsBuilder.from_dataframe(data_k)
                        #make all columns editable
                        gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                        go_k = gb_k.build()
                        
                        ag_k = AgGrid(
                            data_k, 
                            gridOptions=go_k, 
                            # height=300, 
                            fit_columns_on_grid_load=True,
                            theme= "light" # or "streamlit","light","balham","material"
                        )
                        # st.subheader("Returned Data")
                        # st.dataframe(ag_k['data'])
                        
                        df_prices_kids = ag_k["data"]
                        # st.dataframe(ag['data'])
                        df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                        df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                        df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                        
                        df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                        df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                        df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                        precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                        # st.write(precios_kids)
                
                st.subheader("Meals included")
                cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
                breakfast = cole1.checkbox('Breakfast', value=complete_data["breakfast"])
                lunch = cole2.checkbox('Lunch', value=complete_data["lunch"])
                dinner = cole3.checkbox('Dinner', value=complete_data["dinner"])
                other = cole4.checkbox('Other (please describe in meal notes)', value=complete_data["other"])
                st.subheader("Meal notes")
                as1,as2,as3 =st.columns([1,1,1])
                
                notes_en = as1.text_area("English", value=complete_data["notes_en"])
                notes_de = as2.text_area("Deutsch", value=complete_data["notes_de"])
                notes_es = as3.text_area("Spanish", value=complete_data["notes_es"])
                st.subheader("Internal Pricing Notes (not shown to the traveler)")
                notes_precio = st.text_area("Internal Pricing Notes", value=complete_data["notes_precio"])

            
                
                st.subheader("Save changes")
                subir = st.button('Save data')
                if subir:
                    # reemplazar los espacios por guiones bajos
                    if complete_data["Name_en"]==title and complete_data["Operator"]==operator:
                        
                        title_separate = title.replace(" ", "_")
                        operator_separate = operator.replace(" ", "_")
                        
                        with st.spinner("Uploading data..."):
                            
                            image_1 = title_separate+"_"+operator_separate+"_1.png"
                            image_2 = title_separate+"_"+operator_separate+"_2.png"
                            image_3 = title_separate+"_"+operator_separate+"_3.png"
                            # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                            
                            if file_1 is not None:
                                uploadimageToS3(file_1,bucket_name , image_1)
                            if file_2 is not None:
                                uploadimageToS3(file_2,bucket_name , image_2)
                            if file_3 is not None:
                                uploadimageToS3(file_3,bucket_name , image_3)
                                
                            ############################
                            # Connection to MongoDB
                            ############################
                            
                            collection = db["activities"]
                            
                            # In this section you can add new activities to the database
                            # Price_adult is [[people],[price]]
                            
                            record = {
                            "Name_en": title, # ingles
                            "Name_de": title_de, # aleman
                            "Name_es": title_es, # español
                            "Description_en": description,
                            "Description_de": description_de,
                            "Description_es": description_es,
                            "Price_kid_and_adult": precios_kids,
                            "Fixed_price": precios_fijos,
                            "Images":{"1": image_1, "2": image_2, "3":image_3},
                            "Operator": operator,
                            "Email": email,
                            "Location": locations,
                            "breakfast": breakfast,
                            "lunch": lunch,
                            "dinner": dinner,
                            "other": other,
                            "notes_en": notes_en,
                            "notes_de": notes_de,
                            "notes_es": notes_es,
                            "notes_precio": notes_precio
                            }
                            
                            collection.update_one({"_id": complete_data["_id"]}, {"$set": record})
                            st.info("Data saved successfully")
                                
                            
                    
                    
                    if complete_data["Name_en"]!=title or complete_data["Operator"]!=operator:
                        
                        antiguas = []
                        for image in complete_data["Images"].values():
                            antiguas.append(image)
                        # for image in complete_data["Images"].values():
                        
                        
                        title_separate = title.replace(" ", "_")
                        operator_separate = operator.replace(" ", "_")
                        
                    
                        with st.spinner('Saving'):
                            
                            image_1 = title_separate+"_"+operator_separate+"_1.png"
                            image_2 = title_separate+"_"+operator_separate+"_2.png"
                            image_3 = title_separate+"_"+operator_separate+"_3.png"
                            
                            copy_and_delete_s3_file(bucket_name,antiguas[0], image_1)
                            copy_and_delete_s3_file(bucket_name,antiguas[1], image_2)
                            copy_and_delete_s3_file(bucket_name,antiguas[2],image_3)
                            
                            delete_s3_file(bucket_name, antiguas[0])
                            delete_s3_file(bucket_name, antiguas[1])
                            delete_s3_file(bucket_name, antiguas[2])
                            # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                            if file_1 is not None:
                                uploadimageToS3(file_1,bucket_name , image_1)
                            if file_2 is not None:
                                uploadimageToS3(file_2,bucket_name , image_2)
                            if file_3 is not None:
                                uploadimageToS3(file_3,bucket_name , image_3)
                                
                            ############################
                            # Connection to MongoDB
                            ############################
                        
                            
                            collection = db["activities"]
                            
                            # In this section you can add new activities to the database
                            # Price_adult is [[people],[price]]
                            
                            record = {
                            "Name_en": title, # ingles
                            "Name_de": title_de, # aleman
                            "Name_es": title_es, # español
                            "Description_en": description,
                            "Description_de": description_de,
                            "Description_es": description_es,
                            "Price_kid_and_adult": precios_kids,
                            "Fixed_price": precios_fijos,
                            "Images":{"1": image_1, "2": image_2, "3":image_3},
                            "Operator": operator,
                            "Email": email,
                            "Location": locations,
                            "breakfast": breakfast,
                            "lunch": lunch,
                            "dinner": dinner,
                            "other": other,
                            "notes_en": notes_en,
                            "notes_de": notes_de,
                            "notes_es": notes_es,
                            "notes_precio": notes_precio
                            }
                            
                            collection.update_one({"_id": complete_data["_id"]}, {"$set": record})
                            st.info("Data saved successfully")
                                
                    
                
        ########################
        # Create a new activity 
        ########################
        if activities_option == "Create new":
            
            st.subheader("Create a new activity")
            title = st.text_input("Title in English")
            title_de = st.text_input("Title in German")
            title_es = st.text_input("Title in Spanish")
            
            # lista de las locations
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])

            # fin
            
            sep1,sep2, sep3 =st.columns(3)
            operator =sep1.text_input("Operator")
            email = sep2.text_input("Email")
            locations = sep3.multiselect("Choose the locations",list_activities)
            if len(locations)==0:
                st.stop()
            
            description = st.text_area("Description in English")
            description_de = st.text_area("Description in  German")
            description_es = st.text_area("Description in Spanish")

            
            st.subheader("Select 3 images ")
            uploaded_files = st.file_uploader("" ,accept_multiple_files=True)
            
            with st.container():
                
                c1, c2, c3 = st.columns(3)
                if len(uploaded_files)==3:
                    c1.image(uploaded_files[0], use_column_width="auto",output_format="PNG")
                    c2.image(uploaded_files[1], use_column_width="auto",output_format="PNG")
                    c3.image(uploaded_files[2], use_column_width="auto",output_format="PNG")
                    
                    
                    @st.cache()
                    def get_data(filas):
                        incluir = np.arange(1,filas+1)
                        values = [0]*(filas)
                        df = pd.DataFrame(
                            {"Amount of People": incluir,"Price Adults":values,"Price Kids":values}
                        )
                        return df
                    
                    st.subheader("Prices")
                    
                    elegir_precio = st.radio("Choose the price",["Fixed Price","Adults and Kids"],horizontal=True)
                    precios_fijos = False
                    
                    precios_kids = False
                    
                    
                    col1,col2 = st.columns([2,1])
                    if elegir_precio == "Fixed Price":
                        precios_fijos = col1.number_input("Price", key="price_fixed" , step=1)
                            
                    if elegir_precio == "Adults and Kids":
                        with col1:
                            st.subheader("Prices to adults and kids")
                            numero_filas_k = st.slider("Number of people",1,15,step=1, value=5, key="adults_kids_slider")
                            
                            data_k = get_data(numero_filas_k)
                            gb_k = GridOptionsBuilder.from_dataframe(data_k)
                            #make all columns editable
                            gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                            go_k = gb_k.build()
                            
                            ag_k = AgGrid(
                                data_k, 
                                gridOptions=go_k, 
                                # height=300, 
                                fit_columns_on_grid_load=True,
                                theme= "light" # or "streamlit","light","balham","material"
                            )
                            # st.subheader("Returned Data")
                            # st.dataframe(ag_k['data'])
                            
                            df_prices_kids = ag_k["data"]
                            # st.dataframe(ag['data'])
                            df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                            df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                            df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                            
                            df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                            df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                            df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                            precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                            # st.write(precios_kids)

                    
                    st.subheader("Meals included")
                    cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
                    breakfast = cole1.checkbox('Breakfast')
                    lunch = cole2.checkbox('Lunch')
                    dinner = cole3.checkbox('Dinner')
                    other = cole4.checkbox('Other (please describe in meal notes)')
                    st.subheader("Meal notes")
                    as1,as2,as3 =st.columns([1,1,1])
                    
                    notes_en = as1.text_area("English")
                    notes_de = as2.text_area("Deutsch")
                    notes_es = as3.text_area("Spanish")
                    st.subheader("Internal Pricing Notes (not shown to the traveler)")
                    notes_precio = st.text_area("Internal Pricing Notes")

                    
                    st.subheader("Upload  data")
                    subir = st.button('Save all data')
                    if subir:
                        # reemplazar los espacios por guiones bajos
                        title_separate = title.replace(" ", "_")
                        operator_separate = operator.replace(" ", "_")
                        with st.spinner('Uploading...'):
                            
                            image_1 = title_separate+"_"+operator_separate+"_1.png"
                            image_2 = title_separate+"_"+operator_separate+"_2.png"
                            image_3 = title_separate+"_"+operator_separate+"_3.png"
                            # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                            uploadimageToS3(uploaded_files[0],bucket_name , image_1)
                            uploadimageToS3(uploaded_files[1],bucket_name , image_2)
                            uploadimageToS3(uploaded_files[2],bucket_name , image_3)
                            ############################
                            # Connection to MongoDB
                            ############################
                        
                            # Connection to MongoDB since applicacion in streamlit cloud
                            # cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")
                            # Connection to MongoDB since applicacion in local
                            # cluster = pymongo.MongoClient("mongodb://localhost:27017/")
                            # db = cluster["peruviansunrise"]
                            
                            collection = db["activities"]
                            
                            # In this section you can add new activities to the database
                            # Price_adult is [[people],[price]]
                            
                            record = {
                            "Name_en": title, # ingles
                            "Name_de": title_de, # aleman
                            "Name_es": title_es, # español
                            "Description_en": description,
                            "Description_de": description_de,
                            "Description_es": description_es,
                            "Price_kid_and_adult": precios_kids,
                            "Fixed_price": precios_fijos,
                            "Images":{"1": image_1, "2": image_2, "3":image_3},
                            "Operator": operator,
                            "Email": email,
                            "Location": locations,
                            "breakfast": breakfast,
                            "lunch": lunch,
                            "dinner": dinner,
                            "other": other,
                            "notes_en": notes_en,
                            "notes_de": notes_de,
                            "notes_es": notes_es,
                            "notes_precio": notes_precio
                            }
                            
                            collection.insert_one(record)
        ########################
        # Delete a activity
        ########################
        if activities_option == "Delete":
            st.subheader("Delete an activity")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["activities"]
            data = collection.find({},{"Name_en":1, "Operator":1,"_id":1})
            names = []
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                names.append(value["Name_en"])
                list_activities.append(value["Name_en"] + "(" + value["Operator"]+ ")")
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad_1 = st.selectbox("Choose the activity",list_activities)
            if elegir_actividad_1 == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad_1)
            code = ids_activities[order_activity]
            
            complete_data = collection.find_one({"_id":code})
            
            
            
            title = st.header(complete_data["Name_en"])
            description = st.write( complete_data["Description_en"])
            
            operator = st.subheader("Operator: "+complete_data["Operator"])
            
            email = st.subheader("Email: "+ complete_data["Email"])
            
            c1, c2, c3 = st.columns(3)
        
            bucket_name = "peruviansunrise-storage"
            
            url_1 = get_link(bucket_name, complete_data["Images"]["1"])
            url_2 = get_link(bucket_name, complete_data["Images"]["2"])
            url_3 = get_link(bucket_name, complete_data["Images"]["3"])
            
            
            c1.image(url_1, use_column_width="auto")
            c2.image(url_2, use_column_width="auto")
            c3.image(url_3, use_column_width="auto")
            with st.container():
                
                
            
                @st.cache()
                def get_data(filas):
                    incluir = np.arange(1,filas+1)
                    values = [0]*(filas)
                    df = pd.DataFrame(
                        {"Amount of People": incluir,"Price Adults":values,"Price Kids":values}
                    )
                    return df
                
                def get_data_b(filas, adult_prices, kid_prices):
                    
                    incluir = np.arange(1,filas+1)
                    cantidad_filas_data = len(adult_prices)
                    values_1 = adult_prices + [0]*(filas-cantidad_filas_data)
                    values_2 = kid_prices + [0]*(filas-cantidad_filas_data)
                    
                    df = pd.DataFrame(
                        {"Amount of People": incluir,"Price Adults":values_1,"Price Kids":values_2}
                    )
                    return df
                    
                st.subheader("Prices")
                
                
                lista = [complete_data["Fixed_price"],complete_data["Price_kid_and_adult"]]  
                indice=0
                for x in lista:
                    if x!=False:
                        break
                    indice+=1
                    
                elegir_precio = st.radio("Choose the price",["Fixed Price","Adults and Kids"],horizontal=True, index=indice)
                precios_fijos = False
                precios_adultos = False
                precios_kids = False
                
                
                col1,col2 = st.columns([2,1])
                if elegir_precio == "Fixed Price" and complete_data["Fixed_price"]==False:
                    precios_fijos = col1.number_input("Price", key="price_fixed")
                if elegir_precio == "Fixed Price" and complete_data["Fixed_price"]!=False:
                    precios_fijos = col1.number_input("Price", key="price_fixed_1",value=complete_data["Fixed_price"])
                
                if elegir_precio == "Adults and Kids" and complete_data["Price_kid_and_adult"]==False:
                    with col1:
                        st.subheader("Prices to adults and kids")
                        numero_filas_k = st.slider("Number of people",1,15,step=1, value=5, key="adults_kids_slider")
                        
                        data_k = get_data(numero_filas_k)
                        gb_k = GridOptionsBuilder.from_dataframe(data_k)
                        #make all columns editable
                        gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                        go_k = gb_k.build()
                        
                        ag_k = AgGrid(
                            data_k, 
                            gridOptions=go_k, 
                            # height=300, 
                            fit_columns_on_grid_load=True,
                            theme= "light" # or "streamlit","light","balham","material"
                        )
                        # st.subheader("Returned Data")
                        # st.dataframe(ag_k['data'])
                        
                        df_prices_kids = ag_k["data"]
                        # st.dataframe(ag['data'])
                        df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                        df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                        df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                        
                        df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                        df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                        df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                        precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                        # st.write(precios_kids)
                        
                if elegir_precio == "Adults and Kids" and complete_data["Price_kid_and_adult"]!=False:
                    with col1:
                        st.subheader("Prices to adults and kids")
                        elementos_data = len(complete_data["Price_kid_and_adult"][1])
                        numero_filas_k = st.slider("Number of people",elementos_data,15,step=1, value=elementos_data, key="adults_kids_slider")
                        
                        data_k = get_data_b(numero_filas_k, complete_data["Price_kid_and_adult"][1], complete_data["Price_kid_and_adult"][2])
                        gb_k = GridOptionsBuilder.from_dataframe(data_k)
                        #make all columns editable
                        gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                        go_k = gb_k.build()
                        
                        ag_k = AgGrid(
                            data_k, 
                            gridOptions=go_k, 
                            # height=300, 
                            fit_columns_on_grid_load=True,
                            theme= "light" # or "streamlit","light","balham","material"
                        )
                        # st.subheader("Returned Data")
                        # st.dataframe(ag_k['data'])
                        
                        df_prices_kids = ag_k["data"]
                        # st.dataframe(ag['data'])
                        df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                        df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                        df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                        
                        df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                        df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                        df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                        precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                        # st.write(precios_kids)
            
            if st.button("Delete all"):
                with st.spinner('Deleting...'):    
                    order_activity = list_activities.index(elegir_actividad_1)
                    code = ids_activities[order_activity]
                    # delete activity in mongodb
                    
                    collection.delete_one({"_id": ObjectId(code)})
                    # ---
                    # delete activity in s3
                    title = complete_data["Name_en"]
                    operator = complete_data["Operator"]
                    
                    title_separate = title.replace(" ", "_")
                    operator_separate = operator.replace(" ", "_")
                    
                    image_1 = title_separate+"_"+operator_separate+"_1.png"
                    image_2 = title_separate+"_"+operator_separate+"_2.png"
                    image_3 = title_separate+"_"+operator_separate+"_3.png"
                    
                    try:
                        delete_s3_file(bucket_name,image_1)
                        delete_s3_file(bucket_name,image_2)
                        delete_s3_file(bucket_name,image_3)
                        st.success("Activity deleted")
                    # ---
                    except: 
                        st.error("Error deleting images")
                        
                    
                        
        
        
    if menu == "Location":
        # mongodb connection 
        collection = db["locations"]
        # fin
        activities_option = st.sidebar.radio("Option",["Create new","Edit","Delete"])
        if activities_option=="Create new":
            st.subheader("Create new location")
            name_en = st.text_input("Name in english")
            name_de = st.text_input("Name in german")
            name_es = st.text_input("Name in spanish")
            description_en =st.text_area("Description in english")
            description_de = st.text_area("Description in german")
            description_es = st.text_area("Description in spanish")
            st.subheader("Select 1 image ")
            uploaded_file = st.file_uploader("")
        
            if uploaded_file!=None:
                st.image(uploaded_file, width = 500 ,output_format="PNG")
                
                if st.button("Save"):
                    # reemplazar los espacios por guiones bajos
                    title_separate = name_en.replace(" ", "_")
                    
                    with st.spinner('Uploading...'):
                        
                        image_1 = title_separate+".png"
                        
                        # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                        uploadimageToS3(uploaded_file,bucket_name , image_1)
                        ############################
                        # Connection to MongoDB
                        ############################
                        
                        # In this section you can add new activities to the database
                        # Price_adult is [[people],[price]]
                        
                        record = {
                        "Name_en": name_en, # ingles
                        "Name_de": name_de, # aleman
                        "Name_es": name_es, # español
                        "Description_en": description_en,
                        "Description_de": description_de,
                        "Description_es": description_es,
                        "Images": image_1,
                        }
                        
                        collection.insert_one(record)
        if activities_option=="Edit":
            
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            data = collection.find({},{"Name_en":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"])
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad = st.selectbox("Choose the activity",list_activities, key="edit_location")
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            
            
            
            st.subheader("Edit location")
            name_en = st.text_input("Name in english", complete_data["Name_en"])
            name_de = st.text_input("Name in german", complete_data["Name_de"])
            name_es = st.text_input("Name in spanish", complete_data["Name_es"])
            description_en =st.text_area("Description in english", complete_data["Description_en"])
            description_de = st.text_area("Description in german", complete_data["Description_de"])
            description_es = st.text_area("Description in spanish", complete_data["Description_es"])
            st.subheader("Image")
            st.image(get_link(bucket_name, complete_data["Images"]), width=500 )
            
            uploaded_file = st.file_uploader("Upload new image")
        
            if uploaded_file!=None:
                st.subheader("New image")
                st.image(uploaded_file, width = 500 ,output_format="PNG")
            
            if st.button("Save"):
                # reemplazar los espacios por guiones bajos
                title_separate = name_en.replace(" ", "_")
                
                if name_en== complete_data["Name_en"]:
                    with st.spinner('Uploading...'):
                        
                        image_1 = title_separate+".png"
                        
                        ############################
                        # Connection to MongoDB
                        ############################
                        
                        record = {
                        "Name_en": name_en, # ingles
                        "Name_de": name_de, # aleman
                        "Name_es": name_es, # español
                        "Description_en": description_en,
                        "Description_de": description_de,
                        "Description_es": description_es,
                        "Images": image_1,
                        }
                        
                        collection.update_one({"_id":code},{"$set":record})
                        if uploaded_file is not None:
                                uploadimageToS3(uploaded_file,bucket_name , image_1)
                        st.success("Location updated")
                
                if name_en!= complete_data["Name_en"]:
                    with st.spinner('Uploading...'):
                        
                        image_1 = title_separate+".png"
                        
                        ############################
                        # Connection to MongoDB
                        ############################
                        
                        record = {
                        "Name_en": name_en, # ingles
                        "Name_de": name_de, # aleman
                        "Name_es": name_es, # español
                        "Description_en": description_en,
                        "Description_de": description_de,
                        "Description_es": description_es,
                        "Images": image_1,
                        }
                        
                        collection.update_one({"_id":code},{"$set":record})
                        # working with s3
                        
                        copy_and_delete_s3_file(bucket_name, complete_data["Images"], image_1)
                        delete_s3_file(bucket_name, complete_data["Images"])
                        
                        # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                        if uploaded_file is not None:
                            uploadimageToS3(uploaded_file,bucket_name , image_1)
                        st.success("Location updated")
                
        ########################
        # Delete a location
        ########################
        if activities_option == "Delete":
            st.subheader("Delete a activity")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["locations"]
            data = collection.find({},{"Name_en":1, "_id":1})
            names = []
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                names.append(value["Name_en"])
                list_activities.append(value["Name_en"])
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad_1 = st.selectbox("Choose the activity",list_activities)
            if elegir_actividad_1 == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad_1)
            code = ids_activities[order_activity]
            
            complete_data = collection.find_one({"_id":code})
            
            title = st.header(complete_data["Name_en"])
            
            c1, c2 = st.columns(2)
        
            bucket_name = "peruviansunrise-storage"
            
            url_1 = get_link(bucket_name, complete_data["Images"])
            
            description = c1.write( complete_data["Description_en"])        
            
            c2.image(url_1, use_column_width="auto", width=400)
            
            
            if st.button("Delete"):
                with st.spinner('Deleting...'):    
                    order_activity = list_activities.index(elegir_actividad_1)
                    code = ids_activities[order_activity]
                    # delete activity in mongodb
                    
                    collection.delete_one({"_id": ObjectId(code)})
                    # ---
                    # delete activity in s3
                    title = complete_data["Name_en"]
                    
                    title_separate = title.replace(" ", "_")
                    
                    
                    image_1 = title_separate+".png"
                    
                    
                    try:
                        delete_s3_file(bucket_name,image_1)
                        
                        st.success("Activity deleted")
                    # ---
                    except: 
                        st.error("Error deleting images")
                        
        
    if menu=="Transportation":
        # mongodb connection 
        collection = db["transport"]
        # fin
        opciones = st.sidebar.radio("Option",["Create new","Edit","Delete"], key="transportation")
        if opciones == "Create new":
            st.subheader("Create new transport")
            name_en = st.text_input("Name in english", key="trans_en")
            # You can call any Streamlit command, including custom components:
            if "option1a" not in st.session_state:
                st.session_state["option1a"] = ""
            if "option2a" not in st.session_state:
                st.session_state["option2a"] = ""
            if "option3a" not in st.session_state:
                st.session_state["option3a"] = ""
            if "option4a" not in st.session_state:
                st.session_state["option4a"] = ""
            if "option5a" not in st.session_state:
                st.session_state["option5a"] = ""
            if "option6a" not in st.session_state:
                st.session_state["option6a"] = ""
            if "option7a" not in st.session_state:
                st.session_state["option7a"] = ""
            if "option8a" not in st.session_state:
                st.session_state["option8a"] = ""
            if "option9a" not in st.session_state:
                st.session_state["option9a"] = ""
            if "option10a" not in st.session_state:
                st.session_state["option10a"] = ""
                
            if "option1b" not in st.session_state:
                st.session_state["option1b"] = ""
            if "option2b" not in st.session_state:
                st.session_state["option2b"] = ""
            if "option3b" not in st.session_state:
                st.session_state["option3b"] = ""
            if "option4b" not in st.session_state:
                st.session_state["option4b"] = ""
            if "option5b" not in st.session_state:
                st.session_state["option5b"] = ""
            if "option6b" not in st.session_state:
                st.session_state["option6b"] = ""
            if "option7b" not in st.session_state:
                st.session_state["option7b"] = ""
            if "option8b" not in st.session_state:
                st.session_state["option8b"] = ""
            if "option9b" not in st.session_state:
                st.session_state["option9b"] = ""
            if "option10b" not in st.session_state:
                st.session_state["option10b"] = ""
                
            if "descrip_1_en" not in st.session_state:
                st.session_state["descrip_1_en"] = ""
                st.session_state["descrip_1_de"] = ""
                st.session_state["descrip_1_es"] = ""
            if "descrip_2_en" not in st.session_state:
                st.session_state["descrip_2_en"] = ""
                st.session_state["descrip_2_de"] = ""
                st.session_state["descrip_2_es"] = ""
            if "descrip_3_en" not in st.session_state:
                st.session_state["descrip_3_en"] = ""
                st.session_state["descrip_3_de"] = ""
                st.session_state["descrip_3_es"] = ""
            if "descrip_4_en" not in st.session_state:
                st.session_state["descrip_4_en"] = ""
                st.session_state["descrip_4_de"] = ""
                st.session_state["descrip_4_es"] = ""
            if "descrip_5_en" not in st.session_state:
                st.session_state["descrip_5_en"] = ""
                st.session_state["descrip_5_de"] = ""
                st.session_state["descrip_5_es"] = ""
            if "descrip_6_en" not in st.session_state:
                st.session_state["descrip_6_en"] = ""
                st.session_state["descrip_6_de"] = ""
                st.session_state["descrip_6_es"] = ""
            if "descrip_7_en" not in st.session_state:
                st.session_state["descrip_7_en"] = ""
                st.session_state["descrip_7_de"] = ""
                st.session_state["descrip_7_es"] = ""
            if "descrip_8_en" not in st.session_state:
                st.session_state["descrip_8_en"] = ""
                st.session_state["descrip_8_de"] = ""
                st.session_state["descrip_8_es"] = ""
            if "descrip_9_en" not in st.session_state:
                st.session_state["descrip_9_en"] = ""
                st.session_state["descrip_9_de"] = ""
                st.session_state["descrip_9_es"] = ""
            if "descrip_10_en" not in st.session_state:
                st.session_state["descrip_10_en"] = ""
                st.session_state["descrip_10_de"] = ""
                st.session_state["descrip_10_es"] = ""
            
            # lista de las locations
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            
            with st.expander("Location", expanded=True):
                c1, c2 = st.columns((2,5))
                slider_number = c1.number_input("Add", 1, 10)
                
                # it's needed this 2 lines of code to run a lottie animation
                link = "https://assets3.lottiefiles.com/packages/lf20_q6dNvPXDCZ.json"
                lottie_json = load_lottieurl(link)
                # fin
                
                # crear las variables para la eliminación de  las rutas 
                if "route_1" not in st.session_state: 
                    st.session_state['route_1'] = False
                if "route_2" not in st.session_state: 
                    st.session_state['route_2'] = False
                if "route_3" not in st.session_state: 
                    st.session_state['route_3'] = False
                if "route_4" not in st.session_state: 
                    st.session_state['route_4'] = False
                if "route_5" not in st.session_state: 
                    st.session_state['route_5'] = False
                if "route_6" not in st.session_state: 
                    st.session_state['route_6'] = False
                if "route_7" not in st.session_state: 
                    st.session_state['route_7'] = False
                if "route_8" not in st.session_state: 
                    st.session_state['route_8'] = False
                if "route_9" not in st.session_state: 
                    st.session_state['route_9'] = False
                if "route_10" not in st.session_state: 
                    st.session_state['route_10'] = False
                
                value=15
                for x in range(1,11):
                    if st.session_state["route_"+str(x)] == False:
                        value = x
                    x+=1
                
                
                route1 = st.empty()   
                route2 = st.empty()   
                route3 = st.empty()  
                route4 = st.empty()   
                route5 = st.empty()   
                route6 = st.empty()   
                route7 = st.empty()  
                route8 = st.empty()   
                route9 = st.empty()   
                route10 = st.empty() 
                
                if slider_number >= 1:
                    with route1.container():
                        col1a,col2a,col3a, col4a= st.columns([2,2,2,1])
                        with col1a:
                            salida_1 = st.selectbox("Origin",list_activities, key="salida_1")
                            st.session_state['option1a'] = salida_1
                        with col2a:
                            st_lottie(lottie_json, height=70 , key="1_lottie", reverse=False )
                        with col3a:
                            dias_1 = st.selectbox("Destination",list_activities, key="llegada_1")
                            st.session_state['option1b'] = dias_1
                        with col4a:
                            st.markdown("Delete")
                            but = st.button("Delete", key="delete_1")
                            if but:
                                st.session_state['route_1'] = True
                                
                    if st.session_state["route_1"]:
                        st.session_state["option1a"] = ""
                        st.session_state["option1b"] = ""
                        route1.empty()
                        
                if slider_number >= 2:
                    with route2.container():
                        col1b,col2b,col3b, col4b= st.columns([2,2,2,1])
                        with col1b:
                            salida_2 = st.selectbox("Origin",list_activities, key="salida_2")
                            st.session_state['option2a'] = salida_2
                        with col2b:
                            st_lottie(lottie_json, height=70 , key="2_lottie", reverse=False )
                        with col3b:
                            dias_2 = st.selectbox("Destination",list_activities, key="llegada_2")
                            st.session_state['option2b'] = dias_2
                        with col4b:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_2"):
                                st.session_state['route_2'] = True
                    if st.session_state["route_2"]:
                        st.session_state["option2a"] = ""
                        st.session_state["option2b"] = ""
                        route2.empty()
                if slider_number >= 3:
                    with route3.container():
                        col1c,col2c,col3c, col4c= st.columns([2,2,2,1])
                        with col1c:
                            salida_3 = st.selectbox("Origin",list_activities, key="salida_3")
                            st.session_state['option3a'] = salida_3
                        with col2c:
                            st_lottie(lottie_json, height=70 , key="3_lottie", reverse=False )
                        with col3c:
                            dias_3 = st.selectbox("Destination",list_activities, key="llegada_3")
                            st.session_state['option3b'] = dias_3
                        with col4c:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_3"):
                                st.session_state['route_3'] = True
                    if st.session_state["route_3"]:
                        st.session_state["option3a"] = ""
                        st.session_state["option3b"] = ""
                        route3.empty()
                if slider_number >= 4:
                    with route4.container():
                        col1d,col2d,col3d, col4d= st.columns([2,2,2,1])
                        with col1d:
                            salida_4 = st.selectbox("Origin",list_activities, key="salida_4")
                            st.session_state['option4a'] = salida_4
                        with col2d:
                            st_lottie(lottie_json, height=70 , key="4_lottie", reverse=False )
                        with col3d:
                            dias_4 = st.selectbox("Destination",list_activities, key="llegada_4")
                            st.session_state['option4b'] = dias_4
                        with col4d:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_4"):
                                st.session_state['route_4'] = True
                    if st.session_state["route_4"]:
                        st.session_state["option4a"] = ""
                        st.session_state["option4b"] = ""
                        route4.empty()  
                if slider_number >= 5:
                    with route5.container():
                        col1e,col2e,col3e, col4e= st.columns([2,2,2,1])
                        with col1e:
                            salida_5 = st.selectbox("Origin",list_activities, key="salida_5")
                            st.session_state['option5a'] = salida_5
                        with col2e:
                            st_lottie(lottie_json, height=70 , key="5_lottie", reverse=False )
                        with col3e:
                            dias_5 = st.selectbox("Destination",list_activities, key="llegada_5")
                            st.session_state['option5b'] = dias_5
                        with col4e:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_5"):
                                st.session_state['route_5'] = True
                    if st.session_state["route_5"]:
                        st.session_state["option5a"] = ""
                        st.session_state["option5b"] = ""
                        route5.empty() 
                if slider_number >= 6:
                    with route6.container():
                        col1f,col2f,col3f, col4f= st.columns([2,2,2,1])
                        with col1f:
                            salida_6 = st.selectbox("Origin",list_activities, key="salida_6")
                            st.session_state['option6a'] = salida_6
                        with col2f:
                            st_lottie(lottie_json, height=70 , key="6_lottie", reverse=False )
                        with col3f:
                            dias_6 = st.selectbox("Destination",list_activities, key="llegada_6")
                            st.session_state['option6b'] = dias_6
                        with col4f:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_6"):
                                st.session_state['route_6'] = True
                    if st.session_state["route_6"]:
                        st.session_state["option6a"] = ""
                        st.session_state["option6b"] = ""
                        route6.empty() 
                if slider_number >= 7:
                    with route7.container():
                        col1g,col2g,col3g, col4g= st.columns([2,2,2,1])
                        with col1g:
                            salida_7 = st.selectbox("Origin",list_activities, key="salida_7")
                            st.session_state['option7a'] = salida_7
                        with col2g:
                            st_lottie(lottie_json, height=70 , key="7_lottie", reverse=False )
                        with col3g:
                            dias_7 = st.selectbox("Destination",list_activities, key="llegada_7")
                            st.session_state['option7b'] = dias_7
                        with col4g:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_7"):
                                st.session_state['route_7'] = True
                    if st.session_state["route_7"]:
                        st.session_state["option7a"] = ""
                        st.session_state["option7b"] = ""
                        route7.empty() 
                if slider_number >= 8:
                    with route8.container():
                        col1h,col2h,col3h, col4h= st.columns([2,2,2,1])
                        with col1h:
                            salida_8 = st.selectbox("Origin",list_activities, key="salida_8")
                            st.session_state['option8a'] = salida_8
                        with col2h:
                            st_lottie(lottie_json, height=70 , key="8_lottie", reverse=False )
                        with col3h:
                            dias_8 = st.selectbox("Destination",list_activities, key="llegada_8")
                            st.session_state['option8b'] = dias_8
                        with col4h:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_8"):
                                st.session_state['route_8'] = True
                    if st.session_state["route_8"]:
                        st.session_state["option8a"] = ""
                        st.session_state["option8b"] = ""
                        route8.empty() 
                if slider_number >= 9:
                    with route9.container():
                        col1i,col2i,col3i, col4i= st.columns([2,2,2,1])
                        with col1i:
                            salida_9 = st.selectbox("Origin",list_activities, key="salida_9")
                            st.session_state['option9a'] = salida_9
                        with col2i:
                            st_lottie(lottie_json, height=70 , key="9_lottie", reverse=False )
                        with col3i:
                            dias_9 = st.selectbox("Destination",list_activities, key="llegada_9")
                            st.session_state['option9b'] = dias_9
                        with col4i:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_9"):
                                st.session_state['route_9'] = True
                    if st.session_state["route_9"]:
                        st.session_state["option9a"] = ""
                        st.session_state["option9b"] = ""
                        route9.empty() 
                if slider_number >= 10:
                    with route10.container():
                        col1j,col2j,col3j, col4j= st.columns([2,2,2,1])
                        with col1j:
                            salida_10 = st.selectbox("Origin",list_activities, key="salida_10")
                            st.session_state['option10a'] = salida_10
                        with col2j:
                            st_lottie(lottie_json, height=70 , key="10_lottie", reverse=False )
                        with col3j:
                            dias_10 = st.selectbox("Destination",list_activities, key="llegada_10")
                            st.session_state['option10b'] = dias_10
                        with col4j:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_10"):
                                st.session_state['route_10'] = True
                    if st.session_state["route_10"]:
                        st.session_state["option10a"] = ""
                        st.session_state["option10b"] = ""
                        route10.empty()

            # creation of description of the route
            if slider_number >= 1 and st.session_state["route_1"] == False:
                st.subheader("Description "+st.session_state['option1a']+" to "+st.session_state['option1b'])
                with st.container():
                    coli1, coli2, coli3 =st.columns([1,1,1])
                    st.session_state.descrip_1_en = coli1.text_area("English", key="descrip_1_enx")
                    st.session_state.descrip_1_de = coli2.text_area("Deutsch", key="descrip_1_dex")
                    st.session_state.descrip_1_es = coli3.text_area("Spanish", key="descrip_1_esx")
            if  st.session_state["route_1"] != False:
                st.session_state.descrip_1_en = ""
                st.session_state.descrip_1_de = ""
                st.session_state.descrip_1_es = ""
                
            if slider_number >= 2 and st.session_state["route_2"] == False:
                st.subheader("Description "+st.session_state['option2a']+" to "+st.session_state['option2b'])
                with st.container():
                    coli1a, coli2a, coli3a =st.columns([1,1,1])
                    st.session_state.descrip_2_en = coli1a.text_area("English", key="descrip_2_enx")
                    st.session_state.descrip_2_de = coli2a.text_area("Deutsch", key="descrip_2_dex")
                    st.session_state.descrip_2_es = coli3a.text_area("Spanish", key="descrip_2_esx")
            if  st.session_state["route_2"] != False:
                st.session_state.descrip_2_en = ""
                st.session_state.descrip_2_de = ""
                st.session_state.descrip_2_es = ""
                
            if slider_number >= 3 and st.session_state["route_3"] == False:
                st.subheader("Description "+st.session_state['option3a']+" to "+st.session_state['option3b'])
                with st.container():
                    coli1b, coli2b, coli3b =st.columns([1,1,1])
                    st.session_state.descrip_3_en = coli1b.text_area("English", key="descrip_3_enx")
                    st.session_state.descrip_3_de = coli2b.text_area("Deutsch", key="descrip_3_dex")
                    st.session_state.descrip_3_es = coli3b.text_area("Spanish", key="descrip_3_esx")
            if  st.session_state["route_3"] != False:
                st.session_state.descrip_3_en = ""
                st.session_state.descrip_3_de = ""
                st.session_state.descrip_3_es = ""
                
            if slider_number >= 4 and st.session_state["route_4"] == False:
                st.subheader("Description "+st.session_state['option4a']+" to "+st.session_state['option4b'])
                with st.container():
                    coli1c, coli2c, coli3c =st.columns([1,1,1])
                    st.session_state.descrip_4_en = coli1c.text_area("English", key="descrip_4_enx")
                    st.session_state.descrip_4_de = coli2c.text_area("Deutsch", key="descrip_4_dex")
                    st.session_state.descrip_4_es = coli3c.text_area("Spanish", key="descrip_4_esx")
            if  st.session_state["route_4"] != False:
                st.session_state.descrip_4_en = ""
                st.session_state.descrip_4_de = ""
                st.session_state.descrip_4_es = ""
                
            if slider_number >= 5 and st.session_state["route_5"] == False:
                st.subheader("Description "+st.session_state['option5a']+" to "+st.session_state['option5b'])
                with st.container():
                    coli1d, coli2d, coli3d =st.columns([1,1,1])
                    st.session_state.descrip_5_en = coli1d.text_area("English", key="descrip_5_enx")
                    st.session_state.descrip_5_de = coli2d.text_area("Deutsch", key="descrip_5_dex")
                    st.session_state.descrip_5_es = coli3d.text_area("Spanish", key="descrip_5_esx")      
            if  st.session_state["route_5"] != False:
                st.session_state.descrip_5_en = ""
                st.session_state.descrip_5_de = ""
                st.session_state.descrip_5_es = ""
                
            if slider_number >= 6 and st.session_state["route_6"] == False:
                st.subheader("Description "+st.session_state['option6a']+" to "+st.session_state['option6b'])
                with st.container():
                    coli1e, coli2e, coli3e =st.columns([1,1,1])
                    st.session_state.descrip_6_en = coli1e.text_area("English", key="descrip_6_enx")
                    st.session_state.descrip_6_de = coli2e.text_area("Deutsch", key="descrip_6_dex")
                    st.session_state.descrip_6_es = coli3e.text_area("Spanish", key="descrip_6_esx")  
            if  st.session_state["route_6"] != False:
                st.session_state.descrip_6_en = ""
                st.session_state.descrip_6_de = ""
                st.session_state.descrip_6_es = ""
                
            if slider_number >= 7 and st.session_state["route_7"] == False:
                st.subheader("Description "+st.session_state['option7a']+" to "+st.session_state['option7b'])
                with st.container():
                    coli1f, coli2f, coli3f =st.columns([1,1,1])
                    st.session_state.descrip_7_en = coli1f.text_area("English", key="descrip_7_enx")
                    st.session_state.descrip_7_de = coli2f.text_area("Deutsch", key="descrip_7_dex")
                    st.session_state.descrip_7_es = coli3f.text_area("Spanish", key="descrip_7_esx")  
            if  st.session_state["route_7"] != False:
                st.session_state.descrip_7_en = ""
                st.session_state.descrip_7_de = ""
                st.session_state.descrip_7_es = ""
                
            if slider_number >= 8 and st.session_state["route_8"] == False:
                st.subheader("Description "+st.session_state['option8a']+" to "+st.session_state['option8b'])
                with st.container():
                    coli1g, coli2g, coli3g =st.columns([1,1,1])
                    st.session_state.descrip_8_en = coli1g.text_area("English", key="descrip_8_enx")
                    st.session_state.descrip_8_de = coli2g.text_area("Deutsch", key="descrip_8_dex")
                    st.session_state.descrip_8_es = coli3g.text_area("Spanish", key="descrip_8_esx")  
            if  st.session_state["route_8"] != False:
                st.session_state.descrip_8_en = ""
                st.session_state.descrip_8_de = ""
                st.session_state.descrip_8_es = ""
                
            if slider_number >= 9 and st.session_state["route_9"] == False:
                st.subheader("Description "+st.session_state['option9a']+" to "+st.session_state['option9b'])
                with st.container():
                    coli1h, coli2h, coli3h =st.columns([1,1,1])
                    st.session_state.descrip_9_en = coli1h.text_area("English", key="descrip_9_enx")
                    st.session_state.descrip_9_de = coli2h.text_area("Deutsch", key="descrip_9_dex")
                    st.session_state.descrip_9_es = coli3h.text_area("Spanish", key="descrip_9_esx")  
            if  st.session_state["route_9"] != False:
                st.session_state.descrip_9_en = ""
                st.session_state.descrip_9_de = ""
                st.session_state.descrip_9_es = ""
                
            if slider_number >= 10 and st.session_state["route_10"] == False:
                st.subheader("Description "+st.session_state['option10a']+" to "+st.session_state['option10b'])
                with st.container():
                    coli1i, coli2i, coli3i =st.columns([1,1,1])
                    st.session_state.descrip_10_en = coli1i.text_area("English", key="descrip_10_enx")
                    st.session_state.descrip_10_de = coli2i.text_area("Deutsch", key="descrip_10_dex")
                    st.session_state.descrip_10_es = coli3i.text_area("Spanish", key="descrip_10_esx")  
            if  st.session_state["route_10"] != False:
                st.session_state.descrip_10_en = ""
                st.session_state.descrip_10_de = ""
                st.session_state.descrip_10_es = ""
            
            st.subheader("Meals included")
            cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
            breakfast = cole1.checkbox('Breakfast')
            lunch = cole2.checkbox('Lunch')
            dinner = cole3.checkbox('Dinner')
            other = cole4.checkbox('Other (please describe in meal notes)')
            st.subheader("Meal notes")
            as1,as2,as3 =st.columns([1,1,1])
            
            notes_en = as1.text_area("English")
            notes_de = as2.text_area("Deutsch")
            notes_es = as3.text_area("Spanish")
            
            # put the prices
            st.subheader("Prices")
            
            @st.cache()
            def get_data(filas):
                incluir = np.arange(1,filas+1)
                values = [0]*(filas)
                df = pd.DataFrame(
                    {"Amount of People": incluir,"Price Adults":values,"Price Kids":values}
                )
                return df
            
            
            elegir_precio = st.radio("Choose the price",["Fixed Price","Adults and Kids"],horizontal=True)
            precios_fijos = False
            
            precios_kids = False
            
            
            col1,col2 = st.columns([2,1])
            if elegir_precio == "Fixed Price":
                precios_fijos = col1.number_input("Price", key="price_fixed" , step=1)
                    
            if elegir_precio == "Adults and Kids":
                with col1:
                    
                    numero_filas_k = st.slider("Number of people",1,15,step=1, value=5, key="adults_kids_slider")
                    
                    data_k = get_data(numero_filas_k)
                    gb_k = GridOptionsBuilder.from_dataframe(data_k)
                    #make all columns editable
                    gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                    go_k = gb_k.build()
                    
                    ag_k = AgGrid(
                        data_k, 
                        gridOptions=go_k, 
                        # height=300, 
                        fit_columns_on_grid_load=True,
                        theme= "light" # or "streamlit","light","balham","material"
                    )
                    # st.subheader("Returned Data")
                    # st.dataframe(ag_k['data'])
                    
                    df_prices_kids = ag_k["data"]
                    # st.dataframe(ag['data'])
                    df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                    df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                    df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                    
                    df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                    df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                    df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                    precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                    # st.write(precios_kids)

            st.subheader("Operator")
            operator = st.text_input("Service provider")
            st.subheader("Internal Pricing Notes (not shown to the traveler)")
            notes_precio = st.text_area("Internal Pricing Notes")

            cargar_data = st.button("Save all data")
            # algoritmo para ordenar los datos de llenos a vacios.
            llenos = []
            vacios = []
            if cargar_data:
                with st.spinner('Uploading...'):
                    for y in range(1,11):
                        if st.session_state["option"+str(y)+"a"] =="":
                            vacios.append(y)
                        else:
                            llenos.append(y)
                    data_final = llenos + vacios
            # fin 
                    
                    # redefinir las variables de las rutas y definicioes para cada valor del 1-10
                    st.session_state["option1a"] = st.session_state["option"+str(data_final[0])+"a"]
                    st.session_state["option1b"] = st.session_state["option"+str(data_final[0])+"b"]
                    descrip_a1 = st.session_state["descrip_"+str(data_final[0])+"_en"]
                    descrip_b1 = st.session_state["descrip_"+str(data_final[0])+"_de"] 
                    descrip_c1 = st.session_state["descrip_"+str(data_final[0])+"_es"]
                    
                    st.session_state["option2a"] = st.session_state["option"+str(data_final[1])+"a"]
                    st.session_state["option2b"] = st.session_state["option"+str(data_final[1])+"b"]
                    descrip_a2 = st.session_state["descrip_"+str(data_final[1])+"_en"]
                    descrip_b2 = st.session_state["descrip_"+str(data_final[1])+"_de"] 
                    descrip_c2 = st.session_state["descrip_"+str(data_final[1])+"_es"]
                    
                    
                    
                    collection = db["transport"]
                    
                    # In this section you can add new activities to the database
                    # para cada route o ruta we put  the data in the following order : [lugar de salida, lugar de llegada, descripcion ingles, descripcion aleman, descripcion espanol]
                    
                    record = {
                    "Name_en": name_en,
                    "route1": [st.session_state["option"+str(data_final[0])+"a"],st.session_state["option"+str(data_final[0])+"b"], st.session_state["descrip_"+str(data_final[0])+"_en"],st.session_state["descrip_"+str(data_final[0])+"_de"] , st.session_state["descrip_"+str(data_final[0])+"_es"]], 
                    "route2": [st.session_state["option"+str(data_final[1])+"a"],st.session_state["option"+str(data_final[1])+"b"], st.session_state["descrip_"+str(data_final[1])+"_en"],st.session_state["descrip_"+str(data_final[1])+"_de"] , st.session_state["descrip_"+str(data_final[1])+"_es"]], 
                    "route3": [st.session_state["option"+str(data_final[2])+"a"],st.session_state["option"+str(data_final[2])+"b"], st.session_state["descrip_"+str(data_final[2])+"_en"],st.session_state["descrip_"+str(data_final[2])+"_de"] , st.session_state["descrip_"+str(data_final[2])+"_es"]], 
                    "route4": [st.session_state["option"+str(data_final[3])+"a"],st.session_state["option"+str(data_final[3])+"b"], st.session_state["descrip_"+str(data_final[3])+"_en"],st.session_state["descrip_"+str(data_final[3])+"_de"] , st.session_state["descrip_"+str(data_final[3])+"_es"]],
                    "route5": [st.session_state["option"+str(data_final[4])+"a"],st.session_state["option"+str(data_final[4])+"b"], st.session_state["descrip_"+str(data_final[4])+"_en"],st.session_state["descrip_"+str(data_final[4])+"_de"] , st.session_state["descrip_"+str(data_final[4])+"_es"]],
                    "route6": [st.session_state["option"+str(data_final[5])+"a"],st.session_state["option"+str(data_final[5])+"b"], st.session_state["descrip_"+str(data_final[5])+"_en"],st.session_state["descrip_"+str(data_final[5])+"_de"] , st.session_state["descrip_"+str(data_final[5])+"_es"]],
                    "route7": [st.session_state["option"+str(data_final[6])+"a"],st.session_state["option"+str(data_final[6])+"b"], st.session_state["descrip_"+str(data_final[6])+"_en"],st.session_state["descrip_"+str(data_final[6])+"_de"] , st.session_state["descrip_"+str(data_final[6])+"_es"]],
                    "route8": [st.session_state["option"+str(data_final[7])+"a"],st.session_state["option"+str(data_final[7])+"b"], st.session_state["descrip_"+str(data_final[7])+"_en"],st.session_state["descrip_"+str(data_final[7])+"_de"] , st.session_state["descrip_"+str(data_final[7])+"_es"]],
                    "route9": [st.session_state["option"+str(data_final[8])+"a"],st.session_state["option"+str(data_final[8])+"b"], st.session_state["descrip_"+str(data_final[8])+"_en"],st.session_state["descrip_"+str(data_final[8])+"_de"] , st.session_state["descrip_"+str(data_final[8])+"_es"]],
                    "route10": [st.session_state["option"+str(data_final[9])+"a"],st.session_state["option"+str(data_final[9])+"b"], st.session_state["descrip_"+str(data_final[9])+"_en"],st.session_state["descrip_"+str(data_final[9])+"_de"] , st.session_state["descrip_"+str(data_final[9])+"_es"]],
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner,
                    "other": other,
                    "meal notes ingles": notes_en,
                    "meal notes aleman": notes_de,
                    "meal notes espanol": notes_es,
                    "fixed price": precios_fijos,
                    "adults and kids" : precios_kids,
                    "operator" : operator,
                    "notes price":notes_precio
                    }
                    
                    collection.insert_one(record)
                    # poner las variables en su estado inicial
                    st.session_state["option1a"] = ""
                    st.session_state["option2a"] = ""
                    st.session_state["option3a"] = ""
                    st.session_state["option4a"] = ""
                    st.session_state["option5a"] = ""
                    st.session_state["option6a"] = ""
                    st.session_state["option7a"] = ""
                    st.session_state["option8a"] = ""
                    st.session_state["option9a"] = ""
                    st.session_state["option10a"] = ""
                    
                    st.session_state["option1b"] = ""
                    st.session_state["option2b"] = ""
                    st.session_state["option3b"] = ""
                    st.session_state["option4b"] = ""
                    st.session_state["option5b"] = ""
                    st.session_state["option6b"] = ""
                    st.session_state["option7b"] = ""
                    st.session_state["option8b"] = ""
                    st.session_state["option9b"] = ""
                    st.session_state["option10b"] = ""
                
                    st.session_state["descrip_1_en"] = ""
                    st.session_state["descrip_1_de"] = ""
                    st.session_state["descrip_1_es"] = ""
                    st.session_state["descrip_2_en"] = ""
                    st.session_state["descrip_2_de"] = ""
                    st.session_state["descrip_2_es"] = ""
                    st.session_state["descrip_3_en"] = ""
                    st.session_state["descrip_3_de"] = ""
                    st.session_state["descrip_3_es"] = ""
                    st.session_state["descrip_4_en"] = ""
                    st.session_state["descrip_4_de"] = ""
                    st.session_state["descrip_4_es"] = ""
                    st.session_state["descrip_5_en"] = ""
                    st.session_state["descrip_5_de"] = ""
                    st.session_state["descrip_5_es"] = ""
                    st.session_state["descrip_6_en"] = ""
                    st.session_state["descrip_6_de"] = ""
                    st.session_state["descrip_6_es"] = ""
                    st.session_state["descrip_7_en"] = ""
                    st.session_state["descrip_7_de"] = ""
                    st.session_state["descrip_7_es"] = ""
                    st.session_state["descrip_8_en"] = ""
                    st.session_state["descrip_8_de"] = ""
                    st.session_state["descrip_8_es"] = ""
                    st.session_state["descrip_9_en"] = ""
                    st.session_state["descrip_9_de"] = ""
                    st.session_state["descrip_9_es"] = ""
                    st.session_state["descrip_10_en"] = ""
                    st.session_state["descrip_10_de"] = ""
                    st.session_state["descrip_10_es"] = ""
                
                    st.session_state['route_1'] = False
                    st.session_state['route_2'] = False
                    st.session_state['route_3'] = False
                    st.session_state['route_4'] = False
                    st.session_state['route_5'] = False
                    st.session_state['route_6'] = False
                    st.session_state['route_7'] = False
                    st.session_state['route_8'] = False
                    st.session_state['route_9'] = False
                    st.session_state['route_10'] = False
                    st.success('Upload successful!')
        #####################
        # opcion de editar transportation 
        #####################
        if opciones == "Edit":
            st.subheader("Edit a transport")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["transport"]
            data = collection.find({},{"Name_en":1, "operator":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"] + "  (" + value["operator"]+ ")")
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad = st.selectbox("Choose the transport",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            
            name_en = st.text_input("Name in english",complete_data["Name_en"] , key="trans_en")
            
            # You can call any Streamlit command, including custom components:
            # You can call any Streamlit command, including custom components:
            if "option1a" not in st.session_state:
                st.session_state["option1a"] = ""
            if "option2a" not in st.session_state:
                st.session_state["option2a"] = ""
            if "option3a" not in st.session_state:
                st.session_state["option3a"] = ""
            if "option4a" not in st.session_state:
                st.session_state["option4a"] = ""
            if "option5a" not in st.session_state:
                st.session_state["option5a"] = ""
            if "option6a" not in st.session_state:
                st.session_state["option6a"] = ""
            if "option7a" not in st.session_state:
                st.session_state["option7a"] = ""
            if "option8a" not in st.session_state:
                st.session_state["option8a"] = ""
            if "option9a" not in st.session_state:
                st.session_state["option9a"] = ""
            if "option10a" not in st.session_state:
                st.session_state["option10a"] = ""
                
            if "option1b" not in st.session_state:
                st.session_state["option1b"] = ""
            if "option2b" not in st.session_state:
                st.session_state["option2b"] = ""
            if "option3b" not in st.session_state:
                st.session_state["option3b"] = ""
            if "option4b" not in st.session_state:
                st.session_state["option4b"] = ""
            if "option5b" not in st.session_state:
                st.session_state["option5b"] = ""
            if "option6b" not in st.session_state:
                st.session_state["option6b"] = ""
            if "option7b" not in st.session_state:
                st.session_state["option7b"] = ""
            if "option8b" not in st.session_state:
                st.session_state["option8b"] = ""
            if "option9b" not in st.session_state:
                st.session_state["option9b"] = ""
            if "option10b" not in st.session_state:
                st.session_state["option10b"] = ""
                
            if "descrip_1_en" not in st.session_state:
                st.session_state["descrip_1_en"] = ""
                st.session_state["descrip_1_de"] = ""
                st.session_state["descrip_1_es"] = ""
            if "descrip_2_en" not in st.session_state:
                st.session_state["descrip_2_en"] = ""
                st.session_state["descrip_2_de"] = ""
                st.session_state["descrip_2_es"] = ""
            if "descrip_3_en" not in st.session_state:
                st.session_state["descrip_3_en"] = ""
                st.session_state["descrip_3_de"] = ""
                st.session_state["descrip_3_es"] = ""
            if "descrip_4_en" not in st.session_state:
                st.session_state["descrip_4_en"] = ""
                st.session_state["descrip_4_de"] = ""
                st.session_state["descrip_4_es"] = ""
            if "descrip_5_en" not in st.session_state:
                st.session_state["descrip_5_en"] = ""
                st.session_state["descrip_5_de"] = ""
                st.session_state["descrip_5_es"] = ""
            if "descrip_6_en" not in st.session_state:
                st.session_state["descrip_6_en"] = ""
                st.session_state["descrip_6_de"] = ""
                st.session_state["descrip_6_es"] = ""
            if "descrip_7_en" not in st.session_state:
                st.session_state["descrip_7_en"] = ""
                st.session_state["descrip_7_de"] = ""
                st.session_state["descrip_7_es"] = ""
            if "descrip_8_en" not in st.session_state:
                st.session_state["descrip_8_en"] = ""
                st.session_state["descrip_8_de"] = ""
                st.session_state["descrip_8_es"] = ""
            if "descrip_9_en" not in st.session_state:
                st.session_state["descrip_9_en"] = ""
                st.session_state["descrip_9_de"] = ""
                st.session_state["descrip_9_es"] = ""
            if "descrip_10_en" not in st.session_state:
                st.session_state["descrip_10_en"] = ""
                st.session_state["descrip_10_de"] = ""
                st.session_state["descrip_10_es"] = ""

            # lista de las locations
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            # algoritmo para encontrar el nombre de la "location"
            def find_location(name, number):
                if complete_data["route"+str(number)][0] != "":
                    position = list_activities.index(name)
                    return position
                else:
                    return int(0)
            
            # fin
            with st.expander("Location", expanded=True):
                # algoritmo para encontrar la cantidad de rutas "routes" q llenas y las vacias.
                def find_routes():
                    llenos=0
                    for x in range(1,11):
                        if complete_data["route"+str(x)][0] !="":
                            llenos+=1
                    return llenos
                llenos = find_routes()
                # fin 
                
                c1, c2 = st.columns((2,5))
                slider_number = c1.number_input("Add", 1, 10,llenos)
                
                # it's needed this 2 lines of code to run a lottie animation
                link = "https://assets3.lottiefiles.com/packages/lf20_q6dNvPXDCZ.json"
                lottie_json = load_lottieurl(link)
                # fin
                
                # crear las variables para la eliminación de  las rutas 
                if "route_1" not in st.session_state: 
                    st.session_state['route_1'] = False
                if "route_2" not in st.session_state: 
                    st.session_state['route_2'] = False
                if "route_3" not in st.session_state: 
                    st.session_state['route_3'] = False
                if "route_4" not in st.session_state: 
                    st.session_state['route_4'] = False
                if "route_5" not in st.session_state: 
                    st.session_state['route_5'] = False
                if "route_6" not in st.session_state: 
                    st.session_state['route_6'] = False
                if "route_7" not in st.session_state: 
                    st.session_state['route_7'] = False
                if "route_8" not in st.session_state: 
                    st.session_state['route_8'] = False
                if "route_9" not in st.session_state: 
                    st.session_state['route_9'] = False
                if "route_10" not in st.session_state: 
                    st.session_state['route_10'] = False
                
                value=15
                for x in range(1,11):
                    if st.session_state["route_"+str(x)] == False:
                        value = x
                    x+=1
                
                
                route1 = st.empty()   
                route2 = st.empty()   
                route3 = st.empty()  
                route4 = st.empty()   
                route5 = st.empty()   
                route6 = st.empty()   
                route7 = st.empty()  
                route8 = st.empty()   
                route9 = st.empty()   
                route10 = st.empty() 
                
                if slider_number >= 1:
                    with route1.container():
                        col1a,col2a,col3a, col4a= st.columns([2,2,2,1])
                        with col1a:
                            salida_1 = st.selectbox("Origin" , list_activities, find_location(complete_data["route1"][0],1), key="salida_1")
                            st.session_state['option1a'] = salida_1
                        with col2a:
                            st_lottie(lottie_json, height=70 , key="1_lottie", reverse=False )
                        with col3a:
                            dias_1 = st.selectbox("Destination",list_activities,find_location(complete_data["route1"][1],1), key="llegada_1")
                            st.session_state['option1b'] = dias_1
                        with col4a:
                            st.markdown("Delete")
                            but = st.button("Delete", key="delete_1")
                            if but:
                                st.session_state['route_1'] = True
                                
                    if st.session_state["route_1"]:
                        st.session_state["option1a"] = ""
                        st.session_state["option1b"] = ""
                        route1.empty()
                        
                if slider_number >= 2:
                    with route2.container():
                        col1b,col2b,col3b, col4b= st.columns([2,2,2,1])
                        with col1b:
                            salida_2 = st.selectbox("Origin",list_activities,find_location(complete_data["route2"][0],2), key="salida_2")
                            st.session_state['option2a'] = salida_2
                        with col2b:
                            st_lottie(lottie_json, height=70 , key="2_lottie", reverse=False )
                        with col3b:
                            dias_2 = st.selectbox("Destination",list_activities, find_location(complete_data["route2"][1],2),key="llegada_2")
                            st.session_state['option2b'] = dias_2
                        with col4b:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_2"):
                                st.session_state['route_2'] = True
                    if st.session_state["route_2"]:
                        st.session_state["option2a"] = ""
                        st.session_state["option2b"] = ""
                        route2.empty()
                if slider_number >= 3:
                    with route3.container():
                        col1c,col2c,col3c, col4c= st.columns([2,2,2,1])
                        with col1c:
                            salida_3 = st.selectbox("Origin",list_activities,find_location(complete_data["route3"][0],3), key="salida_3")
                            st.session_state['option3a'] = salida_3
                        with col2c:
                            st_lottie(lottie_json, height=70 , key="3_lottie", reverse=False )
                        with col3c:
                            dias_3 = st.selectbox("Destination",list_activities,find_location(complete_data["route3"][1],3), key="llegada_3")
                            st.session_state['option3b'] = dias_3
                        with col4c:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_3"):
                                st.session_state['route_3'] = True
                    if st.session_state["route_3"]:
                        st.session_state["option3a"] = ""
                        st.session_state["option3b"] = ""
                        route3.empty()
                if slider_number >= 4:
                    with route4.container():
                        col1d,col2d,col3d, col4d= st.columns([2,2,2,1])
                        with col1d:
                            salida_4 = st.selectbox("Origin",list_activities, find_location(complete_data["route4"][0],4),key="salida_4")
                            st.session_state['option4a'] = salida_4
                        with col2d:
                            st_lottie(lottie_json, height=70 , key="4_lottie", reverse=False )
                        with col3d:
                            dias_4 = st.selectbox("Destination",list_activities, find_location(complete_data["route4"][1],4),key="llegada_4")
                            st.session_state['option4b'] = dias_4
                        with col4d:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_4"):
                                st.session_state['route_4'] = True
                    if st.session_state["route_4"]:
                        st.session_state["option4a"] = ""
                        st.session_state["option4b"] = ""
                        route4.empty()  
                if slider_number >= 5:
                    with route5.container():
                        col1e,col2e,col3e, col4e= st.columns([2,2,2,1])
                        with col1e:
                            salida_5 = st.selectbox("Origin",list_activities,find_location(complete_data["route5"][0],5), key="salida_5")
                            st.session_state['option5a'] = salida_5
                        with col2e:
                            st_lottie(lottie_json, height=70 , key="5_lottie", reverse=False )
                        with col3e:
                            dias_5 = st.selectbox("Destination",list_activities,find_location(complete_data["route5"][1],5), key="llegada_5")
                            st.session_state['option5b'] = dias_5
                        with col4e:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_5"):
                                st.session_state['route_5'] = True
                    if st.session_state["route_5"]:
                        st.session_state["option5a"] = ""
                        st.session_state["option5b"] = ""
                        route5.empty() 
                if slider_number >= 6:
                    with route6.container():
                        col1f,col2f,col3f, col4f= st.columns([2,2,2,1])
                        with col1f:
                            salida_6 = st.selectbox("Origin",list_activities, find_location(complete_data["route6"][0],6),key="salida_6")
                            st.session_state['option6a'] = salida_6
                        with col2f:
                            st_lottie(lottie_json, height=70 , key="6_lottie", reverse=False )
                        with col3f:
                            dias_6 = st.selectbox("Destination",list_activities, find_location(complete_data["route6"][1],6),key="llegada_6")
                            st.session_state['option6b'] = dias_6
                        with col4f:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_6"):
                                st.session_state['route_6'] = True
                    if st.session_state["route_6"]:
                        st.session_state["option6a"] = ""
                        st.session_state["option6b"] = ""
                        route6.empty() 
                if slider_number >= 7:
                    with route7.container():
                        col1g,col2g,col3g, col4g= st.columns([2,2,2,1])
                        with col1g:
                            salida_7 = st.selectbox("Origin",list_activities,find_location(complete_data["route7"][0],7), key="salida_7")
                            st.session_state['option7a'] = salida_7
                        with col2g:
                            st_lottie(lottie_json, height=70 , key="7_lottie", reverse=False )
                        with col3g:
                            dias_7 = st.selectbox("Destination",list_activities, find_location(complete_data["route7"][1],7),key="llegada_7")
                            st.session_state['option7b'] = dias_7
                        with col4g:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_7"):
                                st.session_state['route_7'] = True
                    if st.session_state["route_7"]:
                        st.session_state["option7a"] = ""
                        st.session_state["option7b"] = ""
                        route7.empty() 
                if slider_number >= 8:
                    with route8.container():
                        col1h,col2h,col3h, col4h= st.columns([2,2,2,1])
                        with col1h:
                            salida_8 = st.selectbox("Origin",list_activities,find_location(complete_data["route8"][0],8), key="salida_8")
                            st.session_state['option8a'] = salida_8
                        with col2h:
                            st_lottie(lottie_json, height=70 , key="8_lottie", reverse=False )
                        with col3h:
                            dias_8 = st.selectbox("Destination",list_activities,find_location(complete_data["route8"][1],8), key="llegada_8")
                            st.session_state['option8b'] = dias_8
                        with col4h:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_8"):
                                st.session_state['route_8'] = True
                    if st.session_state["route_8"]:
                        st.session_state["option8a"] = ""
                        st.session_state["option8b"] = ""
                        route8.empty() 
                if slider_number >= 9:
                    with route9.container():
                        col1i,col2i,col3i, col4i= st.columns([2,2,2,1])
                        with col1i:
                            salida_9 = st.selectbox("Origin",list_activities,find_location(complete_data["route9"][0],9), key="salida_9")
                            st.session_state['option9a'] = salida_9
                        with col2i:
                            st_lottie(lottie_json, height=70 , key="9_lottie", reverse=False )
                        with col3i:
                            dias_9 = st.selectbox("Destination",list_activities,find_location(complete_data["route9"][1],9), key="llegada_9")
                            st.session_state['option9b'] = dias_9
                        with col4i:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_9"):
                                st.session_state['route_9'] = True
                    if st.session_state["route_9"]:
                        st.session_state["option9a"] = ""
                        st.session_state["option9b"] = ""
                        route9.empty() 
                if slider_number >= 10:
                    with route10.container():
                        col1j,col2j,col3j, col4j= st.columns([2,2,2,1])
                        with col1j:
                            salida_10 = st.selectbox("Origin",list_activities,find_location(complete_data["route10"][0],10), key="salida_10")
                            st.session_state['option10a'] = salida_10
                        with col2j:
                            st_lottie(lottie_json, height=70 , key="10_lottie", reverse=False )
                        with col3j:
                            dias_10 = st.selectbox("Destination",list_activities, find_location(complete_data["route10"][1],10),key="llegada_10")
                            st.session_state['option10b'] = dias_10
                        with col4j:
                            st.markdown("Delete")
                            if st.button("Delete", key="delete_10"):
                                st.session_state['route_10'] = True
                    if st.session_state["route_10"]:
                        st.session_state["option10a"] = ""
                        st.session_state["option10b"] = ""
                        route10.empty()

            # creation of description of the route
            if slider_number >= 1 and st.session_state["route_1"] == False:
                st.subheader("Description "+st.session_state['option1a']+" to "+st.session_state['option1b'])
                with st.container():
                    coli1, coli2, coli3 =st.columns([1,1,1])
                    st.session_state.descrip_1_en = coli1.text_area("English", complete_data["route1"][2], key="descrip_1_enx")
                    st.session_state.descrip_1_de = coli2.text_area("Deutsch", complete_data["route1"][3],key="descrip_1_dex")
                    st.session_state.descrip_1_es = coli3.text_area("Spanish", complete_data["route1"][4],key="descrip_1_esx")
            if  st.session_state["route_1"] != False:
                st.session_state.descrip_1_en = ""
                st.session_state.descrip_1_de = ""
                st.session_state.descrip_1_es = ""
                
            if slider_number >= 2 and st.session_state["route_2"] == False:
                st.subheader("Description "+st.session_state['option2a']+" to "+st.session_state['option2b'])
                with st.container():
                    coli1a, coli2a, coli3a =st.columns([1,1,1])
                    st.session_state.descrip_2_en = coli1a.text_area("English",complete_data["route2"][2], key="descrip_2_enx")
                    st.session_state.descrip_2_de = coli2a.text_area("Deutsch",complete_data["route2"][3], key="descrip_2_dex")
                    st.session_state.descrip_2_es = coli3a.text_area("Spanish",complete_data["route2"][4], key="descrip_2_esx")
            if  st.session_state["route_2"] != False:
                st.session_state.descrip_2_en = ""
                st.session_state.descrip_2_de = ""
                st.session_state.descrip_2_es = ""
                
            if slider_number >= 3 and st.session_state["route_3"] == False:
                st.subheader("Description "+st.session_state['option3a']+" to "+st.session_state['option3b'])
                with st.container():
                    coli1b, coli2b, coli3b =st.columns([1,1,1])
                    st.session_state.descrip_3_en = coli1b.text_area("English",complete_data["route3"][2], key="descrip_3_enx")
                    st.session_state.descrip_3_de = coli2b.text_area("Deutsch",complete_data["route3"][3], key="descrip_3_dex")
                    st.session_state.descrip_3_es = coli3b.text_area("Spanish",complete_data["route3"][4], key="descrip_3_esx")
            if  st.session_state["route_3"] != False:
                st.session_state.descrip_3_en = ""
                st.session_state.descrip_3_de = ""
                st.session_state.descrip_3_es = ""
                
            if slider_number >= 4 and st.session_state["route_4"] == False:
                st.subheader("Description "+st.session_state['option4a']+" to "+st.session_state['option4b'])
                with st.container():
                    coli1c, coli2c, coli3c =st.columns([1,1,1])
                    st.session_state.descrip_4_en = coli1c.text_area("English", complete_data["route4"][2],key="descrip_4_enx")
                    st.session_state.descrip_4_de = coli2c.text_area("Deutsch", complete_data["route4"][3], key="descrip_4_dex")
                    st.session_state.descrip_4_es = coli3c.text_area("Spanish", complete_data["route4"][4],key="descrip_4_esx")
            if  st.session_state["route_4"] != False:
                st.session_state.descrip_4_en = ""
                st.session_state.descrip_4_de = ""
                st.session_state.descrip_4_es = ""
                
            if slider_number >= 5 and st.session_state["route_5"] == False:
                st.subheader("Description "+st.session_state['option5a']+" to "+st.session_state['option5b'])
                with st.container():
                    coli1d, coli2d, coli3d =st.columns([1,1,1])
                    st.session_state.descrip_5_en = coli1d.text_area("English",complete_data["route5"][2], key="descrip_5_enx")
                    st.session_state.descrip_5_de = coli2d.text_area("Deutsch",complete_data["route5"][3], key="descrip_5_dex")
                    st.session_state.descrip_5_es = coli3d.text_area("Spanish",complete_data["route5"][4], key="descrip_5_esx")      
            if  st.session_state["route_5"] != False:
                st.session_state.descrip_5_en = ""
                st.session_state.descrip_5_de = ""
                st.session_state.descrip_5_es = ""
                
            if slider_number >= 6 and st.session_state["route_6"] == False:
                st.subheader("Description "+st.session_state['option6a']+" to "+st.session_state['option6b'])
                with st.container():
                    coli1e, coli2e, coli3e =st.columns([1,1,1])
                    st.session_state.descrip_6_en = coli1e.text_area("English",complete_data["route6"][2], key="descrip_6_enx")
                    st.session_state.descrip_6_de = coli2e.text_area("Deutsch",complete_data["route6"][3], key="descrip_6_dex")
                    st.session_state.descrip_6_es = coli3e.text_area("Spanish",complete_data["route6"][4], key="descrip_6_esx")  
            if  st.session_state["route_6"] != False:
                st.session_state.descrip_6_en = ""
                st.session_state.descrip_6_de = ""
                st.session_state.descrip_6_es = ""
                
            if slider_number >= 7 and st.session_state["route_7"] == False:
                st.subheader("Description "+st.session_state['option7a']+" to "+st.session_state['option7b'])
                with st.container():
                    coli1f, coli2f, coli3f =st.columns([1,1,1])
                    st.session_state.descrip_7_en = coli1f.text_area("English",complete_data["route7"][2], key="descrip_7_enx")
                    st.session_state.descrip_7_de = coli2f.text_area("Deutsch",complete_data["route7"][3], key="descrip_7_dex")
                    st.session_state.descrip_7_es = coli3f.text_area("Spanish",complete_data["route7"][4], key="descrip_7_esx")  
            if  st.session_state["route_7"] != False:
                st.session_state.descrip_7_en = ""
                st.session_state.descrip_7_de = ""
                st.session_state.descrip_7_es = ""
                
            if slider_number >= 8 and st.session_state["route_8"] == False:
                st.subheader("Description "+st.session_state['option8a']+" to "+st.session_state['option8b'])
                with st.container():
                    coli1g, coli2g, coli3g =st.columns([1,1,1])
                    st.session_state.descrip_8_en = coli1g.text_area("English",complete_data["route8"][2], key="descrip_8_enx")
                    st.session_state.descrip_8_de = coli2g.text_area("Deutsch",complete_data["route8"][3], key="descrip_8_dex")
                    st.session_state.descrip_8_es = coli3g.text_area("Spanish",complete_data["route8"][4], key="descrip_8_esx")  
            if  st.session_state["route_8"] != False:
                st.session_state.descrip_8_en = ""
                st.session_state.descrip_8_de = ""
                st.session_state.descrip_8_es = ""
                
            if slider_number >= 9 and st.session_state["route_9"] == False:
                st.subheader("Description "+st.session_state['option9a']+" to "+st.session_state['option9b'])
                with st.container():
                    coli1h, coli2h, coli3h =st.columns([1,1,1])
                    st.session_state.descrip_9_en = coli1h.text_area("English",complete_data["route9"][2], key="descrip_9_enx")
                    st.session_state.descrip_9_de = coli2h.text_area("Deutsch",complete_data["route9"][3], key="descrip_9_dex")
                    st.session_state.descrip_9_es = coli3h.text_area("Spanish",complete_data["route9"][4], key="descrip_9_esx")  
            if  st.session_state["route_9"] != False:
                st.session_state.descrip_9_en = ""
                st.session_state.descrip_9_de = ""
                st.session_state.descrip_9_es = ""
                
            if slider_number >= 10 and st.session_state["route_10"] == False:
                st.subheader("Description "+st.session_state['option10a']+" to "+st.session_state['option10b'])
                with st.container():
                    coli1i, coli2i, coli3i =st.columns([1,1,1])
                    st.session_state.descrip_10_en = coli1i.text_area("English",complete_data["route10"][2], key="descrip_10_enx")
                    st.session_state.descrip_10_de = coli2i.text_area("Deutsch",complete_data["route10"][3], key="descrip_10_dex")
                    st.session_state.descrip_10_es = coli3i.text_area("Spanish",complete_data["route10"][4], key="descrip_10_esx")  
            if  st.session_state["route_10"] != False:
                st.session_state.descrip_10_en = ""
                st.session_state.descrip_10_de = ""
                st.session_state.descrip_10_es = ""
            
            st.subheader("Meals included")
            cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
            breakfast = cole1.checkbox('Breakfast', value=complete_data["breakfast"])
            lunch = cole2.checkbox('Lunch', value=complete_data["lunch"])
            dinner = cole3.checkbox('Dinner', value=complete_data["dinner"])
            other = cole4.checkbox('Other (please describe in meal notes)', value=complete_data["other"])
            st.subheader("Meal notes")
            as1,as2,as3 =st.columns([1,1,1])
            
            notes_en = as1.text_area("English", value=complete_data["meal notes ingles"])
            notes_de = as2.text_area("Deutsch", value=complete_data["meal notes aleman"])
            notes_es = as3.text_area("Spanish", value=complete_data["meal notes espanol"])
            
            # put the prices
            @st.cache()
            def get_data(filas):
                incluir = np.arange(1,filas+1)
                values = [0]*(filas)
                df = pd.DataFrame(
                    {"Amount of People": incluir,"Price Adults":values,"Price Kids":values}
                )
                return df
            
            def get_data_b(filas, adult_prices, kid_prices):
                
                incluir = np.arange(1,filas+1)
                cantidad_filas_data = len(adult_prices)
                values_1 = adult_prices + [0]*(filas-cantidad_filas_data)
                values_2 = kid_prices + [0]*(filas-cantidad_filas_data)
                
                df = pd.DataFrame(
                    {"Amount of People": incluir,"Price Adults":values_1,"Price Kids":values_2}
                )
                return df
                
            st.subheader("Prices")
            
            
            lista = [complete_data["fixed price"],complete_data["adults and kids"]]  
            indice=0
            for x in lista:
                if x!=False:
                    break
                indice+=1
                
            elegir_precio = st.radio("Choose the price",["Fixed Price","Adults and Kids"],horizontal=True, index=indice)
            precios_fijos = False
            precios_adultos = False
            precios_kids = False
            
            
            col1,col2 = st.columns([2,1])
            if elegir_precio == "Fixed Price" and complete_data["fixed price"]==False:
                precios_fijos = col1.number_input("Price", key="price_fixed")
            if elegir_precio == "Fixed Price" and complete_data["fixed price"]!=False:
                precios_fijos = col1.number_input("Price", key="price_fixed_1",value=complete_data["fixed price"], step=1)
            
            
            
            if elegir_precio == "Adults and Kids" and complete_data["adults and kids"]==False:
                with col1:
                    st.subheader("Prices to adults and kids")
                    numero_filas_k = st.slider("Number of people",1,15,step=1, value=5, key="adults_kids_slider")
                    
                    data_k = get_data(numero_filas_k)
                    gb_k = GridOptionsBuilder.from_dataframe(data_k)
                    #make all columns editable
                    gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                    go_k = gb_k.build()
                    
                    ag_k = AgGrid(
                        data_k, 
                        gridOptions=go_k, 
                        # height=300, 
                        fit_columns_on_grid_load=True,
                        theme= "light" # or "streamlit","light","balham","material"
                    )
                    # st.subheader("Returned Data")
                    # st.dataframe(ag_k['data'])
                    
                    df_prices_kids = ag_k["data"]
                    # st.dataframe(ag['data'])
                    df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                    df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                    df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                    
                    df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                    df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                    df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                    precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                    # st.write(precios_kids)
                    
            if elegir_precio == "Adults and Kids" and complete_data["adults and kids"]!=False:
                with col1:
                    st.subheader("Prices to adults and kids")
                    elementos_data = len(complete_data["adults and kids"][1])
                    numero_filas_k = st.slider("Number of people",elementos_data,15,step=1, value=elementos_data, key="adults_kids_slider")
                    
                    data_k = get_data_b(numero_filas_k, complete_data["adults and kids"][1], complete_data["adults and kids"][2])
                    gb_k = GridOptionsBuilder.from_dataframe(data_k)
                    #make all columns editable
                    gb_k.configure_columns(["Amount of People","Price Adults","Price Kids"], editable=True)
                    go_k = gb_k.build()
                    
                    ag_k = AgGrid(
                        data_k, 
                        gridOptions=go_k, 
                        # height=300, 
                        fit_columns_on_grid_load=True,
                        theme= "light" # or "streamlit","light","balham","material"
                    )
                    # st.subheader("Returned Data")
                    # st.dataframe(ag_k['data'])
                     
                    df_prices_kids = ag_k["data"]
                    # st.dataframe(ag['data'])
                    df_prices_1k = df_prices_kids["Amount of People"].values.tolist()
                    df_prices_2k = df_prices_kids["Price Adults"].values.tolist()
                    df_prices_3k = df_prices_kids["Price Kids"].values.tolist()
                    
                    df_prices_1k = [x for x in df_prices_1k if str(x) != 'nan']
                    df_prices_2k = [x for x in df_prices_2k if str(x) != 'nan']
                    df_prices_3k = [x for x in df_prices_3k if str(x) != 'nan']
                    precios_kids = [df_prices_1k,df_prices_2k,df_prices_3k]
                    # st.write(precios_kids)
# 
            st.subheader("Operator")
            operator = st.text_input("Service provider", complete_data["operator"])
            st.subheader("Internal Pricing Notes (not shown to the traveler)")
            notes_precio = st.text_area("Internal Pricing Notes", complete_data["notes price"])

            cargar_data = st.button("Save all data")
            # algoritmo para ordenar los datos de llenos a vacios.
            llenos = []
            vacios = []
            if cargar_data:
                with st.spinner('Uploading...'):
                    for y in range(1,11):
                        if st.session_state["option"+str(y)+"a"] =="":
                            vacios.append(y)
                        else:
                            llenos.append(y)
                    data_final = llenos + vacios
            # fin 
                    
                    # redefinir las variables de las rutas y definicioes para cada valor del 1-10
                    st.session_state["option1a"] = st.session_state["option"+str(data_final[0])+"a"]
                    st.session_state["option1b"] = st.session_state["option"+str(data_final[0])+"b"]
                    descrip_a1 = st.session_state["descrip_"+str(data_final[0])+"_en"]
                    descrip_b1 = st.session_state["descrip_"+str(data_final[0])+"_de"] 
                    descrip_c1 = st.session_state["descrip_"+str(data_final[0])+"_es"]
                    
                    st.session_state["option2a"] = st.session_state["option"+str(data_final[1])+"a"]
                    st.session_state["option2b"] = st.session_state["option"+str(data_final[1])+"b"]
                    descrip_a2 = st.session_state["descrip_"+str(data_final[1])+"_en"]
                    descrip_b2 = st.session_state["descrip_"+str(data_final[1])+"_de"] 
                    descrip_c2 = st.session_state["descrip_"+str(data_final[1])+"_es"]
                    
                    
                    
                    collection = db["transport"]
                    
                    # In this section you can add new activities to the database
                    # para cada route o ruta we put  the data in the following order : [lugar de salida, lugar de llegada, descripcion ingles, descripcion aleman, descripcion espanol]
                    
                    record = {
                    "Name_en": name_en,
                    "route1": [st.session_state["option"+str(data_final[0])+"a"],st.session_state["option"+str(data_final[0])+"b"], st.session_state["descrip_"+str(data_final[0])+"_en"],st.session_state["descrip_"+str(data_final[0])+"_de"] , st.session_state["descrip_"+str(data_final[0])+"_es"]], 
                    "route2": [st.session_state["option"+str(data_final[1])+"a"],st.session_state["option"+str(data_final[1])+"b"], st.session_state["descrip_"+str(data_final[1])+"_en"],st.session_state["descrip_"+str(data_final[1])+"_de"] , st.session_state["descrip_"+str(data_final[1])+"_es"]], 
                    "route3": [st.session_state["option"+str(data_final[2])+"a"],st.session_state["option"+str(data_final[2])+"b"], st.session_state["descrip_"+str(data_final[2])+"_en"],st.session_state["descrip_"+str(data_final[2])+"_de"] , st.session_state["descrip_"+str(data_final[2])+"_es"]], 
                    "route4": [st.session_state["option"+str(data_final[3])+"a"],st.session_state["option"+str(data_final[3])+"b"], st.session_state["descrip_"+str(data_final[3])+"_en"],st.session_state["descrip_"+str(data_final[3])+"_de"] , st.session_state["descrip_"+str(data_final[3])+"_es"]],
                    "route5": [st.session_state["option"+str(data_final[4])+"a"],st.session_state["option"+str(data_final[4])+"b"], st.session_state["descrip_"+str(data_final[4])+"_en"],st.session_state["descrip_"+str(data_final[4])+"_de"] , st.session_state["descrip_"+str(data_final[4])+"_es"]],
                    "route6": [st.session_state["option"+str(data_final[5])+"a"],st.session_state["option"+str(data_final[5])+"b"], st.session_state["descrip_"+str(data_final[5])+"_en"],st.session_state["descrip_"+str(data_final[5])+"_de"] , st.session_state["descrip_"+str(data_final[5])+"_es"]],
                    "route7": [st.session_state["option"+str(data_final[6])+"a"],st.session_state["option"+str(data_final[6])+"b"], st.session_state["descrip_"+str(data_final[6])+"_en"],st.session_state["descrip_"+str(data_final[6])+"_de"] , st.session_state["descrip_"+str(data_final[6])+"_es"]],
                    "route8": [st.session_state["option"+str(data_final[7])+"a"],st.session_state["option"+str(data_final[7])+"b"], st.session_state["descrip_"+str(data_final[7])+"_en"],st.session_state["descrip_"+str(data_final[7])+"_de"] , st.session_state["descrip_"+str(data_final[7])+"_es"]],
                    "route9": [st.session_state["option"+str(data_final[8])+"a"],st.session_state["option"+str(data_final[8])+"b"], st.session_state["descrip_"+str(data_final[8])+"_en"],st.session_state["descrip_"+str(data_final[8])+"_de"] , st.session_state["descrip_"+str(data_final[8])+"_es"]],
                    "route10": [st.session_state["option"+str(data_final[9])+"a"],st.session_state["option"+str(data_final[9])+"b"], st.session_state["descrip_"+str(data_final[9])+"_en"],st.session_state["descrip_"+str(data_final[9])+"_de"] , st.session_state["descrip_"+str(data_final[9])+"_es"]],
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner,
                    "other": other,
                    "meal notes ingles": notes_en,
                    "meal notes aleman": notes_de,
                    "meal notes espanol": notes_es,
                    "fixed price": precios_fijos,
                    "adults and kids" : precios_kids,
                    "operator" : operator,
                    "notes price":notes_precio
                    }
                    
                    collection.insert_one(record)
                    # poner las variables en su estado inicial
                    st.session_state["option1a"] = ""
                    st.session_state["option2a"] = ""
                    st.session_state["option3a"] = ""
                    st.session_state["option4a"] = ""
                    st.session_state["option5a"] = ""
                    st.session_state["option6a"] = ""
                    st.session_state["option7a"] = ""
                    st.session_state["option8a"] = ""
                    st.session_state["option9a"] = ""
                    st.session_state["option10a"] = ""
                    
                    st.session_state["option1b"] = ""
                    st.session_state["option2b"] = ""
                    st.session_state["option3b"] = ""
                    st.session_state["option4b"] = ""
                    st.session_state["option5b"] = ""
                    st.session_state["option6b"] = ""
                    st.session_state["option7b"] = ""
                    st.session_state["option8b"] = ""
                    st.session_state["option9b"] = ""
                    st.session_state["option10b"] = ""
                
                    st.session_state["descrip_1_en"] = ""
                    st.session_state["descrip_1_de"] = ""
                    st.session_state["descrip_1_es"] = ""
                    st.session_state["descrip_2_en"] = ""
                    st.session_state["descrip_2_de"] = ""
                    st.session_state["descrip_2_es"] = ""
                    st.session_state["descrip_3_en"] = ""
                    st.session_state["descrip_3_de"] = ""
                    st.session_state["descrip_3_es"] = ""
                    st.session_state["descrip_4_en"] = ""
                    st.session_state["descrip_4_de"] = ""
                    st.session_state["descrip_4_es"] = ""
                    st.session_state["descrip_5_en"] = ""
                    st.session_state["descrip_5_de"] = ""
                    st.session_state["descrip_5_es"] = ""
                    st.session_state["descrip_6_en"] = ""
                    st.session_state["descrip_6_de"] = ""
                    st.session_state["descrip_6_es"] = ""
                    st.session_state["descrip_7_en"] = ""
                    st.session_state["descrip_7_de"] = ""
                    st.session_state["descrip_7_es"] = ""
                    st.session_state["descrip_8_en"] = ""
                    st.session_state["descrip_8_de"] = ""
                    st.session_state["descrip_8_es"] = ""
                    st.session_state["descrip_9_en"] = ""
                    st.session_state["descrip_9_de"] = ""
                    st.session_state["descrip_9_es"] = ""
                    st.session_state["descrip_10_en"] = ""
                    st.session_state["descrip_10_de"] = ""
                    st.session_state["descrip_10_es"] = ""
                
                    st.session_state['route_1'] = False
                    st.session_state['route_2'] = False
                    st.session_state['route_3'] = False
                    st.session_state['route_4'] = False
                    st.session_state['route_5'] = False
                    st.session_state['route_6'] = False
                    st.session_state['route_7'] = False
                    st.session_state['route_8'] = False
                    st.session_state['route_9'] = False
                    st.session_state['route_10'] = False
                    
                    st.success('Upload successful!')        
        
        if opciones == "Delete":
            st.subheader("Delete a transport")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["transport"]
            data = collection.find({},{"Name_en":1, "operator":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"] + "  (" + value["operator"]+ ")")
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad = st.selectbox("Choose the transport",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            
            if st.button("Delete all"):
                with st.spinner('Deleting...'):    
                    order_activity = list_activities.index(elegir_actividad)
                    code = ids_activities[order_activity]
                    # delete activity in mongodb
                    collection.delete_one({"_id": ObjectId(code)})
                    st.info("Deleted")
    ##################
    # Accommodation 
    ##################
    
    if menu == "Accommodations":
        
        opciones = st.sidebar.radio("Option",["Create new","Edit","Delete"], key="accommodations_key")
        if opciones == "Create new":
            st.subheader("Create a new accommodation")
            col1, col2 = st.columns((1.5,1))
            with col1:
                name_en = st.text_input("Name in english")
                name_de = st.text_input("Name in deutsch")
                name_es = st.text_input("Name in español")
                
                # Put the prices
                @st.cache()
                def get_data():
                    incluir = np.arange(1)
                    values = [0]*(1)
                    df = pd.DataFrame(
                        {"Single": incluir,"Double":values,"Triple":values}
                    )
                    return df
                
                precios_kids = False
                st.subheader("Prices")
                st.markdown('* These prices are for a maximum of 3 people per room and per night')
                st.markdown('* Also this prices are just optional, you can change them later')
                
                data_k = get_data()
                gb_k = GridOptionsBuilder.from_dataframe(data_k)
                #make all columns editable
                gb_k.configure_columns(["Single","Double","Triple"], editable=True)
                go_k = gb_k.build()
                
                ag_k = AgGrid(
                    data_k, 
                    gridOptions=go_k, 
                    height=93, 
                    fit_columns_on_grid_load=True,
                    theme= "light" # or "streamlit","light","balham","material"
                )
                # st.subheader("Returned Data")
                # st.dataframe(ag_k['data'])
                
                df_prices_kids = ag_k["data"]
                # st.dataframe(ag['data'])
                df_prices_1k = float(df_prices_kids["Single"].values)
                df_prices_2k = float(df_prices_kids["Double"].values)
                df_prices_3k = float(df_prices_kids["Triple"].values)
                
                precios = [df_prices_1k,df_prices_2k,df_prices_3k]
                # st.write(precios)
                st.subheader("Image")
                uploaded_files = st.file_uploader("Select 1 image")
                if uploaded_files!=None:
                    st.image(uploaded_files, use_column_width="auto",output_format="PNG")

                    
            with col2:
                # lista de las locations
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection_location = db["locations"]
                data = collection_location.find({},{"Name_en":1})
                
                list_activities = []
                for value in data:
                    list_activities.append(value["Name_en"])
                # fin
                lugares = st.multiselect("Choose the location",list_activities)
                lista = ["1 ★", "2 ★★", "3 ★★★", "4 ★★★★", "5 ★★★★★"]
                calidad = st.selectbox("Choose the hotel rating",lista)
                estrellas = lista.index(calidad)+1
                
            
            if st.button("Save data"):
                with st.spinner('Saving...'):
                    title_separate = name_en.replace(" ", "_")
                    image_1 = title_separate+".png"
                    
                    collection = db["accommodations"]
                    
                    # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                    uploadimageToS3(uploaded_files,bucket_name , image_1)
                    
                    # In this section you can add new activities to the database
                    # para cada route o ruta we put  the data in the following order : [lugar de salida, lugar de llegada, descripcion ingles, descripcion aleman, descripcion espanol]
                    
                    record = {
                    "Name_en": name_en,
                    "Name_de": name_de,
                    "Name_es": name_es,
                    "location": lugares,
                    "rating": estrellas,
                    "imagen": image_1,
                    "prices": precios
                    }
                    
                    collection.insert_one(record)
                    st.success('Upload successful!')
        
        if opciones == "Edit":
            
            st.subheader("Edit an accommodation")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["accommodations"]
            data = collection.find({},{"Name_en":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"])
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad = st.selectbox("Choose the transport",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            st.subheader("Change values")
            col1, col2 = st.columns((2,1))
            with col1:
                name_en = st.text_input("Name in english", complete_data["Name_en"])
                name_de = st.text_input("Name in deutsch", complete_data["Name_de"])
                name_es = st.text_input("Name in español", complete_data["Name_es"])
                # Put the prices
                @st.cache()
                def get_data():
                    incluir = np.arange(1)
                    values = complete_data["prices"][0]
                    values_2 = complete_data["prices"][1]
                    values_3 = complete_data["prices"][2]
                    df = pd.DataFrame(
                        {"Single": [values],"Double":[values_2],"Triple":[values_3]}
                    )
                    return df
                
                precios_kids = False
                
                st.subheader("Prices")
                st.markdown('* These prices are for a maximum of 3 people per room and per night')
                st.markdown('* Also this prices are just optional, you can change them later')
                
                data_k = get_data()
                gb_k = GridOptionsBuilder.from_dataframe(data_k)
                #make all columns editable
                gb_k.configure_columns(["Single","Double","Triple"], editable=True)
                go_k = gb_k.build()
                
                ag_k = AgGrid(
                    data_k, 
                    gridOptions=go_k, 
                    height=93, 
                    fit_columns_on_grid_load=True,
                    theme= "light" # or "streamlit","light","balham","material"
                )
                # st.subheader("Returned Data")
                # st.dataframe(ag_k['data'])
                
                df_prices_kids = ag_k["data"]
                # st.dataframe(ag['data'])
                df_prices_1k = float(df_prices_kids["Single"].values)
                df_prices_2k = float(df_prices_kids["Double"].values)
                df_prices_3k = float(df_prices_kids["Triple"].values)
                
                precios = [df_prices_1k,df_prices_2k,df_prices_3k]

                st.subheader("Image")
                st.image(get_link(bucket_name, complete_data["imagen"]), width=500 )
                uploaded_file = st.file_uploader("Upload new image")
                if uploaded_file!=None:
                    st.subheader("New image")
                    st.image(uploaded_file, width = 500 ,output_format="PNG")
                    
                    
            with col2:
                # lista de las locations
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection_location = db["locations"]
                data = collection_location.find({},{"Name_en":1})
                
                list_activities = []
                for value in data:
                    list_activities.append(value["Name_en"])
                # fin
                lugares = st.multiselect("Choose the location",list_activities, default=complete_data["location"])
                lista = ["1 ★", "2 ★★", "3 ★★★", "4 ★★★★", "5 ★★★★★"]
                calidad = st.selectbox("Choose the hotel rating",lista, index=complete_data["rating"])
                estrellas = lista.index(calidad)+1
            
            
            
            
            
            if st.button("Save"):
                # reemplazar los espacios por guiones bajos
                title_separate = name_en.replace(" ", "_")
                
                if name_en== complete_data["Name_en"]:
                    with st.spinner('Uploading...'):
                        
                        image_1 = title_separate+".png"
                        
                        ############################
                        # Connection to MongoDB
                        ############################
                        
                        record = {
                        "Name_en": name_en,
                        "Name_de": name_de,
                        "Name_es": name_es,
                        "location": lugares,
                        "rating": estrellas,
                        "imagen": image_1,
                        "prices": precios
                        }
                        
                        
                        collection.update_one({"_id":code},{"$set":record})
                        if uploaded_file is not None:
                                uploadimageToS3(uploaded_file,bucket_name , image_1)
                        st.success("Data updated")
                
                if name_en!= complete_data["Name_en"]:
                    with st.spinner('Uploading...'):
                        
                        image_1 = title_separate+".png"
                        
                        ############################
                        # Connection to MongoDB
                        ############################
                        
                        record = {
                        "Name_en": name_en,
                        "Name_de": name_de,
                        "Name_es": name_es,
                        "location": lugares,
                        "rating": estrellas,
                        "imagen": image_1,
                        "prices": precios
                        }
                        
                        collection.update_one({"_id":code},{"$set":record})
                        # working with s3
                        
                        copy_and_delete_s3_file(bucket_name, complete_data["imagen"], image_1)
                        delete_s3_file(bucket_name, complete_data["imagen"])
                        
                        # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
                        if uploaded_file is not None:
                            uploadimageToS3(uploaded_file,bucket_name , image_1)
                        st.success("Data updated")
                
        ########################
        # Delete a location
        ########################
        if opciones == "Delete":
            st.subheader("Delete an accommodation")
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["accommodations"]
            data = collection.find({},{"Name_en":1, "_id":1})
            names = []
            list_activities_1 = [""]
            ids_activities = [""]
            for value in data:
                names.append(value["Name_en"])
                list_activities_1.append(value["Name_en"])
                ids_activities.append(value["_id"])
            # FIN 
            elegir_actividad_1 = st.selectbox("Choose the activity",list_activities_1)
            if elegir_actividad_1 == "":
                st.stop()
                
            
            order_activity = list_activities_1.index(elegir_actividad_1)
            code = ids_activities[order_activity]
            
            complete_data = collection.find_one({"_id":code})
            
            title = st.header(complete_data["Name_en"])
            
            c1, c2 = st.columns(2)
        
            bucket_name = "peruviansunrise-storage"
            
            url_1 = get_link(bucket_name, complete_data["imagen"])
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            
            lugares = c1.multiselect("Choose the location",list_activities, default=complete_data["location"])
            lista = ["1 ★", "2 ★★", "3 ★★★", "4 ★★★★", "5 ★★★★★"]
            calidad = c1.selectbox("Choose the hotel rating",lista, index=complete_data["rating"])
            c2.image(url_1, use_column_width="auto", width=400)
            
            
            if st.button("Delete"):
                with st.spinner('Deleting...'):  
                    collection = db["accommodations"]  
                    order_activity = list_activities_1.index(elegir_actividad_1)
                    code = ids_activities[order_activity]
                    # delete activity in mongodb
                    
                    collection.delete_one({"_id": ObjectId(code)})
                    # ---
                    # delete activity in s3
                    title = complete_data["Name_en"]
                    title_separate = title.replace(" ", "_")
                    image_1 = title_separate+".png"
                    try:
                        delete_s3_file(bucket_name,image_1)
                        
                        st.success("Activity deleted")
                    # ---
                    except: 
                        st.error("Error deleting images")
                    
    ########################
    # Create a bundle
    ########################
    if menu == "Bundle":
        activities_option = st.sidebar.radio("Option",["Create new","Edit","Delete"], key="bundle_options")
        if activities_option == "Create new":
            
            st.subheader("Create a new bundle")
            
            name_en = st.text_input("Name in English")
            name_de = st.text_input("Name in German")
            name_es = st.text_input("Name in Spanish")
        
            if 'data_location' not in st.session_state:
                st.session_state.data_location = [] #!esto debe de estar asi o generara errores, cuidado!
            if "lugares_pasado" not in st.session_state:
                st.session_state.lugares_pasado = [""]
        
            def update_all():
                st.session_state.bundlelocation = st.session_state.data_location
                
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            lugares = st.multiselect("Choose the location",list_activities, key= "lugarcitos", on_change=update_all)
            if lugares == []:
                st.stop()
            st.session_state.lugares_actual = lugares
            
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["activities"]
            data = collection.find({},{"Name_en":1, "Operator":1,"_id":1, "Location":1})
            
            list_activities = [""]
            ids_activities = [""]
            transporte = [""]

            for value in data:
                g = [i for i in value["Location"] if i in lugares]
                if len(g) > 0:
                    list_activities.append(value["Name_en"] + " (" + value["Operator"]+ ")")
                    ids_activities.append(value["_id"])
                    transporte.append("X")
            
            # Pedir datos de mongo db para  obtener los nombres de los transportes
            collection = db["transport"]
            data = collection.find({},{"Name_en":1, "operator":1,"_id":1, "route1":1, "route2":1, "route3":1, "route4":1, "route5":1, "route6":1, "route7":1, "route8":1, "route9":1, "route10":1})
            for value in data:
                
                g1 = [i for i in value["route1"] if i in lugares]
                g2 = [i for i in value["route2"] if i in lugares]
                g3 = [i for i in value["route3"] if i in lugares]
                g4 = [i for i in value["route4"] if i in lugares]
                g5 = [i for i in value["route5"] if i in lugares]
                g6 = [i for i in value["route6"] if i in lugares]
                g7 = [i for i in value["route7"] if i in lugares]
                g8 = [i for i in value["route8"] if i in lugares]
                g9 = [i for i in value["route9"] if i in lugares]
                g10 = [i for i in value["route10"] if i in lugares]
                final = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9 + g10
                if len(final)>0:
                    list_activities.append(value["route1"][0]+" --> "+value["route1"][1]+" (" + value["operator"]+ ")") 
                    transporte.append(value["route1"][0]+" to "+value["route1"][1]) 
                    ids_activities.append(value["_id"])
                    if len(final)>=2:
                        list_activities.append(value["route2"][0]+" --> "+value["route2"][1]+" (" + value["operator"]+ ")") 
                        transporte.append(value["route2"][0]+" to "+value["route2"][1]) 
                        ids_activities.append(value["_id"])
                        if len(final)>=3:
                            list_activities.append(value["route3"][0]+" --> "+value["route3"][1]+" (" + value["operator"]+ ")") 
                            transporte.append(value["route3"][0]+" to "+value["route3"][1]) 
                            ids_activities.append(value["_id"])
                            if len(final)>=4:
                                list_activities.append(value["route4"][0]+" --> "+value["route4"][1]+" (" + value["operator"]+ ")") 
                                transporte.append(value["route4"][0]+" to "+value["route4"][1]) 
                                ids_activities.append(value["_id"])
                                if len(final)>=5:
                                    list_activities.append(value["route5"][0]+" --> "+value["route5"][1]+" (" + value["operator"]+ ")") 
                                    transporte.append(value["route5"][0]+" to "+value["route5"][1]) 
                                    ids_activities.append(value["_id"])
                                    if len(final)>=6:
                                        list_activities.append(value["route6"][0]+" --> "+value["route6"][1]+" (" + value["operator"]+ ")") 
                                        transporte.append(value["route6"][0]+" to "+value["route6"][1]) 
                                        ids_activities.append(value["_id"])
                                        if len(final)>=7:
                                            list_activities.append(value["route7"][0]+" --> "+value["route7"][1]+" (" + value["operator"]+ ")") 
                                            transporte.append(value["route7"][0]+" to "+value["route7"][1]) 
                                            ids_activities.append(value["_id"])
                                            if len(final)>=8:
                                                list_activities.append(value["route8"][0]+" --> "+value["route8"][1]+" (" + value["operator"]+ ")") 
                                                transporte.append(value["route8"][0]+" to "+value["route8"][1]) 
                                                ids_activities.append(value["_id"])
                                                if len(final)>=9:
                                                    list_activities.append(value["route9"][0]+" --> "+value["route9"][1]+" (" + value["operator"]+ ")") 
                                                    transporte.append(value["route9"][0]+" to "+value["route9"][1]) 
                                                    ids_activities.append(value["_id"])
                                                    if len(final)>=10:
                                                        list_activities.append(value["route10"][0]+" --> "+value["route10"][1]+" (" + value["operator"]+ ")") 
                                                        transporte.append(value["route10"][0]+" to "+value["route10"][1]) 
                                                        ids_activities.append(value["_id"])
        
            #! Nueva forma de hacer
            
            #! Fin
            with st.expander('Select values', expanded=True):
                col1, col2 = st.columns(2)
                with col1:

                    st.subheader("Activities & Transport")
                    from streamlit_sortables import sort_items


                    original_items = list_activities
                    # sorted_items = sort_items(original_items)

                    # st.write(f'original_items: {original_items}')
                    # st.write(f'sorted_items: {sorted_items}')
                    if "data_sort" not in st.session_state:
                        st.session_state.data_sort = []
                    if "modified_sort"  not in st.session_state:
                        st.session_state.modified_sort = []
                    if "actual_sort"  not in st.session_state:
                        st.session_state.actual_sort = []

                    if "counter" not in st.session_state:
                        st.session_state.counter = 0
                        st.experimental_rerun()

                    def data_changed():
                        for x in st.session_state.actual_sort:
                            if x not in st.session_state.data_sort:
                                st.session_state.data_sort.append(x)
                        for x in st.session_state.data_sort:
                            if x not in st.session_state.actual_sort:
                                st.session_state.data_sort.remove(x)
                        st.session_state.modified_sort = st.session_state.data_sort 
                    values = st.multiselect("Select values", original_items, default= None, key="bundlelocation", on_change=data_changed )
                    st.session_state.data_location = values
                    if len(values)=="":
                            st.stop()
                
                with col2.container():
                    st.subheader("Reorder the activities")
                    st.write("Drag and drop the activities to reorder them")
                    st.session_state.counter += 1
                    st.session_state.actual_sort = values 

                    if st.session_state.actual_sort == [original_items[0]]:
                        st.write("ok")
                        sorted_items = sort_items(st.session_state.actual_sort)
                        st.session_state.data_sort = sorted_items
                    else:    
                        listita = []
                        for x in st.session_state.actual_sort:
                            if x not in st.session_state.data_sort:
                                st.session_state.modified_sort.append(x)
                        for x in st.session_state.data_sort:
                            if x not in st.session_state.actual_sort:
                                st.session_state.data_sort.remove(x)
                        sorted_items = sort_items(st.session_state.modified_sort + listita )
                        st.session_state.data_sort = sorted_items
                    # # eliminar  el "" valor inicial
                    # if st.session_state.counter==1:
                    #     del st.session_state.data_sort[0]
                    elegir_actividad = st.session_state.data_sort
            
                if elegir_actividad ==None or elegir_actividad==[]:
                    st.stop()
                
                else:
                    #! crear la funcion para crear todos los modelos de actividades 
                    def crear_actividad(data):
                        co1, co2, co3 = st.columns((2,2,1))
                        co2.subheader(data["Name_en"])
                        st.write(data["Description_en"])

                    #! crear la funcion para crear todos los modelos para el transporte
                    def crear_transporte(data, number):
                        
                        co1, co2= st.columns((0.75,2))
                        order_activity = list_activities.index(elegir_actividad[number])
                        transporte_title = transporte[order_activity]
                        co2.subheader(transporte_title)
                        st.write(data["notes price"])
                        
                        
                    for x in range(len(elegir_actividad)):
                        order_activity = list_activities.index(elegir_actividad[x])
                        code = ids_activities[order_activity]
                        
                        collection = db["activities"]
                        complete_data = collection.find_one({"_id":code})
                        # en este caso es una actividad
                        if complete_data != None:
                            
                            crear_actividad(complete_data)

                        if complete_data == None:
                            collection = db["transport"]
                            complete_data = collection.find_one({"_id":code})                
                            
                            crear_transporte(complete_data, x)
            
            st.subheader("Product Description")
            description_en = st.text_area("Description in English", height=100)
            description_de = st.text_area("Description in German", height=100)
            description_es = st.text_area("Description in Spanish", height=100)
            st.subheader("Meals included")
            cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
            breakfast = cole1.checkbox('Breakfast')
            lunch = cole2.checkbox('Lunch')
            dinner = cole3.checkbox('Dinner')
            other = cole4.checkbox('Other (please describe in meal notes)')
            st.subheader("Meal notes")
            as1,as2,as3 =st.columns([1,1,1])
            
            notes_en = as1.text_area("English")
            notes_de = as2.text_area("Deutsch")
            notes_es = as3.text_area("Spanish")
            
            # guardar datos
            guardar = st.button("Save bundle")
            if guardar:
                with st.spinner("Saving bundle..."):
                    collection = db["bundle"]
                    
                    # In this section you can add new activities to the database
                    # para cada route o ruta we put  the data in the following order : [lugar de salida, lugar de llegada, descripcion ingles, descripcion aleman, descripcion espanol]
                    
                    record = {
                    "Name_en": name_en,
                    "Name_de": name_de,
                    "Name_es": name_es,
                    "Places" : lugares,
                    "Items":sorted_items,
                    "Description_en": description_en,
                    "Description_de": description_de,
                    "Description_es": description_es,
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner,
                    "other": other,
                    "meal notes ingles": notes_en,
                    "meal notes aleman": notes_de,
                    "meal notes espanol": notes_es
                    }
                    
                    collection.insert_one(record)
                    
                st.success('Upload successful!')


        if activities_option=="Edit":

            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            lugar = st.multiselect("Choose the places",list_activities)

            todos = st.checkbox("All places", value=True)
            if todos:
                lugar = list_activities
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection = db["bundle"]
                data = collection.find({},{"Name_en":1,"Places":1, "_id":1})
                # filtrar los datos para que solo aparezcan los bundles que estan en el lugar seleccionado
                list_activities = [""]
                ids_activities = [""]
                for value in data:
                        list_activities.append(value["Name_en"])
                        ids_activities.append(value["_id"])
                # FIN 

            if todos == False:
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection = db["bundle"]
                data = collection.find({},{"Name_en":1,"Places":1, "_id":1})
                # filtrar los datos para que solo aparezcan los bundles que estan en el lugar seleccionado
                list_activities = [""]
                ids_activities = [""]
                for value in data:
                    for i in value["Places"]:
                        if i in lugar:
                            list_activities.append(value["Name_en"])
                            ids_activities.append(value["_id"])
                # FIN 

            elegir_actividad = st.selectbox("Choose the bundle",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            
            st.subheader("Create a new bundle")
            
            name_en = st.text_input("Name in English", value=complete_data["Name_en"])
            name_de = st.text_input("Name in German", value=complete_data["Name_de"])
            name_es = st.text_input("Name in Spanish", value=complete_data["Name_es"])
        
            if 'data_location_2' not in st.session_state:
                st.session_state.data_location_2 = [] #!esto debe de estar asi o generara errores, cuidado!
            if "lugares_pasado_2" not in st.session_state:
                st.session_state.lugares_pasado_2 = [""]
        
            def update_all():
                st.session_state.bundlelocation2 = st.session_state.data_location_2
                
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            # fin
            lugares = st.multiselect("Choose the location",list_activities, default=complete_data["Places"] ,key= "lugarcitos2", on_change=update_all)
            if lugares == []:
                st.stop()
            st.session_state.lugares_actual2 = lugares
            
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["activities"]
            data = collection.find({},{"Name_en":1, "Operator":1,"_id":1, "Location":1})
            
            list_activities = [""]
            ids_activities = [""]
            transporte = [""]

            for value in data:
                g = [i for i in value["Location"] if i in lugares]
                if len(g) > 0:
                    list_activities.append(value["Name_en"] + " (" + value["Operator"]+ ")")
                    ids_activities.append(value["_id"])
                    transporte.append("X")
            
            # Pedir datos de mongo db para  obtener los nombres de los transportes
            collection = db["transport"]
            data = collection.find({},{"Name_en":1, "operator":1,"_id":1, "route1":1, "route2":1, "route3":1, "route4":1, "route5":1, "route6":1, "route7":1, "route8":1, "route9":1, "route10":1})
            for value in data:
                
                g1 = [i for i in value["route1"] if i in lugares]
                g2 = [i for i in value["route2"] if i in lugares]
                g3 = [i for i in value["route3"] if i in lugares]
                g4 = [i for i in value["route4"] if i in lugares]
                g5 = [i for i in value["route5"] if i in lugares]
                g6 = [i for i in value["route6"] if i in lugares]
                g7 = [i for i in value["route7"] if i in lugares]
                g8 = [i for i in value["route8"] if i in lugares]
                g9 = [i for i in value["route9"] if i in lugares]
                g10 = [i for i in value["route10"] if i in lugares]
                final = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9 + g10
                if len(final)>0:
                    list_activities.append(value["route1"][0]+" --> "+value["route1"][1]+" (" + value["operator"]+ ")") 
                    transporte.append(value["route1"][0]+" to "+value["route1"][1]) 
                    ids_activities.append(value["_id"])
                    if len(final)>=2:
                        list_activities.append(value["route2"][0]+" --> "+value["route2"][1]+" (" + value["operator"]+ ")") 
                        transporte.append(value["route2"][0]+" to "+value["route2"][1]) 
                        ids_activities.append(value["_id"])
                        if len(final)>=3:
                            list_activities.append(value["route3"][0]+" --> "+value["route3"][1]+" (" + value["operator"]+ ")") 
                            transporte.append(value["route3"][0]+" to "+value["route3"][1]) 
                            ids_activities.append(value["_id"])
                            if len(final)>=4:
                                list_activities.append(value["route4"][0]+" --> "+value["route4"][1]+" (" + value["operator"]+ ")") 
                                transporte.append(value["route4"][0]+" to "+value["route4"][1]) 
                                ids_activities.append(value["_id"])
                                if len(final)>=5:
                                    list_activities.append(value["route5"][0]+" --> "+value["route5"][1]+" (" + value["operator"]+ ")") 
                                    transporte.append(value["route5"][0]+" to "+value["route5"][1]) 
                                    ids_activities.append(value["_id"])
                                    if len(final)>=6:
                                        list_activities.append(value["route6"][0]+" --> "+value["route6"][1]+" (" + value["operator"]+ ")") 
                                        transporte.append(value["route6"][0]+" to "+value["route6"][1]) 
                                        ids_activities.append(value["_id"])
                                        if len(final)>=7:
                                            list_activities.append(value["route7"][0]+" --> "+value["route7"][1]+" (" + value["operator"]+ ")") 
                                            transporte.append(value["route7"][0]+" to "+value["route7"][1]) 
                                            ids_activities.append(value["_id"])
                                            if len(final)>=8:
                                                list_activities.append(value["route8"][0]+" --> "+value["route8"][1]+" (" + value["operator"]+ ")") 
                                                transporte.append(value["route8"][0]+" to "+value["route8"][1]) 
                                                ids_activities.append(value["_id"])
                                                if len(final)>=9:
                                                    list_activities.append(value["route9"][0]+" --> "+value["route9"][1]+" (" + value["operator"]+ ")") 
                                                    transporte.append(value["route9"][0]+" to "+value["route9"][1]) 
                                                    ids_activities.append(value["_id"])
                                                    if len(final)>=10:
                                                        list_activities.append(value["route10"][0]+" --> "+value["route10"][1]+" (" + value["operator"]+ ")") 
                                                        transporte.append(value["route10"][0]+" to "+value["route10"][1]) 
                                                        ids_activities.append(value["_id"])
        
            #! Nueva forma de hacer
            
            #! Fin
            with st.expander('Select values', expanded=True):
                col1, col2 = st.columns(2)
                with col1:

                    st.subheader("Activities & Transport")
                    from streamlit_sortables import sort_items


                    original_items = list_activities
                    # sorted_items = sort_items(original_items)

                    # st.write(f'original_items: {original_items}')
                    # st.write(f'sorted_items: {sorted_items}')
                    if "data_sort2" not in st.session_state:
                        st.session_state.data_sort2 = []
                    if "modified_sort2"  not in st.session_state:
                        st.session_state.modified_sort2 = []
                    if "actual_sort2"  not in st.session_state:
                        st.session_state.actual_sort2 = []

                    if "counter2" not in st.session_state:
                        st.session_state.counter2 = 0
                        st.experimental_rerun()

                    def data_changed():
                        for x in st.session_state.actual_sort2:
                            if x not in st.session_state.data_sort2:
                                st.session_state.data_sort2.append(x)
                        for x in st.session_state.data_sort2:
                            if x not in st.session_state.actual_sort2:
                                st.session_state.data_sort2.remove(x)
                        st.session_state.modified_sort2 = st.session_state.data_sort2 
                        
                    values = st.multiselect("Select values", original_items, default= complete_data["Items"] , key="bundlelocation2", on_change=data_changed )
                    st.session_state.data_location_2 = values
                    if len(values)=="":
                            st.stop()
                
                with col2.container():
                    st.subheader("Reorder the activities")
                    st.write("Drag and drop the activities to reorder them")
                    st.session_state.counter2 += 1
                    st.session_state.actual_sort2 = values 

                    if st.session_state.actual_sort2 == [original_items[0]]:
                        st.write("ok")
                        sorted_items = sort_items(st.session_state.actual_sort2)
                        st.session_state.data_sort2 = sorted_items
                    else:    
                        listita = []
                        for x in st.session_state.actual_sort2:
                            if x not in st.session_state.data_sort2:
                                st.session_state.modified_sort2.append(x)
                        for x in st.session_state.data_sort2:
                            if x not in st.session_state.actual_sort2:
                                st.session_state.data_sort2.remove(x)
                        sorted_items = sort_items(st.session_state.modified_sort2 + listita )
                        st.session_state.data_sort2 = sorted_items
                    # # eliminar  el "" valor inicial
                    # if st.session_state.counter2==1:
                    #     del st.session_state.data_sort[0]
                    elegir_actividad = st.session_state.data_sort2
            
                if elegir_actividad ==None or elegir_actividad==[]:
                    st.stop()
                
                else:
                    #! crear la funcion para crear todos los modelos de actividades 
                    def crear_actividad(data):
                        co1, co2, co3 = st.columns((2,2,1))
                        co2.subheader(data["Name_en"])
                        st.write(data["Description_en"])

                    #! crear la funcion para crear todos los modelos para el transporte
                    def crear_transporte(data, number):
                        
                        co1, co2= st.columns((0.75,2))
                        order_activity = list_activities.index(elegir_actividad[number])
                        transporte_title = transporte[order_activity]
                        co2.subheader(transporte_title)
                        st.write(data["notes price"])
                        
                        
                    for x in range(len(elegir_actividad)):
                        order_activity = list_activities.index(elegir_actividad[x])
                        code = ids_activities[order_activity]
                        
                        collection = db["activities"]
                        complete_data_act = collection.find_one({"_id":code})
                        # en este caso es una actividad
                        if complete_data_act != None:
                            
                            crear_actividad(complete_data_act)
                        if complete_data_act == None:
                            collection = db["transport"]
                            complete_data_act = collection.find_one({"_id":code})                
                            
                            crear_transporte(complete_data_act, x)
            
            st.subheader("Product Description")
            description_en = st.text_area("Description in English", height=100, value=complete_data["Description_en"])
            description_de = st.text_area("Description in German", height=100, value=complete_data["Description_de"])
            description_es = st.text_area("Description in Spanish", height=100, value=complete_data["Description_es"])
            st.subheader("Meals included")
            cole1, cole2, cole3 , cole4= st.columns([1,1,1,1])
            breakfast = cole1.checkbox('Breakfast', complete_data["breakfast"])
            lunch = cole2.checkbox('Lunch',complete_data["lunch"])
            dinner = cole3.checkbox('Dinner', complete_data["dinner"])
            other = cole4.checkbox('Other (please describe in meal notes)', complete_data["other"])
            st.subheader("Meal notes")
            as1,as2,as3 =st.columns([1,1,1])
            
            notes_en = as1.text_area("English", value=complete_data["meal notes ingles"])
            notes_de = as2.text_area("Deutsch", value=complete_data["meal notes aleman"])
            notes_es = as3.text_area("Spanish", value=complete_data["meal notes espanol"])
            
            # guardar datos
            guardar = st.button("Edit bundle")
            if guardar:
                with st.spinner("Saving bundle..."):
                    collection = db["bundle"]
                    
                    # In this section you can add new activities to the database
                    # para cada route o ruta we put  the data in the following order : [lugar de salida, lugar de llegada, descripcion ingles, descripcion aleman, descripcion espanol]
                    
                    record = {
                    "Name_en": name_en,
                    "Name_de": name_de,
                    "Name_es": name_es,
                    "Places" : lugares,
                    "Items":sorted_items,
                    "Description_en": description_en,
                    "Description_de": description_de,
                    "Description_es": description_es,
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner,
                    "other": other,
                    "meal notes ingles": notes_en,
                    "meal notes aleman": notes_de,
                    "meal notes espanol": notes_es
                    }
                    
                    
                    collection.update_one({"_id": complete_data["_id"]}, {"$set": record})
                    
                st.success('Upload successful!')


        if activities_option=="Delete":
            st.subheader("Delete a bundle")

            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection_location = db["locations"]
            data = collection_location.find({},{"Name_en":1})
            
            list_activities = []
            for value in data:
                list_activities.append(value["Name_en"])
            lugar = st.multiselect("Choose the places",list_activities)

            todos = st.checkbox("All places", value=True)
            if todos:
                lugar = list_activities
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection = db["bundle"]
                data = collection.find({},{"Name_en":1,"Places":1, "_id":1})
                # filtrar los datos para que solo aparezcan los bundles que estan en el lugar seleccionado
                list_activities = [""]
                ids_activities = [""]
                for value in data:
                        list_activities.append(value["Name_en"])
                        ids_activities.append(value["_id"])
                # FIN 

            if todos == False:
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection = db["bundle"]
                data = collection.find({},{"Name_en":1,"Places":1, "_id":1})
                # filtrar los datos para que solo aparezcan los bundles que estan en el lugar seleccionado
                list_activities = [""]
                ids_activities = [""]
                for value in data:
                    for i in value["Places"]:
                        if i in lugar:
                            list_activities.append(value["Name_en"])
                            ids_activities.append(value["_id"])
                # FIN 

            elegir_actividad = st.selectbox("Choose the bundle",list_activities)
            if elegir_actividad == "":
                st.stop()
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
        
            
            st.title(complete_data["Name_en"])
            st.write(complete_data["Description_en"])
            st.subheader("Items included")
            for x in complete_data["Items"]:
                st.write(x)


            if st.button("Delete bundle"):
                with st.spinner('Deleting...'):    
                    
                    # delete activity in mongodb
                    collection.delete_one({"_id": ObjectId(code)})
                    # ---
                st.info("Bundle deleted")
                

if menu_sidebar=="Crear programa":
    bucket_name = "peruviansunrise-storage"
    with st.sidebar:
        st.subheader("Steps to create a program")            
        menu_programa = st.radio("Select a step",("Itinerary","Activities & Transportation","Accommodations","Pricing","Operations", "Preview"))
    


    if menu_programa== "Itinerary":
        # Inicializar las variables para el nuevo programa
        if "base_name_program" not in st.session_state:
            st.session_state.base_name_program = ""
        if "eleccion_fechas_program" not in st.session_state:
            st.session_state.eleccion_fechas_program = "I have my exact travel dates"
        if  "exact_initial_dates_base_program" not in st.session_state:
            st.session_state.exact_initial_dates_base_program = date.today()
        if "exact_end_dates_base_program" not in st.session_state:
            st.session_state.exact_end_dates_base_program = date.today() + timedelta(days=7)
        if "approximate_dates_base_program" not in st.session_state:
            st.session_state.approximate_dates_base_program = ["January",1]
        if "no_dates_base_program" not in st.session_state:
            st.session_state.no_dates_base_program = 1
        if "lenguage_base_program" not in st.session_state:
            st.session_state.lenguage_base_program = "English"
        if "client_base_program" not in st.session_state:
            st.session_state.client_base_program = ""
        if "adults_cantidad_base_program" not in st.session_state:
            st.session_state.adults_cantidad_base_program = 1
        if "children_base_program" not in st.session_state:
            st.session_state.children_base_program = 0 
        if "number of places_base_program" not in st.session_state:
            st.session_state.number_of_places_base_program = ""
        if "nights_data_base_program" not in st.session_state:
            st.session_state.nights_data_base_program = [["Lima (Peru)", 0]]
        if "days_data_base_program" not in st.session_state:
            st.session_state.days_places_base_program = ""


        # https://extras.streamlit.app/Color%20ya%20Headers
        colored_header(
            label="Itinerary",
            description="",
            color_name="yellow-80",
        )
        st.subheader("Main name")
        name_program = st.text_input("Name of this program", value=st.session_state.base_name_program)
        st.session_state.base_name_program = name_program

        st.subheader("Edit trip dates")
        col1, col2 = st.columns((1,2))
        with col1:
            opciones_fechas = ["I have my exact travel dates", "I have approximate dates", "I don't have my dates yet"]
            eleccion_fechas = st.radio("Select", opciones_fechas, index=int(opciones_fechas.index(st.session_state.eleccion_fechas_program)))
            st.session_state.eleccion_fechas_program = eleccion_fechas
        with col2:    
            
            if eleccion_fechas=="I have my exact travel dates": 
                # I have imported this with "from datetime importe  date"
                
                result = date_range_picker("Select a date range", st.session_state.exact_initial_dates_base_program, st.session_state.exact_end_dates_base_program )
                st.write("Result:", result)
                st.write(result[0].strftime("%Y-%m-%d"))
                st.session_state.exact_initial_dates_base_program = result[0]
                st.session_state.exact_end_dates_base_program = result[1]
            if eleccion_fechas=="I have approximate dates":
                meses_del_año = ["January","February","March","April","May","June","July","August","September","October","November","December"]
                month = st.selectbox("Month of departure",meses_del_año, index=int(meses_del_año.index(st.session_state.approximate_dates_base_program[0])))
                days = st.number_input("Approx. duration in days", min_value=1, max_value=31, value=st.session_state.approximate_dates_base_program[1])
                st.session_state.approximate_dates_base_program = [month, days]
            if eleccion_fechas=="I don't have my dates yet":
                days = st.number_input("Approx. duration in days", min_value=1, max_value=31, value=int(st.session_state.no_dates_base_program))
                st.session_state.no_dates_base_program = days
            


        st.subheader("Proposal")
            
        # st.info(f"Phase #{val}")
        co1, co2 = st.columns((1,1))
        lenguages = ["English", "Spanish", "Deutsch"]
        lenguage = co1.selectbox("Lenguage", lenguages, index=int(lenguages.index(st.session_state.lenguage_base_program)))
        st.session_state.lenguage_base_program = lenguage
        
        st.subheader("Passengers")
        client_name = st.text_input("Client name", value=st.session_state.client_base_program)
        st.session_state.client_base_program = client_name
        coa1, coa2 = st.columns((1,1))
        adultos = coa1.number_input("Adults", min_value=1, max_value=50, value=st.session_state.adults_cantidad_base_program, step=1)
        st.session_state.adults_cantidad_base_program = adultos
        niños = coa2.number_input("Kids", min_value=0, max_value=50, value=st.session_state.children_base_program, step=1)
        st.session_state.children_base_program = niños
        st.subheader("Trip Plan Overview")
        

        # Creation of table for Itinerary
        df_template = pd.DataFrame(
            '',
            index=range(29),
            columns=["Lugar", "Dias"])
        
        # obtener la cantidad de elementos en los datos guardados de este dataframe
        dias_base_trip = len(st.session_state.nights_data_base_program)
        
        
        if dias_base_trip > 0:
            df_template.loc[0] = st.session_state.nights_data_base_program[0]  # adding a row
            if dias_base_trip > 1:
                df_template.loc[1] = st.session_state.nights_data_base_program[1]  # adding a row
                if dias_base_trip > 2:
                    df_template.loc[2] = st.session_state.nights_data_base_program[2]
                    if dias_base_trip > 3:
                        df_template.loc[3] = st.session_state.nights_data_base_program[3]
                        if dias_base_trip > 4:
                            df_template.loc[4] = st.session_state.nights_data_base_program[4]
                            if dias_base_trip > 5:
                                df_template.loc[5] = st.session_state.nights_data_base_program[5]
                                if dias_base_trip > 6:
                                    df_template.loc[6] = st.session_state.nights_data_base_program[6]
                                    if dias_base_trip > 7:
                                        df_template.loc[7] = st.session_state.nights_data_base_program[7]
                                        if dias_base_trip > 8:
                                            df_template.loc[8] = st.session_state.nights_data_base_program[8]
                                            if dias_base_trip > 9:
                                                df_template.loc[9] = st.session_state.nights_data_base_program[9]
                                                if dias_base_trip > 10:
                                                    df_template.loc[10] = st.session_state.nights_data_base_program[10]
                                                    if dias_base_trip > 11:
                                                        df_template.loc[11] = st.session_state.nights_data_base_program[11]
                                                        if dias_base_trip > 12:
                                                            df_template.loc[12] = st.session_state.nights_data_base_program[12]
                                                            if dias_base_trip > 13:
                                                                df_template.loc[13] = st.session_state.nights_data_base_program[13]
                                                                if dias_base_trip > 14:
                                                                    df_template.loc[14] = st.session_state.nights_data_base_program[14]
                                                                    if dias_base_trip > 15:
                                                                        df_template.loc[15] = st.session_state.nights_data_base_program[15]
                                                                        if dias_base_trip > 16:
                                                                            df_template.loc[16] = st.session_state.nights_data_base_program[16]
                                                                            if dias_base_trip > 17:
                                                                                df_template.loc[17] = st.session_state.nights_data_base_program[17]
                                                                                if dias_base_trip > 18:
                                                                                    df_template.loc[18] = st.session_state.nights_data_base_program[18]
                                                                                    if dias_base_trip > 19:
                                                                                        df_template.loc[19] = st.session_state.nights_data_base_program[19]
                                                                                        if dias_base_trip > 20:
                                                                                            df_template.loc[20] = st.session_state.nights_data_base_program[20]
                                                                                            if dias_base_trip > 21:
                                                                                                df_template.loc[21] = st.session_state.nights_data_base_program[21]
                                                                                                if dias_base_trip > 22:
                                                                                                    df_template.loc[22] = st.session_state.nights_data_base_program[22]
                                                                                                    if dias_base_trip > 23:
                                                                                                        df_template.loc[23] = st.session_state.nights_data_base_program[23]
                                                                                                        if dias_base_trip > 24:
                                                                                                            df_template.loc[24] = st.session_state.nights_data_base_program[24]
                                                                                                            if dias_base_trip > 25:
                                                                                                                df_template.loc[25] = st.session_state.nights_data_base_program[25]
                                                                                                                if dias_base_trip > 26:
                                                                                                                    df_template.loc[26] = st.session_state.nights_data_base_program[26]
                                                                                                                    if dias_base_trip > 27:
                                                                                                                        df_template.loc[27] = st.session_state.nights_data_base_program[27]
                                                                                                                        if dias_base_trip > 28:
                                                                                                                            df_template.loc[28] = st.session_state.nights_data_base_program[28]

        
        df_template.index = df_template.index + 1  # shifting index
        df_template.sort_index(inplace=True)

        
        
        from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, JsCode # pip install streamlit-aggrid==0.2.3

        onRowDragEnd = JsCode("""
        function onRowDragEnd(e) {
            console.log('onRowDragEnd', e);
        }
        """)

        getRowNodeId = JsCode("""
        function getRowNodeId(data) {
            return data.id
        }
        """)

        onGridReady = JsCode("""
        function onGridReady() {
            immutableStore.forEach(
                function(data, index) {
                    data.id = index;
                    });
            gridOptions.api.setRowData(immutableStore);
            }
        """)

        onRowDragMove = JsCode("""
        function onRowDragMove(event) {
            var movingNode = event.node;
            var overNode = event.overNode;

            var rowNeedsToMove = movingNode !== overNode;

            if (rowNeedsToMove) {
                var movingData = movingNode.data;
                var overData = overNode.data;

                immutableStore = newStore;

                var fromIndex = immutableStore.indexOf(movingData);
                var toIndex = immutableStore.indexOf(overData);

                var newStore = immutableStore.slice();
                moveInArray(newStore, fromIndex, toIndex);

                immutableStore = newStore;
                gridOptions.api.setRowData(newStore);

                gridOptions.api.clearFocusedCell();
            }

            function moveInArray(arr, fromIndex, toIndex) {
                var element = arr[fromIndex];
                arr.splice(fromIndex, 1);
                arr.splice(toIndex, 0, element);
            }
        }
        """)


        # lista de las locations
        # Pedir datos de mongo db para  obtener los nombres de las actividades
        collection_location = db["locations"]
        data1 = collection_location.find({},{"Name_en":1})
        
        list_activitiess = []
        for value in data1:
            list_activitiess.append(value["Name_en"])
        # fin
        #ordenar los datos en orden alfabetico de a-z
        list_activitiess = list(set(list_activitiess))
        list_activitiess.sort()
        

        gb = GridOptionsBuilder.from_dataframe(df_template)
        gb.configure_default_column(rowDrag = False, rowDragManaged = True, rowDragEntireRow = False, rowDragMultiRow=True, editable=True)

        gb.configure_column('Lugar', type=['textColumn'], editable=True,
            cellEditor='agRichSelectCellEditor',
            cellEditorParams={'values':[""]+ list_activitiess },
            cellEditorPopup=True,
            rowDrag = True,
            rowDragEntireRow = True,
            rowDragManaged = True
        )

        gb.configure_grid_options(enableRangeSelection=True, rowDragManaged = True, onRowDragEnd = onRowDragEnd, deltaRowDataMode = True, getRowNodeId = getRowNodeId, onGridReady = onGridReady, animateRows = True, onRowDragMove = onRowDragMove)


        response = AgGrid(
            df_template,
            gridOptions=gb.build(),
            fit_columns_on_grid_load=True,
            editable=True,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme = "light",  # or ['streamlit', 'light', 'dark', 'blue', 'fresh', 'material']
            update_mode=GridUpdateMode.MANUAL,
            height=300
        )
        
            # response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
            
        
        # st.write(response['data']) 
        df= pd.DataFrame(response['data'])
        # limpiar de valores vacios
        df = df[df['Lugar'].astype(bool)]

        contador = len(df.index)
        st.session_state.contador = contador
        contador = len(df.index)
    
        if contador >= 1:
            
            st.session_state.destino_1 = df.iloc[0,0]
            st.session_state.dias_1 = df.iloc[0,1]
        if contador >= 2:
            
            st.session_state.destino_2 = df.iloc[1,0]
            st.session_state.dias_2 = df.iloc[1,1]
        if contador >= 3:
            st.session_state.destino_3 = df.iloc[2,0]
            st.session_state.dias_3 = df.iloc[2,1]
        if contador >= 4:
            st.session_state.destino_4 = df.iloc[3,0]
            st.session_state.dias_4 = df.iloc[3,1]
        if contador >= 5:
            st.session_state.destino_5 = df.iloc[4,0]
            st.session_state.dias_5 = df.iloc[4,1]
        if contador >= 6:
            st.session_state.destino_6 = df.iloc[5,0]
            st.session_state.dias_6 = df.iloc[5,1]        


        #? This is data showed in the app
        # st.write(df)

        # save this data in the session state in form of a list 
        lugar_data_base = df.values.tolist()
        
        st.session_state.nights_data_base_program = lugar_data_base
        # st.write(st.session_state.nights_data_base_program)



        ##############################
        # Data for Activities & Transportation
        ##############################
        # if st.session_state.contador == 2:
        #     st.info("Please complete the Itinerary section")
        #     st.stop()

        st.title(name_program)
        st.markdown("""---""")
        # st.write(st.session_state)   
        lugares=[]
        numeros=[]
        for i in range(1, st.session_state.contador+1):
            lugares.append(st.session_state[f"destino_{i}"])
            numeros.append(st.session_state[f"dias_{i}"])
            
        data_act = pd.DataFrame({"Lugar": lugares, "Dias": numeros})
        # st.table(data_act)


        # Cargar los datos para que se guarden en el cache de sesion_state
        destinos = list_activitiess
        
        # I use this https://datagy.io/pandas-add-row/#:~:text=Age%2C%20and%20Location.-,Add%20a%20Row%20to%20a%20Pandas%20DataFrame,the%20Pandas%20concat()%20function.
        def creation_dataframe_by_days(df):
            # Inserting a Row at a Specific Index
            # if we have current indices from 0-3 and we want to insert a new row at index 2, we can simply assign it using index 1.5.
            df['Dias'] = df['Dias'].astype(int)
            valores = df["Dias"].sum() 
            df.loc[valores+1, "Dias"] = 1 
            # se aumenta en 1 para que el ultimo dia no se mantenga en 0 y se incluya actividades 
            # el orden del codigo es muy importante
            for x in range(0,valores):
                if df.loc[x,"Dias"] > 1:
                    
                    df.loc[x+0.5] = [df.loc[x,"Lugar"],int(df.loc[x,"Dias"]-1)]
                    df = df.sort_index().reset_index(drop=True)
                    df["Dias"].loc[x] = int(1)
                
            return df
        data_limpia= creation_dataframe_by_days(data_act)
        data_limpia['Dias'] = data_limpia['Dias'].astype(int)
        # st.table(data_limpia)

        # with st.form('my_form_2'):

        # st.write(data_limpia.loc[1,"Lugar"])
        # Obtener datos para los dias segun donde este el pasajero
        diccionario={}
        valores = len(data_limpia.index)
        for value in range(0,valores):
            if int(data_limpia.loc[value,"Dias"]) == 0:
                diccionario[value]=[data_limpia.loc[value,"Lugar"],data_limpia.loc[value+1,"Lugar"]]
                
                
                if int(data_limpia.loc[value+1,"Dias"]) == 0:
                    diccionario[value] = [data_limpia.loc[value,"Lugar"],data_limpia.loc[value+1,"Lugar"],data_limpia.loc[value+2,"Lugar"]]
            else:
                diccionario[value]=[data_limpia.loc[value,"Lugar"]]
            
        # st.write("diccionario")
        # st.write(diccionario)

        #  Se refinan los datos para que no se repitan los lugares
        new_dicc={}
        new_dicc[0]=diccionario[0]
        for value in range(1,len(diccionario)):
            
            if len(diccionario[value-1])==1:
                new_dicc[value]=diccionario[value]
            if len(diccionario[value-1])>=2:
                continue
        
        # Lista de listas  con los lugares segun los dias que se encuentre el pasajero en cada lugar
        final_data=list(new_dicc.values())
        # Final es la lista de listas completamente limpia, sin repetidos
        final =[]

        for  value in final_data:
            myset = set(value)
            new = list(myset)
            # Before append data we need drop NaN values to avoid errors
            new = [x for x in new if str(x) != 'nan']
            final.append(new)
        #! This data is really important for the next steps
        # st.write(final)
        st.session_state.days_places_base_program = final
        

        # Pedir datos de mongo db para  obtener los nombres de las actividades
        collection = db["locations"]
        data = collection.find({},{"Name_en":1, "_id":1})
        
        list_activities = [""]
        ids_activities = [""]
        for value in data:
            list_activities.append(value["Name_en"])
            ids_activities.append(value["_id"])
        # FIN 
        i=0
        filas = len(df)
        
        for lugar in df["Lugar"]:
            
            dias = df["Dias"].iloc[i] 
            i+=1
            elegir_actividad = lugar
            order_activity = list_activities.index(elegir_actividad)
            code = ids_activities[order_activity]
            complete_data = collection.find_one({"_id":code})
            with st.container():
                col1, col2 = st.columns((3,1))
                if i==1:
                    if int(dias) == 0:
                        col1.subheader(complete_data["Name_en"]+ " - arrival 🛬")
                        col1.markdown(complete_data["Description_en"])
                        col2.image(resize_image(get_link(bucket_name, complete_data["Images"]), 900, 600) )
                    else:
                        col1.subheader(complete_data["Name_en"]+ " - arrival 🛬"+ " - "+ str(dias) + " nights")
                        col1.markdown(complete_data["Description_en"])
                        col2.image(resize_image(get_link(bucket_name, complete_data["Images"]), 900, 600) )
                elif i==filas:
                    if int(dias) == 0:
                        col1.subheader(complete_data["Name_en"]+ " - departure 🛫")
                        col1.markdown(complete_data["Description_en"])
                        col2.image(resize_image(get_link(bucket_name, complete_data["Images"]), 900, 600) )
                    else:
                        col1.subheader(complete_data["Name_en"]+ " - departure 🛫"+ " - "+ str(dias) + " nights")
                        col1.markdown(complete_data["Description_en"])
                        col2.image(resize_image(get_link(bucket_name, complete_data["Images"]), 900, 600) )
                else:
                    col1.subheader(complete_data["Name_en"]+ " - "+ str(dias) + " nights")
                    col1.markdown(complete_data["Description_en"])
                    col2.image(resize_image(get_link(bucket_name, complete_data["Images"]), 900, 600) )


    if menu_programa== "Activities & Transportation":
        
        # https://extras.streamlit.app/Color%20ya%20Headers
        colored_header(
            label="Activities & Transportation",
            description="",
            color_name="yellow-80",
        )
    


        try:
            def activities_and_transport_program(lugares, index, default_value=None):
                if 'data_location_act'+index not in st.session_state:
                    st.session_state["data_location_act"+index] = [] #!esto debe de estar asi o generara errores, cuidado!
                if "lugares_pasado_act"+index not in st.session_state:
                    st.session_state["lugares_pasado_act"+index] = [""]
                
            
                def update_all():
                    st.session_state["bundlelocation_act"+index] = st.session_state["data_location_act"+index]
                    
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection_location = db["locations"]
                data = collection_location.find({},{"Name_en":1})
                
                list_activities = []
                for value in data:
                    list_activities.append(value["Name_en"])
                # fin
                lugares = st.multiselect("Choose the location",list_activities, default= lugares,  key= "lugarcitos"+index, on_change=update_all)
            
                if lugares == []:
                    st.stop()
                st.session_state.lugares_actual = lugares
                
                # Pedir datos de mongo db para  obtener los nombres de las actividades
                collection = db["activities"]
                data = collection.find({},{"Name_en":1, "Operator":1,"_id":1, "Location":1})
                
                list_activities = ["", "None"]
                ids_activities = ["", "None"]
                transporte = ["", "None"]

                for value in data:
                    g = [i for i in value["Location"] if i in lugares]
                    if len(g) > 0:
                        list_activities.append(value["Name_en"] + " (" + value["Operator"]+ ")")
                        ids_activities.append(value["_id"])
                        transporte.append("X")
                
                # Pedir datos de mongo db para  obtener los nombres de los transportes
                collection = db["transport"]
                data = collection.find({},{"Name_en":1, "operator":1,"_id":1, "route1":1, "route2":1, "route3":1, "route4":1, "route5":1, "route6":1, "route7":1, "route8":1, "route9":1, "route10":1})
                for value in data:
                    
                    g1 = [i for i in value["route1"] if i in lugares]
                    g2 = [i for i in value["route2"] if i in lugares]
                    g3 = [i for i in value["route3"] if i in lugares]
                    g4 = [i for i in value["route4"] if i in lugares]
                    g5 = [i for i in value["route5"] if i in lugares]
                    g6 = [i for i in value["route6"] if i in lugares]
                    g7 = [i for i in value["route7"] if i in lugares]
                    g8 = [i for i in value["route8"] if i in lugares]
                    g9 = [i for i in value["route9"] if i in lugares]
                    g10 = [i for i in value["route10"] if i in lugares]
                    final = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9 + g10
                    if len(final)>0:
                        list_activities.append(value["route1"][0]+" --> "+value["route1"][1]+" (" + value["operator"]+ ")") 
                        transporte.append(value["route1"][0]+" to "+value["route1"][1]) 
                        ids_activities.append(value["_id"])
                        if len(final)>=2:
                            list_activities.append(value["route2"][0]+" --> "+value["route2"][1]+" (" + value["operator"]+ ")") 
                            transporte.append(value["route2"][0]+" to "+value["route2"][1]) 
                            ids_activities.append(value["_id"])
                            if len(final)>=3:
                                list_activities.append(value["route3"][0]+" --> "+value["route3"][1]+" (" + value["operator"]+ ")") 
                                transporte.append(value["route3"][0]+" to "+value["route3"][1]) 
                                ids_activities.append(value["_id"])
                                if len(final)>=4:
                                    list_activities.append(value["route4"][0]+" --> "+value["route4"][1]+" (" + value["operator"]+ ")") 
                                    transporte.append(value["route4"][0]+" to "+value["route4"][1]) 
                                    ids_activities.append(value["_id"])
                                    if len(final)>=5:
                                        list_activities.append(value["route5"][0]+" --> "+value["route5"][1]+" (" + value["operator"]+ ")") 
                                        transporte.append(value["route5"][0]+" to "+value["route5"][1]) 
                                        ids_activities.append(value["_id"])
                                        if len(final)>=6:
                                            list_activities.append(value["route6"][0]+" --> "+value["route6"][1]+" (" + value["operator"]+ ")") 
                                            transporte.append(value["route6"][0]+" to "+value["route6"][1]) 
                                            ids_activities.append(value["_id"])
                                            if len(final)>=7:
                                                list_activities.append(value["route7"][0]+" --> "+value["route7"][1]+" (" + value["operator"]+ ")") 
                                                transporte.append(value["route7"][0]+" to "+value["route7"][1]) 
                                                ids_activities.append(value["_id"])
                                                if len(final)>=8:
                                                    list_activities.append(value["route8"][0]+" --> "+value["route8"][1]+" (" + value["operator"]+ ")") 
                                                    transporte.append(value["route8"][0]+" to "+value["route8"][1]) 
                                                    ids_activities.append(value["_id"])
                                                    if len(final)>=9:
                                                        list_activities.append(value["route9"][0]+" --> "+value["route9"][1]+" (" + value["operator"]+ ")") 
                                                        transporte.append(value["route9"][0]+" to "+value["route9"][1]) 
                                                        ids_activities.append(value["_id"])
                                                        if len(final)>=10:
                                                            list_activities.append(value["route10"][0]+" --> "+value["route10"][1]+" (" + value["operator"]+ ")") 
                                                            transporte.append(value["route10"][0]+" to "+value["route10"][1]) 
                                                            ids_activities.append(value["_id"])
            
                #! Nueva forma de hacer
                
                #! Fin
                with st.expander('Select values', expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:

                        st.subheader("Activities & Transport")
                        from streamlit_sortables import sort_items

                        original_items = list_activities
                        # sorted_items = sort_items(original_items)

                        # st.write(f'original_items: {original_items}')
                        # st.write(f'sorted_items: {sorted_items}')
                        if "data_sort_act"+index not in st.session_state:
                            st.session_state["data_sort_act"+index] = []
                        if "modified_sort_act"+index  not in st.session_state:
                            st.session_state["modified_sort_act"+index] = []
                        if "actual_sort_act"+index  not in st.session_state:
                            st.session_state["actual_sort_act"+index] = []

                        if "counter" not in st.session_state:
                            st.session_state.counter = 0
                            st.experimental_rerun()

                        def data_changed_act():
                            for x in st.session_state["actual_sort_act"+index]:
                                if x not in st.session_state["data_sort_act"+index]:
                                    st.session_state["data_sort_act"+index].append(x)
                            for x in st.session_state["data_sort_act"+index]:
                                if x not in st.session_state["actual_sort_act"+index]:
                                    st.session_state["data_sort_act"+index].remove(x)
                            st.session_state["modified_sort_act"+index] = st.session_state["data_sort_act"+index]
                        values = st.multiselect("Select values", original_items, default= default_value, key="bundlelocation_act"+index, on_change=data_changed_act )
                        st.session_state["data_location_act"+index] = values
                        if len(values)=="":
                                st.stop()
                    
                    with col2.container():
                        st.subheader("Reorder the activities")
                        st.write("Drag and drop the activities to reorder them")
                        st.session_state.counter += 1
                        st.session_state["actual_sort_act"+index] = values 

                        if st.session_state["actual_sort_act"+index] == [original_items[0]]:
                            
                            sorted_items = st.session_state["actual_sort_act"+index] 
                            st.session_state["data_sort_act"+index]= sorted_items
                        else:    
                            listita = []
                            for x in st.session_state["actual_sort_act"+index]:
                                if x not in st.session_state["data_sort_act"+index]:
                                    st.session_state["modified_sort_act"+index].append(x)
                            for x in st.session_state["data_sort_act"+index]:
                                if x not in st.session_state["actual_sort_act"+index]:
                                    st.session_state["data_sort_act"+index].remove(x)
                            sorted_items = sort_items(st.session_state["modified_sort_act"+index] + listita, key=None)
                            st.session_state["data_sort_act"+index] = sorted_items
                        # # eliminar  el "" valor inicial
                        # if st.session_state.counter==1:
                        #     del st.session_state.data_sort[0]
                        elegir_actividad = st.session_state["data_sort_act"+index]
                
                    if elegir_actividad ==None or elegir_actividad==[]:
                        st.stop()
                    
                    else:
                        #! crear la funcion para crear todos los modelos de actividades 
                        def crear_actividad(data):
                            co1, co2, co3 = st.columns((2,2,1))
                            co2.subheader(data["Name_en"])
                            st.write(data["Description_en"])

                        #! crear la funcion para crear todos los modelos para el transporte
                        def crear_transporte(data, number):
                            
                            co1, co2= st.columns((0.75,2))
                            order_activity = list_activities.index(elegir_actividad[number])
                            transporte_title = transporte[order_activity]
                            co2.subheader(transporte_title)
                            st.write(data["notes price"])
                            
                        if elegir_actividad != [""]:
                            for x in range(len(elegir_actividad)):
                                order_activity = list_activities.index(elegir_actividad[x])
                                code = ids_activities[order_activity]
                                
                                collection = db["activities"]
                                complete_data = collection.find_one({"_id":code})
                                # en este caso es una actividad
                                if complete_data != None:
                                    
                                    crear_actividad(complete_data)

                                if complete_data == None:
                                    collection = db["transport"]
                                    complete_data = collection.find_one({"_id":code})                
                                    
                                    crear_transporte(complete_data, x)
                        else:
                            return elegir_actividad

                return elegir_actividad
            
            cantidad_dias = len(st.session_state.days_places_base_program)
            

            # Inicializar variables para guardar data
            if "contador_act_trans" not in st.session_state:
                st.session_state.contador_act_trans = 1
            

            if "data_boom_1" not in st.session_state:
                st.session_state.data_boom_1 = None
            if "data_boom_2" not in st.session_state:
                st.session_state.data_boom_2 = None
            if "data_boom_3" not in st.session_state:
                st.session_state.data_boom_3 = None
            if "data_boom_4" not in st.session_state:
                st.session_state.data_boom_4 = None
            if "data_boom_5" not in st.session_state:
                st.session_state.data_boom_5 = None
            if "data_boom_6" not in st.session_state:
                st.session_state.data_boom_6 = None
            if "data_boom_7" not in st.session_state:
                st.session_state.data_boom_7 = None
            if "data_boom_8" not in st.session_state:
                st.session_state.data_boom_8 = None
            if "data_boom_9" not in st.session_state:
                st.session_state.data_boom_9 = None
            if "data_boom_10" not in st.session_state:
                st.session_state.data_boom_10 = None
            if "data_boom_11" not in st.session_state:
                st.session_state.data_boom_11 = None
            if "data_boom_12" not in st.session_state:
                st.session_state.data_boom_12 = None
            if "data_boom_13" not in st.session_state:
                st.session_state.data_boom_13 = None
            if "data_boom_14" not in st.session_state:
                st.session_state.data_boom_14 = None
            if "data_boom_15" not in st.session_state:
                st.session_state.data_boom_15 = None
            if "data_boom_16" not in st.session_state:
                st.session_state.data_boom_16 = None
            if "data_boom_17" not in st.session_state:
                st.session_state.data_boom_17 = None
            if "data_boom_18" not in st.session_state:
                st.session_state.data_boom_18 = None
            if "data_boom_19" not in st.session_state:
                st.session_state.data_boom_19 = None
            if "data_boom_20" not in st.session_state:
                st.session_state.data_boom_20 = None
            if "data_boom_21" not in st.session_state:
                st.session_state.data_boom_21 = None
            if "data_boom_22" not in st.session_state:
                st.session_state.data_boom_22 = None
            if "data_boom_23" not in st.session_state:
                st.session_state.data_boom_23 = None
            if "data_boom_24" not in st.session_state:
                st.session_state.data_boom_24 = None
            if "data_boom_25" not in st.session_state:
                st.session_state.data_boom_25 = None
            if "data_boom_26" not in st.session_state:
                st.session_state.data_boom_26 = None
            if "data_boom_27" not in st.session_state:
                st.session_state.data_boom_27 = None
            if "data_boom_28" not in st.session_state:
                st.session_state.data_boom_28 = None
            if "data_boom_29" not in st.session_state:
                st.session_state.data_boom_29 = None
            if "data_boom_30" not in st.session_state:
                st.session_state.data_boom_30 = None
            if "data_boom_31" not in st.session_state:
                st.session_state.data_boom_31 = None
            if "data_boom_32" not in st.session_state:
                st.session_state.data_boom_32 = None
            if "data_boom_33" not in st.session_state:
                st.session_state.data_boom_33 = None
            if "data_boom_34" not in st.session_state:
                st.session_state.data_boom_34 = None
            if "data_boom_35" not in st.session_state:
                st.session_state.data_boom_35 = None
            if "data_boom_36" not in st.session_state:
                st.session_state.data_boom_36 = None
            if "data_boom_37" not in st.session_state:
                st.session_state.data_boom_37 = None
            if "data_boom_38" not in st.session_state:
                st.session_state.data_boom_38 = None
            if "data_boom_39" not in st.session_state:
                st.session_state.data_boom_39 = None
            if "data_boom_40" not in st.session_state:
                st.session_state.data_boom_40 = None
            if "data_boom_41" not in st.session_state:
                st.session_state.data_boom_41 = None
            if "data_boom_42" not in st.session_state:
                st.session_state.data_boom_42 = None
            if "data_boom_43" not in st.session_state:
                st.session_state.data_boom_43 = None
            if "data_boom_44" not in st.session_state:
                st.session_state.data_boom_44 = None
            if "data_boom_45" not in st.session_state:
                st.session_state.data_boom_45 = None
            if "data_boom_46" not in st.session_state:
                st.session_state.data_boom_46 = None
            if "data_boom_47" not in st.session_state:
                st.session_state.data_boom_47 = None
            if "data_boom_48" not in st.session_state:
                st.session_state.data_boom_48 = None
            if "data_boom_49" not in st.session_state:
                st.session_state.data_boom_49 = None
            if "data_boom_50" not in st.session_state:
                st.session_state.data_boom_50 = None


            if cantidad_dias >= 1:
                lugares = ""
                for  lugar in st.session_state.days_places_base_program[0]:
                    lugares+=lugar+" - "
                lugares = lugares[:-3]
                st.markdown("## DAY 1"+" - "+str(lugares))
                if st.session_state.contador_act_trans == 1:
                    data_1 = activities_and_transport_program(st.session_state.days_places_base_program[0], str(0))
                    st.session_state.data_boom_1 = data_1
                    
                elif st.session_state.contador_act_trans != 1 :
                    data_1 = activities_and_transport_program(st.session_state.days_places_base_program[0], str(0), st.session_state.data_boom_1)
                    st.session_state.data_boom_1 = data_1
                
                if cantidad_dias >= 2:
                    lugares = ""
                    for  lugar in st.session_state.days_places_base_program[1]:
                        lugares+=lugar+" - "
                    lugares = lugares[:-3]
                    st.markdown("## DAY 2"+" - "+str(lugares))
                    if st.session_state.contador_act_trans ==1:
                        data_2 = activities_and_transport_program(st.session_state.days_places_base_program[1], str(1))
                        st.session_state.data_boom_2 = data_2
                        
                    elif st.session_state.contador_act_trans != 1:
                        data_2 = activities_and_transport_program(st.session_state.days_places_base_program[1], str(1), st.session_state.data_boom_2)
                        st.session_state.data_boom_2 = data_2
                    
                    if cantidad_dias >= 3:  
                        lugares = ""
                        for  lugar in st.session_state.days_places_base_program[2]:
                            lugares+=lugar+" - "
                        lugares = lugares[:-3]
                        st.markdown("## DAY 3"+" - "+str(lugares))
                        if st.session_state.contador_act_trans ==1:
                            data_3 = activities_and_transport_program(st.session_state.days_places_base_program[2], str(2))
                            st.session_state.data_boom_3 = data_3
                            
                        elif st.session_state.contador_act_trans != 1:
                            data_3 = activities_and_transport_program(st.session_state.days_places_base_program[2], str(2), st.session_state.data_boom_3)
                            st.session_state.data_boom_3 = data_3
                        
                        if cantidad_dias >= 4:
                            lugares = ""
                            for  lugar in st.session_state.days_places_base_program[3]:
                                lugares+=lugar+" - "
                            lugares = lugares[:-3]
                            st.markdown("## DAY 4"+" - "+str(lugares))
                            if st.session_state.contador_act_trans ==1:
                                data_4 = activities_and_transport_program(st.session_state.days_places_base_program[3], str(3))
                                st.session_state.data_boom_4 = data_4
                                
                            elif st.session_state.contador_act_trans != 1:
                                data_4 = activities_and_transport_program(st.session_state.days_places_base_program[3], str(3), st.session_state.data_boom_4)
                                st.session_state.data_boom_4 = data_4
                            
                            if cantidad_dias >= 5:
                                lugares = ""
                                for  lugar in st.session_state.days_places_base_program[4]:
                                    lugares+=lugar+" - "
                                lugares = lugares[:-3]
                                st.markdown("## DAY 5"+" - "+str(lugares))
                                if st.session_state.contador_act_trans ==1:
                                    data_5 = activities_and_transport_program(st.session_state.days_places_base_program[4], str(4))
                                    st.session_state.data_boom_5 = data_5
                                elif st.session_state.contador_act_trans != 1:
                                    data_5 = activities_and_transport_program(st.session_state.days_places_base_program[4], str(4), st.session_state.data_boom_5)
                                    st.session_state.data_boom_5 = data_5
                                
                                if cantidad_dias >= 6:
                                    lugares = ""
                                    for  lugar in st.session_state.days_places_base_program[5]:
                                        lugares+=lugar+" - "
                                    lugares = lugares[:-3]
                                    st.markdown("## DAY 6"+" - "+str(lugares))
                                    if st.session_state.contador_act_trans ==1:
                                        data_6 = activities_and_transport_program(st.session_state.days_places_base_program[5], str(5))
                                        st.session_state.data_boom_6 = data_6
                                    elif st.session_state.contador_act_trans != 1:
                                        data_6 = activities_and_transport_program(st.session_state.days_places_base_program[5], str(5), st.session_state.data_boom_6)
                                        st.session_state.data_boom_6 = data_6
                                    
                                    if cantidad_dias >= 7:
                                        lugares = ""
                                        for  lugar in st.session_state.days_places_base_program[6]:
                                            lugares+=lugar+" - "
                                        lugares = lugares[:-3]
                                        st.markdown("## DAY 7"+" - "+str(lugares))
                                        if st.session_state.contador_act_trans ==1:
                                            data_7 = activities_and_transport_program(st.session_state.days_places_base_program[6], str(6))
                                            st.session_state.data_boom_7 = data_7
                                        elif st.session_state.contador_act_trans != 1:
                                            data_7 = activities_and_transport_program(st.session_state.days_places_base_program[6], str(6), st.session_state.data_boom_7)
                                            st.session_state.data_boom_7 = data_7
                                        
                                        if cantidad_dias >= 8:
                                            lugares = ""
                                            for  lugar in st.session_state.days_places_base_program[7]:
                                                lugares+=lugar+" - "
                                            lugares = lugares[:-3]
                                            st.markdown("## DAY 8"+" - "+str(lugares))
                                            if st.session_state.contador_act_trans ==1:
                                                data_8 = activities_and_transport_program(st.session_state.days_places_base_program[7], str(7))
                                                st.session_state.data_boom_8 = data_8
                                            elif st.session_state.contador_act_trans != 1:
                                                data_8 = activities_and_transport_program(st.session_state.days_places_base_program[7], str(7), st.session_state.data_boom_8)
                                                st.session_state.data_boom_8 = data_8
                                            
                                            if cantidad_dias >= 9:
                                                lugares = ""
                                                for  lugar in st.session_state.days_places_base_program[8]:
                                                    lugares+=lugar+" - "
                                                lugares = lugares[:-3]
                                                st.markdown("## DAY 9"+" - "+str(lugares))
                                                if st.session_state.contador_act_trans ==1:
                                                    data_9 = activities_and_transport_program(st.session_state.days_places_base_program[8], str(8))
                                                    st.session_state.data_boom_9 = data_9
                                                elif st.session_state.contador_act_trans != 1:
                                                    data_9 = activities_and_transport_program(st.session_state.days_places_base_program[8], str(8), st.session_state.data_boom_9)
                                                    st.session_state.data_boom_9 = data_9
                                                
                                                if cantidad_dias >= 10:
                                                    lugares = ""
                                                    for  lugar in st.session_state.days_places_base_program[9]:
                                                        lugares+=lugar+" - "
                                                    lugares = lugares[:-3]
                                                    st.markdown("## DAY 10"+" - "+str(lugares))
                                                    if st.session_state.contador_act_trans ==1:
                                                        data_10 = activities_and_transport_program(st.session_state.days_places_base_program[9], str(9))
                                                        st.session_state.data_boom_10 = data_10
                                                    elif st.session_state.contador_act_trans != 1:
                                                        data_10 = activities_and_transport_program(st.session_state.days_places_base_program[9], str(9), st.session_state.data_boom_10)
                                                        st.session_state.data_boom_10 = data_10
                                                    
                                                    if cantidad_dias >= 11:
                                                        lugares = ""
                                                        for  lugar in st.session_state.days_places_base_program[10]:
                                                            lugares+=lugar+" - "
                                                        lugares = lugares[:-3]
                                                        st.markdown("## DAY 11"+" - "+str(lugares))
                                                        if st.session_state.contador_act_trans ==1:
                                                            data_11 = activities_and_transport_program(st.session_state.days_places_base_program[10], str(10))
                                                            st.session_state.data_boom_11 = data_11
                                                        elif st.session_state.contador_act_trans != 1:
                                                            data_11 = activities_and_transport_program(st.session_state.days_places_base_program[10], str(10), st.session_state.data_boom_11)
                                                            st.session_state.data_boom_11 = data_11
                                                        
                                                        if cantidad_dias >= 12:
                                                            lugares = ""
                                                            for  lugar in st.session_state.days_places_base_program[11]:
                                                                lugares+=lugar+" - "
                                                            lugares = lugares[:-3]
                                                            st.markdown("## DAY 12"+" - "+str(lugares))
                                                            if st.session_state.contador_act_trans ==1:
                                                                data_12 = activities_and_transport_program(st.session_state.days_places_base_program[11], str(11))
                                                                st.session_state.data_boom_12 = data_12
                                                            elif st.session_state.contador_act_trans != 1:
                                                                data_12 = activities_and_transport_program(st.session_state.days_places_base_program[11], str(11), st.session_state.data_boom_12)
                                                                st.session_state.data_boom_12 = data_12
                                                            
                                                            if cantidad_dias >= 13:
                                                                lugares = ""
                                                                for  lugar in st.session_state.days_places_base_program[12]:
                                                                    lugares+=lugar+" - "
                                                                lugares = lugares[:-3]
                                                                st.markdown("## DAY 13"+" - "+str(lugares))
                                                                if st.session_state.contador_act_trans ==1:
                                                                    data_13 = activities_and_transport_program(st.session_state.days_places_base_program[12], str(12))
                                                                    st.session_state.data_boom_13 = data_13
                                                                elif st.session_state.contador_act_trans != 1:
                                                                    data_13 = activities_and_transport_program(st.session_state.days_places_base_program[12], str(12), st.session_state.data_boom_13)
                                                                    st.session_state.data_boom_13 = data_13
                                                                
                                                                if cantidad_dias >= 14:
                                                                    lugares = ""
                                                                    for  lugar in st.session_state.days_places_base_program[13]:
                                                                        lugares+=lugar+" - "
                                                                    lugares = lugares[:-3]
                                                                    st.markdown("## DAY 14"+" - "+str(lugares))
                                                                    if st.session_state.contador_act_trans ==1:
                                                                        data_14 = activities_and_transport_program(st.session_state.days_places_base_program[13], str(13))
                                                                        st.session_state.data_boom_14 = data_14
                                                                    elif st.session_state.contador_act_trans != 1:
                                                                        data_14 = activities_and_transport_program(st.session_state.days_places_base_program[13], str(13), st.session_state.data_boom_14)
                                                                        st.session_state.data_boom_14 = data_14

        
            if st.button("Save"):
                st.session_state.contador_act_trans +=1
                st.info("Saved")
        except:
            st.write("")
    st.markdown("##")
    st.markdown("##")
    