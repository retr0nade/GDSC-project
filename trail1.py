#all required libraries are imported
from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from mtranslate import translate
import google.generativeai as genai
import streamlit as st


genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #google api key is inputted here
model = genai.GenerativeModel("gemini-pro") #gemini pro is used here
chat = model.start_chat(history=[])


#function is defined 
def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response 

    
#gui changes are made here
st.set_page_config("Q&A Chatbot")
st.header("CONVERSATIONAL MULTILANGUAGE CHATBOT")
input = st.text_input("Input: ",key="input")
submit = st.button("GENERATE AND TRANSLATE")


#start of generating prompts and language translation
data = pd.read_excel(os.path.join('data', 'language.xlsx'),sheet_name='wiki') #excel file is read here
data.dropna(inplace=True) #all the N/A values are dropped
lang = data['name'].to_list() #langauge name is inputted into a list called lang
langlist=tuple(lang)
langcode = data['iso'].to_list() #langauge code is inputted into a list called langcode

# creating dictionary where langcode is key and lang is value
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}


#user selects choice from the sidebar
choice = st.sidebar.radio('SELECT LANGUAGE',langlist)


to_be_translated = str()

#once inut and submit both are executed then the generation and translation starts
if input and submit:
    response = get_gemini_response(input)
    for chunk in response: #for loop is used for longer lines of generated response
        st.subheader("RESPONSE")
        st.write(chunk.text)
        to_be_translated = chunk.text
        st.header('TRANSLATED RESPONSE')
        output = translate(to_be_translated,lang_array[choice]) #generated response gets translated line by line based on language choice given
        st.write(output)


#future scope
#this project can be further enhcanced to take input from different languages and also a TTS csn be implemeted in many languages 
#along with downloading the audio file 
#due to time restrictions the project could not be better
