
#################################################### 
# How create a visualizer of a pdf file in streamlit 
#################################################### 


# import streamlit as st
# import base64


# def show_pdf(file_path):
#     with open(file_path,"rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)
    
# show_pdf('peruvian.pdf')




#################################################### 
# Upload and download images from S3 AWS  with streamlit interface
#################################################### 


# import os
# import boto3
# from botocore.exceptions import ClientError

# access_key =  "AKIARCQ5LPGG24TLZA3E"
# access_secret = "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"
# bucket_name = "peruviansunrise-storage"

# # connect to s3 service

# client_s3 = boto3.client(
#     's3',
#     aws_access_key_id=access_key,
#     aws_secret_access_key=access_secret
# )
# # Upload files to S3 bucket
# data_file_folder = "C:/Users/Usuario/Desktop/data_peruvian"

# for file in os.listdir(data_file_folder):
#     if not file.startswith("~"):
#         try:
#             print("Uploading file: ", file)
#             client_s3.upload_file(
#             os.path.join(data_file_folder, file),
#             bucket_name,
#             file
#             )
#         except ClientError as e:
#             print("Credential is incorrect")
#             print(e)
#         except Exception as e:
#             print(e)
            
            


#################################################### 
# wait message on interface streamlit
# https://github.com/tanglespace/hydralit_components#info-card
#################################################### 
# import hydralit_components as hc
# import time

# # a dedicated single loader 
# with hc.HyLoader('Now doing loading',hc.Loaders.pulse_bars, ):
#     time.sleep(5)

# # for 3 loaders from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[0,1,2,3,4,5,6,7,8,9,10]):
#     time.sleep(5)

# # for 1 (index=5) from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=5):
#     time.sleep(5)

# # for 4 replications of the same loader (index=2) from the standard loader group
# with hc.HyLoader('Now doing loading',hc.Loaders.standard_loaders,index=[2,2,2,2]):
#     time.sleep(5)


#################################################### 
# Create  steps interface in streamlit
# https://github.com/Mohamed-512/Extra-Streamlit-Components
#################################################### 
# import extra_streamlit_components as stx
# import streamlit as st
# val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
# st.info(f"Phase #{val}")



#################################################### 
# tabs with css
# https://github.com/Socvest/streamlit-on-Hover-tabs
# This works with streamlit 1.11.0 or lower
# A secon best interface to create dashboards in streamlit with many options and cool
#################################################### 


#################################################### 
# Option to create a pdf file merger in streamlit
# PDF MERGE 2 OR MORE PDFS
# 
#################################################### 

# from datetime import datetime
# from pathlib import Path
# import streamlit as st
# import streamlit_pydantic as sp
# from typing import Optional, List
# from streamlit_pydantic.types import FileContent
# from pydantic import BaseModel, Field
# from PyPDF2 import PdfFileWriter, PdfFileReader


# # Make folder for storing user uploads
# destination_folder = Path('downloads')
# destination_folder.mkdir(exist_ok=True, parents=True)

# import base64
# #! This is used to pre uploaded pdf to the app 
# with open("pdfaa.pdf", "rb") as pdf_file:
#     data_2 = base64.b64encode(pdf_file.read())
# #! Fin

# # Defines what options are in the form
# class PDFMergeRequest(BaseModel):
#     pdf_uploads: Optional[List[FileContent]] = Field(
#         data_2,
#         alias="PDF File to Split",
#         description="PDF that needs to be split",
#     )

# pdf_output = '.pdf'
# output_suffix = '.pdf'
# merge = 'Merge Multiple PDFs into One'
# split = 'Split One PDF into Multiple'
# view_choice = merge 
# if view_choice == merge:
#     # Get the data from the form, stop running if user hasn't submitted pdfs yet
#     data = sp.pydantic_form(key="pdf_merge_form", model=PDFMergeRequest )
#     #! If you want to use the app without the opcion of pre upload pdf, just put the next value this in 2 and not in 1
#     if data is None or data.pdf_uploads is None or len(data.pdf_uploads) < 1:
#         st.warning("Upload at least 2 PDFs and press Submit")
#         st.stop()

