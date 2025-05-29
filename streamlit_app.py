import streamlit as st
import openai
import os
from dotenv import load_dotenv
from chat_handler import get_bot_response  # Use your existing logic
from token_usage import extract_token_usage, estimate_cost

# Load environment variables
load_dotenv(dotenv_path="confidential.env")

# Set your OpenAI API key
openai.api_key = os.getenv("openai_api_key")  # Ideally use st.secrets for deployment

# Set up Streamlit page config
st.set_page_config(page_title="Chitti Chatbot", page_icon="🤖")

st.title("🤖 Chitti - Your Car Knowledge Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, text = message
    if role == "user":
        st.chat_message("user").write(text)
    else:
        st.chat_message("assistant").write(text)

# Chat input
user_input = st.chat_input("Ask Chitti about cars...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)

    with st.spinner("Chitti is typing..."):
        # Get response from chatbot
        bot_response = get_bot_response(user_input, st.session_state.messages)
        st.session_state.messages.append(("assistant", bot_response))

        st.chat_message("assistant").write(bot_response)
