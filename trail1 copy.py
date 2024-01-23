from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from mtranslate import translate
import google.generativeai as genai
import streamlit as st
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response 
    
st.set_page_config("Q&A Chatbot")
st.header("CONVERSATIONAL CHATBOT")


input = st.text_input("Input: ",key="input")
submit = st.button("send")



#start of language translation

# read language dataset
data = pd.read_excel(os.path.join('data', 'language.xlsx'),sheet_name='wiki')
data.dropna(inplace=True)
lang = data['name'].to_list()
langlist=tuple(lang)
langcode = data['iso'].to_list()

# create dictionary of language and 2 letter langcode
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# layout
st.title("Language Translation app")
input = st.text_area("INPUT",height=200)

choice = st.sidebar.radio('SELECT LANGUAGE',langlist)
# I/O
if len(input) > 0 :
    try:
        output = translate(input,lang_array[choice])
        st.text_area("TRANSLATED TEXT",output,height=50)
    except Exception as e:
        st.error(e)

submit = st.button("TRANSLATE")



#chat history function

if 'chat_history' not in st.session_state:
    st.session_state['CHAT_HISTORY'] = []


st.subheader("CHAT_HISTORY: ")       
for role,response in st.session_state["CHAT_HISTORY"]:
    st.write(f"{role}:{response}")
    
    
    
