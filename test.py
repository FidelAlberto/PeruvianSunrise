
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
# Pop UP message in streamlit app
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
import extra_streamlit_components as stx
import streamlit as st
val = stx.stepper_bar(steps=["Ready", "Get Set", "Go"])
st.info(f"Phase #{val}")
