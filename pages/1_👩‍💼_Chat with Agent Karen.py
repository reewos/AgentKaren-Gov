import os
import streamlit as st

from utils.grok_api import GrokAPI
from utils.functions import save_complaint

# Page Configuration
st.title("👩‍💼🤖 Chat with AgentKaren.gov")

# System Prompt for KarenGov
system_prompt = """
You are KarenGov, an empathetic and highly attentive AI designed to assist citizens with their complaints. Your role is to:
- Listen carefully to each user's concerns.
- Understand and empathize with their emotions and situation.
- Respond in a calm, supportive, and professional tone.
- Validate the user's feelings while offering practical solutions or steps to resolve their issues.
- Always aim to make the user feel heard, understood, and respected.

Remember:
- Use language that shows you care and understand the user's perspective.
- If the user seems upset, acknowledge their frustration or disappointment.
- Provide clear, concise information or steps for resolution where applicable.
- Avoid jargon unless explaining technical terms is necessary for understanding.

Here's an example response for a complaint about a lost document:

'User: I lost my birth certificate, and I need it for my new job!'
KarenGov: 'I understand how stressful this must be for you, especially with your new job on the line. Let's see how we can help you replace your birth certificate. Here's what you can do...'
"""

# Welcome Message
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm AgentKaren.gov. How may I assist you today?"}]
    # Add system prompt to the initial messages
    st.session_state.messages.insert(0, {"role": "system", "content": system_prompt})

# Display messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.sidebar.title("Settings")
    
# API Key Input
api_key = st.sidebar.text_input("🔑 Enter your API Key", type="password", value=os.environ.get('GROK_API_KEY'))
if api_key:
    st.session_state.api_key = api_key

# Name and Location Inputs
name = st.sidebar.text_input("🧑 Full Name", value=st.session_state.get("name", ""))
location =st.sidebar.text_input("📍 Location (coordinates)", value=st.session_state.get("location", ""))
if name and location:
    st.session_state.name = name
    st.session_state.location = location

# Validate API Key
if "api_key" not in st.session_state:
    st.sidebar.error("Please enter a valid API Key.")
    st.stop()

# User Input
user_input = st.chat_input("Describe your complaint...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process complaint
    grok_api = GrokAPI(st.session_state.api_key)
    try:
        emotion_level, topic = grok_api.detect_sentiment(st.session_state.messages[1:])
    except Exception as e:
        emotion_level = 'Medium'
        topic = 'NA'
        print(f"Error in detect_sentiment: {e}")
    response = grok_api.chat_response(st.session_state.messages)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Save complaint
    if emotion_level:
        save_complaint(st.session_state.name, st.session_state.location, user_input, emotion_level, response, topic)