
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
import streamlit as st
from streamlit_quill import st_quill

with st.container():

    c1, c2 = st.columns([2, 1])

    with c1:
        content = st_quill(
            placeholder="Write here",
            html=True,
            readonly=False,
            key="none",
            
        )
        