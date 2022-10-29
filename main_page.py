"""

Fidel Alberto Ramos Calachahuin
VittaQuant Inc.
Aplication 1 of example to the webpage
Cloud Streamlit

"""
from genericpath import exists
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
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
    menu_sidebar = option_menu("Program", ['Create new', "Templates", "Save this program"],
        icons=['house', 'folder','save'], menu_icon="cast", default_index=0)
    
menu = option_menu(None, ["Itinerary","Activities & Transportation","Accommodations","Pricing"], 
    icons=['calendar', 'binoculars', "tag", 'credit-card'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#212529", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"10px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#ffc300"},
    }
)


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
    
    
    
if menu_sidebar == "Templates":
    st.write("Estamos trabajando en ello")
    
if menu_sidebar == "Create new":
    
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
    
    
    
    st.sidebar.caption("Developed by [**Fidel Ramos**](https://vittaquant-ai.com)")
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

    image = {0:"data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=",
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
    markup = left.slider("Markup",0,100,20,key = "markup")
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
                price=f"The total price is {price} USD"
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
                price=f"The total price is {price} USD"
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
                price=f"The total price is {price} USD"
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
                price=f"The total price is {price} USD"
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
        