#     data.pdf_uploads.insert(0,data_2)
#     # st.write(data.pdf_uploads)
    

#     # Save Uploaded PDFs
#     uploaded_paths = []
#     for pdf_data in data.pdf_uploads:
#         try:
#             input_pdf_path = destination_folder / f"input_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
#             input_pdf_path.write_bytes(pdf_data.as_bytes())
#             uploaded_paths.append(input_pdf_path)
#         #! This is a hack to get around the fact that streamlit_pydantic doesn't support base64 encoded files
#         #! This a piece of code to allow the app to work with a pdf previously uploaded to the app
#         except AttributeError:
#             input_pdf_path.write_bytes(base64.b64decode(pdf_data, validate=True))
#             uploaded_paths.append(input_pdf_path)    
#         #! Fin

#     pdf_writer = PdfFileWriter()
#     for path in uploaded_paths:
#         pdf_reader = PdfFileReader(str(path))
#         for page in range(pdf_reader.getNumPages()):
#             # Add each page to the writer object
#             pdf_writer.addPage(pdf_reader.getPage(page))

#     # Write out the merged PDF
#     output_pdf_path = destination_folder / f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.pdf"
#     with open(str(output_pdf_path), 'wb') as out:
#         pdf_writer.write(out)
#     output_path = output_pdf_path
#     # Convert to stacked / merged image
    

#     # Allow download
#     if output_suffix == pdf_output:
#         output_mime = 'application/pdf'
#     st.download_button('Download Merged Document', output_path.read_bytes(), f"output_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}{output_suffix}", mime=output_mime)





####################################################
#? Create a input with many options negrita, subrayado, etc in html
####################################################
# import streamlit as st
# from streamlit_quill import st_quill
# import streamlit.components.v1 as components

# with st.container():

#     c1, c2 = st.columns([2, 1])

#     with c1:
#         content = st_quill(
#             placeholder="Write here",
#             html=True,
#             readonly=False,
#             key="none",
            
#         )
#     # st.markdown(content, unsafe_allow_html=True)
#     st.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")

# components.html(content, height=600)


####################################################
#? Learning to use the st.session_state  to update the value of a variable in the app
####################################################

# import streamlit as st
# def calc_area():
#     st.session_state['area'] = st.session_state['side'] ** 2

# def calc_side():
#     st.session_state['side'] = st.session_state['area'] ** (1/2)
# st.write('Area of Sqaure Calculation')
# side = st.number_input("length:", key='side', on_change = calc_area)
# area = st.number_input("area:", key='area', on_change = calc_side)

# st.write(st.session_state)



# ####################################################

# def update_values():
#     st.session_state["value_1"] = st.session_state["final"][0]
#     st.session_state['value_2'] = st.session_state["final"][1]

# value_1 = st.selectbox('Select a value', [1, 2, 3], key='value_1')
# value_2 = st.selectbox('Select a value', [1, 2, 3], key='value_2')

# final = st.sidebar.selectbox('Select a value', [[1,2],[2,1]], key='final', on_change=update_values)
# st.write(st.session_state.final)


####################################################
#? usign on_click to update the value of a variable in the app
####################################################
# import streamlit as st
# import datetime

# st.title('Counter Example')
# if 'count' not in st.session_state:
#     st.session_state.count = 0
#     st.session_state.last_updated = datetime.time(0,0)

# def update_counter():
#     st.session_state.count += st.session_state.increment_value
#     st.session_state.last_updated = st.session_state.update_time

# with st.form(key='my_form'):
#     st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
#     st.number_input('Enter a value', value=0, step=1, key='increment_value')
#     submit = st.form_submit_button(label='Update', on_click=update_counter)

# st.write('Current Count = ', st.session_state.count)
# st.write('Last Updated = ', st.session_state.last_updated)



####################################################
#? Prueba template titulos, descripciones y descarga de pdf 
####################################################

# import streamlit as st

# st.sidebar.write("This is the sidebar")
# uno = "Dia 1 (Lima es lo mejor) "
	
# def ha(url):
#     st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"ColorMeBlue text”"}</h1>', unsafe_allow_html=True)
# #ha(uno)

