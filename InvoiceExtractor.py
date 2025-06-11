from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load Gemini pro model and get responses
model=genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image_data,prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
            "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
            "data": bytes_data, # Get the bytes data of the uploaded file
            }
        ]
        
        return image
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Multilanguage Inovice Extractor")
input=st.text_input("Input: ", key="input")
uploaded_file=st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="image")
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices.  We will upload a image as inoice and you will have to answer any questions based
on the uploaded invoice image."""

# When submit is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)