#  I use this to create a Iam user in AWS and get the access key and secret access key.
#  https://www.youtube.com/watch?v=JmrYZPjSDl4

# Then I follow the instructions 
#  https://m-germanengineer.medium.com/tutorial-launch-saleable-streamlit-dashboards-aws-part-1-f7f5372e66e

# to upload files  type .png .mp4 or audio use this steps
# https://discuss.streamlit.io/t/uploading-a-video-file-to-an-aws-s3-bucket/30942

#################################################### 
# Upload and download images from S3 AWS  with streamlit interface
#################################################### 

import streamlit as st
import os
import boto3
from botocore.exceptions import ClientError
import requests 

# Iam using the account IAM ""
bucket_name = "peruviansunrise-storage"
region_bucket='sa-east-1'
# S3_KEY = st.secrets["db_username"]
# S3_SECRET = st.secrets["db_password"]

S3_KEY = "AKIARCQ5LPGGXYOEXLWC"
S3_SECRET = "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"

# connect to s3 service and download a file from S3 bucket
def get_link(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',aws_access_key_id = S3_KEY, aws_secret_access_key = S3_SECRET,region_name = region_bucket)
    
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response



    
    
# You should put your data here like : appl.csv, logo.png, etc.
# url = get_link(bucket_name, 'ejemplo.PNG')

# if url is not None:
#     response = requests.get(url)

# st.header("Image from S3")
# st.image(url, width=200)

#################################################### 
 
import time
# to create and upload a file to S3 bucket
def uploadimageToS3(file, bucket, s3_file):
    s3 = boto3.client('s3',
                      region_name=region_bucket,
                      aws_access_key_id= S3_KEY,
                      aws_secret_access_key=S3_SECRET)
    
    try:
        # upload_file()   is used just to  work with .cvs not with .png .mp4 or audio
        s3.upload_fileobj(file, bucket, s3_file)
        st.success('File Successfully Uploaded')
        return True
    except FileNotFoundError:
        time.sleep(9)
        st.error('File not found.')
        return False     

# c1, c2 = st.columns(2)
# c1.subheader("Upload a PNG File")


# uploaded_image = c1.file_uploader("Select an PNG file")

# if uploaded_image is not None:
#     # this is call "internet media types" like for example : "video/mp4"
#     if uploaded_image.type != "image/png":  
#         c1.error('Only PNG images are supported. Please upload a different file')
        
#     else:
#         c1.success(uploaded_image.name + ' Selected')
        
#         if c1.button('Upload'):
#             with st.spinner('Uploading...'):
#                 # here is important to (put  the data itself, bucket_name, and the name that you want to save in s3)
#                 uploadimageToS3(uploaded_image,bucket_name , uploaded_image.name)

#################################################### 
# delete one object from S3 bucket  using another user in group = "s3storage"
#################################################### 

# def delete_s3_file(bucket_name, name_actual):
#     """
#     This is  a function to copy a file  and delete the original file
#     """
#     try:
#         s3 = boto3.client('s3',
#                         region_name='sa-east-1',
#                         aws_access_key_id= "AKIARCQ5LPGGVMGM6N6M",
#                         aws_secret_access_key="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")
        
#         s3.delete_object(Bucket=bucket_name, Key=name_actual)
#     # put this exception is really important
#     except Exception as e:
#         pass 


# delete_s3_file(bucket_name, "cuscolandia.png")



# this use a user with group="s3-full-2"
# not delete because this doesn't work
def copy_and_delete_s3_file(bucket_name, name_actual, name_new):
    """
    This is  a function to copy a file  and delete the original file
    """
    try:
        client= boto3.client('s3',aws_access_key_id = S3_KEY, 
                                aws_secret_access_key = S3_SECRET)
        
        client.copy_object(Bucket=bucket_name, CopySource=bucket_name+"/"+name_actual, Key=name_new)
        client.delete_object(Bucket=bucket_name, Key=name_actual)
    # put this exception is really important
    except Exception as e:
        pass 
    
# copy_and_delete_s3_file(bucket_name,"miau_asdg_3.png", "fidel_ramos.png" )



#################################################### 
# delete one object from S3 bucket  using another user in group = "s3storage"
#################################################### 

# this user used administrator privileges 
import boto3
def delete_s3_file(bucket_name, name_actual):
    #  jefaso is a user
    s3 = boto3.resource('s3',aws_access_key_id = S3_KEY, 
                                    aws_secret_access_key = S3_SECRET)
    s3.Object(bucket_name, name_actual).delete()
        


