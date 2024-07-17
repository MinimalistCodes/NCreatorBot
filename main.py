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
    page_title="SalesTrek - AI Sales Script Generator",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

#save to pdf function
def save_chat_to_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for message in chat_history:
        role = "User" if message["role"] == "user" else "Assistant"
        content = message["content"]
        pdf.multi_cell(0, 10, f"{role}: {content}")
        pdf.ln(10)

    pdf_file = "chat_history.pdf"
    pdf.output(pdf_file)
    return pdf_file

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

#load styles.css
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# UI Title
st.markdown("## NotionHelper - Your AI Notion Assistant")
st.markdown("### Ask me anything about Notion and I will help you with the best possible answer!")
st.markdown("---")  # Horizontal line
    
    
# Don't show Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []  # Initialize chat history
    #clear chat history
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({"role": "assistant", "content": "Welcome! Type a message to get started."})


# Display chat messages
with st.container():  # Use container for styling
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
# User Input
if prompt := st.chat_input("Your message"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display "Sales Coach is typing..."
    with st.chat_message("assistant"):
        message_placeholder = st.empty() 
        message_placeholder.markdown("Sales Coach is typing...")

    # Get and append AI response (with a delay to simulate typing)
    time.sleep(1)  # Adjust the delay as needed
    response = ai_sales_coach(prompt)
    message_placeholder.markdown(response)  # Update the placeholder
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear user input after sending message
    st.session_state.messages = st.session_state.messages[-100:]  # Limit chat history to last 100 messages
    
    
  
