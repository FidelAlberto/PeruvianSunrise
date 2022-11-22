"""

Fidel Alberto Ramos Calachahuin
VittaQuant Inc.
Cloud Streamlit

"""

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




# CREATION OF favicon

st.set_page_config(layout="wide",#"centered", 
    page_icon="🗽",
    page_title="Peruvian Sunrise")

hide_menu="""
<style>
MainMenu {
    visibility:hidden;
}
footer
{
    visibility:hidden;
}
</style>
"""

st.markdown(hide_menu , unsafe_allow_html=True)
# ------------------------------------------
# Initialize the bars and menus
with st.sidebar:
    menu_sidebar = option_menu("Program", ['Create new', "Templates", "Save this program", "Data"],
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
    

    val = stx.stepper_bar(steps=["Fase 0", "Data", "Diseño", "Revision"])
    # st.info(f"Phase #{val}")

    st.sidebar.selectbox("Lenguage", ["English", "Spanish", "Alemán"], index=0)
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
        
        gb = GridOptionsBuilder.from_dataframe(df_template)
        gb.configure_default_column(editable=True)

        gb.configure_column('Lugar', type=['textColumn'], editable=True,
            cellEditor='agRichSelectCellEditor',
            cellEditorParams={'values':["",'Lima','Cusco','Arequipa','Madre de Dios','Ica']},
            cellEditorPopup=True
        )

        gb.configure_grid_options(enableRangeSelection=True)


        response = AgGrid(
            df_template,
            gridOptions=gb.build(),
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme = "alpine"  # or "streamlit","alpine","balham","material"
        )
        
        # response = AgGrid(df_template, editable=True, fit_columns_on_grid_load=True)
        st.form_submit_button("Save")

    


    # st.write(response['data']) 
    df= pd.DataFrame(response['data'])
    # limpiar de valores vacios
    df = df[df['Lugar'].astype(bool)]
    
    
    
    st.sidebar.caption("Developed by  [**Fidel Ramos**](https://vittaquant-ai.com)")
    st.sidebar.caption("**VittaQuant Techonologies**")
    st.sidebar.markdown('##')  

        
        # You can call any Streamlit command, including custom components:
        



    # with st.form('my_form'):    
    #     col1,col2,col3= st.columns([2,1,1])
    #     with col1:
    #         destino_1 = st.selectbox("Select arrival location",destinos, key="1_first")
    #         st.session_state['destino_1'] = destino_1
    #     with col2:
    #         dias_1 = st.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_first")
    #         st.session_state['dias_1'] = dias_1
    #     contador = st.session_state['contador']
        
        

        
        
    #     if st.form_submit_button('Add'):

    #         if contador >= 2:
    #             destino_2 = col1.selectbox("Overnight Location",destinos, key="1_a")
    #             dias_2 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_a")
    #             st.session_state.contador = 3
    #             st.session_state.destino_2 = destino_2
    #             st.session_state.dias_2 = dias_2
                
        #     if contador >= 3:
                
        #         destino_3 = col1.selectbox("Overnight Location",destinos, key="1_b")
        #         dias_3 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_b")
        #         st.session_state.contador = 4 
        #         st.session_state.destino_3 = destino_3
        #         st.session_state.dias_3 = dias_3
                
        #     if contador >= 4:
        #         destino_4 = col1.selectbox("Overnight Location",destinos, key="1_c")
        #         dias_4 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_c")
        #         st.session_state.contador = 5
        #         st.session_state.destino_4 = destino_4
        #         st.session_state.dias_4 = dias_4
                
        #     if contador >= 5:
        #         destino_5 = col1.selectbox("Overnight Location",destinos, key="1_d")
        #         dias_5 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_d")
        #         st.session_state.contador = 6
        #         st.session_state.destino_5 = destino_5
        #         st.session_state.dias_5 = dias_5
        
        
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
    
                
    # if contador >= 3:
        
    #     destino_3 = col1.selectbox("Overnight Location",destinos, key="1_b")
    #     dias_3 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_b")
    #     st.session_state.contador = 4 
    #     st.session_state.destino_3 = destino_3
    #     st.session_state.dias_3 = dias_3
        
    # if contador >= 4:
    #     destino_4 = col1.selectbox("Overnight Location",destinos, key="1_c")
    #     dias_4 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_c")
    #     st.session_state.contador = 5
    #     st.session_state.destino_4 = destino_4
    #     st.session_state.dias_4 = dias_4
        
    # if contador >= 5:
    #     destino_5 = col1.selectbox("Overnight Location",destinos, key="1_d")
    #     dias_5 = col2.number_input("Nights", min_value=0, max_value=50, value=0, step=1, key="2_d")
    #     st.session_state.contador = 6
    #     st.session_state.destino_5 = destino_5
    #     st.session_state.dias_5 = dias_5
        
        
        
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

    if st.button("Generar"):
        if cantidad == 1:
            template = env.get_template("templates/sample_1.html")
            html = template.render(
                student=student,
                a=a,
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
        # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        # pdf=pdfkit.from_string(html, False, configuration=config)
        
        # 1 row  to put the app in cloud ----------------------
        pdf = pdfkit.from_string(html, False, css='sample.css')
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
    
    
    
    ############################
    # Connection to MongoDB
    ############################

    
    # Connection to MongoDB since applicacion in streamlit cloud
    # cluster = pymongo.MongoClient("mongodb+srv://test:Empresas731@cluster0.vzqjn.mongodb.net/peruviansunrise?retryWrites=true&w=majority")
    # Connection to MongoDB since applicacion in local
    cluster = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cluster["peruviansunrise"]
    
    # FIN
        
    if menu == "Activities":
        
        activities_option = st.sidebar.radio("Option",["Create new","Edit","Delete"])
        
        if activities_option == "Edit":
            # Pedir datos de mongo db para  obtener los nombres de las actividades
            collection = db["activities"]
            data = collection.find({},{"Name_en":1, "Operator":1,"_id":1})
            
            list_activities = [""]
            ids_activities = [""]
            for value in data:
                list_activities.append(value["Name_en"] + "(" + value["Operator"]+ ")")
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
            
            c1.image(url_1, use_column_width="auto")
            c2.image(url_2, use_column_width="auto")
            c3.image(url_3, use_column_width="auto")
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
                            theme= "alpine" # or "streamlit","alpine","balham","material"
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
                            theme= "alpine" # or "streamlit","alpine","balham","material"
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
                            "Location": locations
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
                            "Location": locations
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
                                theme= "alpine" # or "streamlit","alpine","balham","material"
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
                            "Location": locations
                            }
                            
                            collection.insert_one(record)
        ########################
        # Delete a activity
        ########################
        if activities_option == "Delete":
            st.subheader("Delete a activity")
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
                            theme= "alpine" # or "streamlit","alpine","balham","material"
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
                            theme= "alpine" # or "streamlit","alpine","balham","material"
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
                        
                    
                        
            
            
            



    if menu=="Transportation":
            
        st.sidebar.radio("Option",["Create new","Edit","Delete"])
        bucket_name = "peruviansunrise-storage"
        url = get_link(bucket_name, 'ejemplo.PNG')
        if url is not None:
            response = requests.get(url)
        st.subheader("Image from S3")
        st.image(url, width=250 )


    if menu == "Bundle":
        st.info("Estamos trabajando en ello")
        
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
            
            
            
            st.subheader("Create new location")
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
                        