# def basic(dia, actividad, fecha):
#     uno = "<font size='6'>"+dia+"</font> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<font size='6'>"+actividad+"</font> <br/>"+fecha         
#     return uno

# # uno = "<font size='6'>DAY 1</font> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<font size='6'>CUSCO TO LIMA</font> <br/> Agosto 16 de 2022"    
# uno = basic("DAY 1", "CUSCO TO LIMA", "Agosto 16 de 2022")
# dos = basic("DAY 2", "CUSCO TO LIMA", "Agosto 16 de 2022")
# def fidel(url):
#      st.markdown(f"""<p style='background-color:#E5E7E9 ;
#                                         color:black;
#                                         font-size:18px;
#                                         border-radius:3px;
#                                         line-height:30px;
#                                         padding-top:15px;
#                                         padding-bottom:15px;
#                                         padding-left:17px;
#                                         opacity:1'>
#                                         {url}</style>
#                                         <br></p>""", unsafe_allow_html=True)
# fidel(uno)

# st.markdown("##")
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
# st.markdown("##")
# fidel(dos)
# st.markdown("##")
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
    
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")
# with st.container():
#     col1, col2 = st.columns((1.5,4))
#     col1.markdown(":smirk:")
#     col2.subheader("Cusco City Tour (B/L/D) ")
#     col2.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca. ")

# st.markdown("##")
# st.markdown("##")
# col1, col2, col3 = st.columns(3)
# col1.image("https://media.istockphoto.com/id/636641586/es/foto/catedral-de-cuzco-en-el-per%C3%BA.jpg?s=612x612&w=0&k=20&c=j0_-xrQl00fIJjyGEVpxkgLm4b5WJy5fJLMhWCXWuNY=", width=420)
# col2.image("https://media.istockphoto.com/id/636641586/es/foto/catedral-de-cuzco-en-el-per%C3%BA.jpg?s=612x612&w=0&k=20&c=j0_-xrQl00fIJjyGEVpxkgLm4b5WJy5fJLMhWCXWuNY=", width=420)
# col3.image("https://media.istockphoto.com/id/636641586/es/foto/catedral-de-cuzco-en-el-per%C3%BA.jpg?s=612x612&w=0&k=20&c=j0_-xrQl00fIJjyGEVpxkgLm4b5WJy5fJLMhWCXWuNY=", width=420)
# st.markdown("##")
# st.markdown("##")
# st.markdown("##")
# st.markdown("##")
# with st.container():
#     cal1, cal2 = st.columns((2,1))
#     cal1.subheader("Lima City Tour (B/L/D) ")
#     cal1.subheader("★★★★")
#     cal1.markdown("#")
#     cal1.write("Lima es la capital de Perú ubicada en la árida costa del Pacífico del país. Pese a que su centro colonial se conserva, es una desbordante metrópolis y una de las ciudades más grandes de Sudamérica. El Museo Larco alberga una colección de arte precolombino y el Museo de la Nación recorre la historia de las civilizaciones antiguas de Perú. La Plaza de Armas y la catedral del siglo XVI son el núcleo del antiguo centro de Lima. ")
#     cal2.image("https://media.istockphoto.com/id/636641586/es/foto/catedral-de-cuzco-en-el-per%C3%BA.jpg?s=612x612&w=0&k=20&c=j0_-xrQl00fIJjyGEVpxkgLm4b5WJy5fJLMhWCXWuNY=", width=420)

# import autoit
# import time
# run = st.button("Imprimir")
# if run:
#     #! pip install -U pyautoit
#     #! https://pypi.org/project/PyAutoIt/
    
#     autoit.send("^p")
#     time.sleep(2)
#     st.info("Se imprimio")





####################################################
#? Mandatory Date Range Picker
# https://extras.streamlit.app/Mandatory%20Date%20Range%20Picker
# para mejorar la interfaz de usuario al seleccionar fechas
####################################################

