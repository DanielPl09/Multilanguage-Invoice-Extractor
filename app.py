from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#model=genai.GenerativeModel('gemini-pro-vision')
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        
        bytes_data=uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
            
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
        


st.set_page_config(page_title="Multilanguage Invoice Extractor")

st.header("Multilanguage Invoice Extractor")
st.markdown("**developed by:** Vishnukanth.k")


input=st.text_input("Input Prompt: ",key=input)
uploaded_file=st.file_uploader("Choose an image of the invoice",type=["jpg","jpeg","png"])

image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
you are an expert in understaing invoices. The attached document contains an image of an invoice in Hebrew. Convert the invoice image to coherent text containing key value pairs and table data of the given image.
Dont make up any infromation which is not explictily in the invoice, and print all the information in Hebrew.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)
