
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
# Copy of main_page to create the cover of the program
#################################################### 


            