# #
# from streamlit_extras.mandatory_date_range import date_range_picker
# import streamlit as st
# st.write(
#     """
#     This is an example of a date range picker that *always* returns a start and
#     end date, even if the user has only selected one of the dates. Until the
#     user selects both dates, the app will not run.
#     """
# )
# result = date_range_picker("Select a date range")
# st.write("Result:", result)

####################################################
#? streamlit toggle switch confirmar con  operaciones
# https://discuss.streamlit.io/t/streamlit-toggle-switch/32474
# para mejorar la interfaz de usuario al seleccionar
####################################################

# import streamlit as st
# import  streamlit_toggle as tog


# def requerir(url):
#     st.markdown(f'<h1 style="color:#D35400 ;font-size:20px; padding-top:1px ;">{url}</h1>', unsafe_allow_html=True)
# def confirmar(url):
#     st.markdown(f'<h1 style="color:#2ECC71 ;font-size:20px; padding-top:1px ;">{url}</h1>', unsafe_allow_html=True)


# st.subheader("Toggle Switch 🎵")

# col1, col3 = st.columns((7,1))

# with col3:
    
#     miau = tog.st_toggle_switch(label="", 
#                     key="Key1", 
#                     default_value=False, 
#                     label_after = False, 
#                     inactive_color = '#EC6100', 
#                     active_color="#26BF00", 
#                     track_color="#17202A"
#                     )

# with col1:
#     if miau:
#         confirmar("Confirmed")
#     else:
#         requerir("Required")
#     st.write("Cuzco es una ciudad de los Andes peruanos que fue la capital del Imperio Inca y es conocida por sus restos arqueológicos y la arquitectura colonial española. La Plaza de Armas es el centro de la ciudad antigua, con galerías, balcones de madera tallada y ruinas de murallas incas. El convento de Santo Domingo, de estilo barroco, se construyó sobre el Templo del Sol inca (Qoricancha) y tiene restos arqueológicos de cantería inca.")


####################################################
#? Sorteable elements
# https://github.com/ohtaman/streamlit-sortables

####################################################
import streamlit as st
from streamlit_sortables import sort_items


original_items = ['A', 'B', 'C', "D", "E", "F"]
# sorted_items = sort_items(original_items)

# st.write(f'original_items: {original_items}')
# st.write(f'sorted_items: {sorted_items}')
if "data" not in st.session_state:
    st.session_state.data = 0
if "modified"  not in st.session_state:
    st.session_state.modified = 0
if "actual"  not in st.session_state:
    st.session_state.actual = 0

if "counter" not in st.session_state:
    st.session_state.counter = 0

def data_changed():
    for x in st.session_state.actual:
        if x not in st.session_state.data:
            st.session_state.data.append(x)
    for x in st.session_state.data:
        if x not in st.session_state.actual:
            st.session_state.data.remove(x)

    st.session_state.modified = st.session_state.data 



values = st.multiselect("Select values", original_items, default= [original_items[0]], key="valores", on_change=data_changed )
st.session_state.counter += 1
st.session_state.actual = values 

if st.session_state.actual == [original_items[0]]:
    st.write("ok")
    sorted_items = sort_items(st.session_state.actual)
    st.session_state.data = sorted_items
else:    
    listita = []
    for x in st.session_state.actual:
        if x not in st.session_state.data:
            st.session_state.modified.append(x)
    for x in st.session_state.data:
        if x not in st.session_state.actual:
            st.session_state.data.remove(x)
    sorted_items = sort_items(st.session_state.modified + listita , key=None)
    st.session_state.data = sorted_items

st.write("st.session_state.data", st.session_state.data)



lista = ["","A", "B", "C", "D", "E", "F"]
act = st.multiselect("Select values", lista, key="miau", default=None )
st.write("act", act)


st.title("Sorteable elements")

import streamlit as st
from streamlit_sortables import sort_items

original_items = [
    {'header': 'first container',  'items': ['A', 'B', 'C']},
    {'header': 'second container', 'items': ['D', 'E', 'F']}
]

sorted_items = sort_items(original_items, multi_containers=True)

st.write(f'original_items: {original_items}')
st.write(f'sorted_items: {sorted_items}')





# ! Crear tablas  con buscador
# https://github.com/blackary/streamlit-keyup