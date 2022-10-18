"""

Fidel Alberto Ramos Calachahuin
VittaQuant Inc.
Aplication 1 of example to the webpage
Cloud Streamlit

"""
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



# # CREATION OF "RECIBO DE VENTA"

# st.set_page_config(layout="wide",#"centered", 
#     page_icon="🗽",
#     page_title="Mi empresa")

# # Everything is accessible via st.secrets :

# #password_guess = st.sidebar.text_input('Contraseña')
# #if password_guess != st.secrets["db_password"]:
# #    st.stop()
# # ------------------------------------------
# st.sidebar.info("Escribe el nombre de tu clientes ")


# st.title("Generador de recibos 👌")

# st.write(
#     "Con esta aplicación podras descargar un pdf de tus recibos de pago automaticamente"
# )



# left, right = st.columns(2)

# right.write("Tu recibo se verá de esta forma")


# env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
# template = env.get_template("template.html")


# left.write("Llena tus datos:")
# form = left.form("template_form")
# student = form.text_input("Nombre del Cliente")
# course = form.selectbox(
#     "Productos",
#     ["Viaje a Cusco", "Un curso de ingles", "Un pollo a la brasa"],
#     index=0,
# )
# grade = form.slider("Precio", 1, 100, 60)
# submit = form.form_submit_button("Generar")


# if submit:
#     html = template.render(
#         student=student,
#         course=course,
#         grade=f"{grade} soles",#grade=f"{grade}/100",
#         date=date.today().strftime("%B %d, %Y"),
#     )
#     # 2 rows  DELETE  to work in Windows-------------------
#     # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
#     # pdf=pdfkit.from_string(html, False, configuration=config)
    
#     # 1 row  to put the app in cloud ----------------------
#     pdf = pdfkit.from_string(html, False)
    

#     right.success("🎉 ¡Tu recibo fue generado exitosamente!")
#     # st.write(html, unsafe_allow_html=True)
#     # st.write("")
#     right.download_button(
#         "⬇️ Download PDF",
#         data=pdf,
#         file_name="recibo.pdf",
#             mime="application/octet-stream",
#     )
    
# END OF "RECIBO DE VENTA"


# Prueba de sistema en base a tutorial
# https://towardsdatascience.com/convert-html-to-pdf-using-python-4df78b40de1b


import pdfkit

#Define path to wkhtmltopdf.exe
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

#Define path to HTML file
path_to_file = 'sample.html'
# url = 'https://wkhtmltopdf.org/'




# CREATION OF "RECIBO DE VENTA"

st.set_page_config(layout="wide",#"centered", 
    page_icon="🗽",
    page_title="Mi empresa")

# Everything is accessible via st.secrets :

#password_guess = st.sidebar.text_input('Contraseña')
#if password_guess != st.secrets["db_password"]:
#    st.stop()
# ------------------------------------------
st.sidebar.info("App Peruvian Sunrise")


st.title("Programa de Viajes")

st.write(
    "Con esta aplicación podras descargar un pdf con las configuraciones de tu viaje de forma personalizada"
)



left, right = st.columns(2)




left.write("Llena los datos")
form = left.form("template_form")
student = form.multiselect("Actividades",["Willkommen in Lima","Freier Tag in Cus","Ankunft in Arequipa und Freier Tag in Arequip","Von den Anden in den Dschunge"],default="Willkommen in Lima")
cantidad = len(student)
if cantidad == 1:
    a=student[0]
if cantidad == 2:
    a=student[0]
    b=student[1]
if cantidad == 3:
    a=student[0]
    b=student[1]
    c=student[2]
if cantidad == 4:
    a=student[0]
    b=student[1]
    c=student[2]
    d=student[3]
price = form.number_input("Precio",2000,5000)
submit = form.form_submit_button("Generar")



imagenes ={ "Willkommen in Lima": ["https://www.hajosiewer.de/wp-content/uploads/Paraglider-an-der-K%C3%BCste-von-Lima.jpg","https://d26gc54f207k5x.cloudfront.net/media/public/cache/800x800/2019/02/14/peru-lima-plaza.jpeg","https://d13d0f5of5vzfo.cloudfront.net/images/products/8a0092ff7b3ad211017b720ac8694fab/large_AdobeStock_107539601_lindrik_online_800x600.jpg"],
           "Freier Tag in Cus":["https://www.perurail.com/wp-content/uploads/2020/11/Machu-Picchu-la-Ciudadela-Inca.jpg","https://turismoi.pe/uploads/city/image/20775/large_cusco.jpg","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZn0aeL4sYldq2gH0mA7Q_Rn_xVdy23YQRJw&usqp=CAU"],
           "Ankunft in Arequipa und Freier Tag in Arequip":["https://perumin.com/perumin34/assets/uploads/images/4135c-foto-arequipa.jpg","https://thumbs.dreamstime.com/b/stratovolcano-el-misti-arequipa-per%C3%BA-40716272.jpg","https://bananomeridiano.com/wp-content/uploads/2019/06/que-ver-en-arequipa-plaza-de-armas.jpg"],
           "Von den Anden in den Dschunge":["https://cdn.getyourguide.com/img/location/5df35b210202a.jpeg/70.jpg","https://lp-cms-production.imgix.net/2021-04/shutterstockRF_1021961164.jpg","https://www.sandovallake.com/wp-content/uploads/2019/06/canopy-tours-sandoval-lake-reserve-2.jpg"]}


env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())

if submit:
    if cantidad == 1:
        template = env.get_template("sample_1.html")
        html = template.render(
            student=student,
            a=a,
            imag_1a = imagenes[a][0],
            imag_2a = imagenes[a][1],
            imag_3a = imagenes[a][2],
            date=date.today().strftime("%B %d, %Y"),
            price=f"The total price is {price} USD"
        )
    if cantidad == 2:
        template = env.get_template("sample_2.html")
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
        template = env.get_template("sample_3.html")
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
        template = env.get_template("sample_4.html")
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
    # 2 rows  DELETE  to work in Windows-------------------
    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # pdf=pdfkit.from_string(html, False, configuration=config)
    
    # 1 row  to put the app in cloud ----------------------
    
    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(html, False, configuration=config, css='sample.css')
    #Convert HTML file to PDF
    # pdf = pdfkit.from_file(path_to_file, output_path='peruvian.pdf', configuration=config, css='sample.css')

    right.success("🎉 ¡Tu recibo fue generado exitosamente!")
    # st.write(html, unsafe_allow_html=True)
    # st.write("")
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="recibo.pdf",
            mime="application/octet-stream",
    )
