


from datetime import datetime
from pathlib import Path
import streamlit as st
import streamlit_pydantic as sp
from typing import Optional, List
from streamlit_pydantic.types import FileContent
from pydantic import BaseModel, Field
from PyPDF2 import PdfFileWriter, PdfFileReader
import base64


st.sidebar.subheader("VittaQuant")
lenguage = ["English", "Spanish", "Deutsch"]
lenguage = st.selectbox("Select your lenguage", lenguage)

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
        col1, col2 = st.columns(2)
        col1.image("imagenes/1a.png", width=200)
        col2.image("imagenes/2a.png", width=200)
        option_1a = col1.checkbox("Select", key="1a")
        option_2a = col2.checkbox("Select", key="2a")
        
        if option_1a:
            data_2 = merge_pdfs("imagenes/1.pdf")
            
        if option_2a:
            data_2 = merge_pdfs("imagenes/2.pdf")   
        if data_2==None:
            st.stop()
    if lenguage=="Spanish":
        col1, col2 = st.columns(2)
        col1.image("imagenes/3a.png", width=200)
        col2.image("imagenes/4a.png", width=200)
        option_3a = col1.checkbox("Select", key="3a")
        option_4a = col2.checkbox("Select", key="4a")
        
        if option_3a:
            data_2 = merge_pdfs("imagenes/3.pdf")
            
        if option_4a:
            data_2 = merge_pdfs("imagenes/4.pdf")  
        if data_2==None:
            st.stop()
    if lenguage=="Deutsch":
        col1, col2 = st.columns(2)
        col1.image("imagenes/5a.png", width=200)
        col2.image("imagenes/6a.png", width=200)
        option_5a = col1.checkbox("Select", key="5a")
        option_6a = col2.checkbox("Select", key="6a")
        
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







