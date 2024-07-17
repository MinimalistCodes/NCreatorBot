import time
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os, sys, json
from fpdf import FPDF

# Load environment va   riables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


st.set_page_config(
    page_title="NotionHelper - Your AI Notion Assistant",
    page_icon=":robot:",
    layout="wide",
)


def ai_sales_coach(user_input):
    
    prompt = f"""
      I would like you to act as a professional web developer; your job will be to design notion widgets out of HTML, CSS, and JavaScript. 
      I require each code to be in separate files. 
      We will be using them to embed within a notion page
      I would also like you to be a certified notion professional and aide me in ideas for templates to create and sell. 
      They'll be solutions for sales and cybersecurity professionals. 
      You'll help me with fully fleshed out templates when asked so I can know and understand how to build each page, including all formulas, both simple and advanced. 
      
      
      Please provide a comprehensive response to the following request:
      {user_input}
      """
    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
    return llm.invoke(prompt)


# UI Title
st.markdown("## NotionHelper - Your AI Notion Assistant")
st.markdown("### Ask me anything about Notion and I will help you with the best possible answer!")
st.markdown("---")  # Horizontal line
    
    
# Don't show Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize chat history
    # Welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Welcome! Type 'help' to get started!"})

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Sales Coach:** {message['content']}")
    st.markdown("---")  # Separate messages with a horizontal line

# User Input
with st.form(key='user_input_form'):
    user_input = st.text_area(label='Your message')
    submit_button = st.form_submit_button(label='Send')

if submit_button:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get and append AI response
    response = ai_sales_coach(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
  
