import os 
import streamlit as st
import requests
import pandas as pd
import sqlite3
import time
from dotenv import load_dotenv

load_dotenv()

# ------------------ DATABASE CONFIGURATION ------------------ #
conn = sqlite3.connect("complaints.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                location TEXT,
                complaint TEXT,
                emotion_level TEXT,
                resolution TEXT,
                topic TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()
conn.close()

# ------------------ MAIN INTERFACE ------------------ #
def main():
    # Sidebar
    st.sidebar.title("Settings")
    
    # API Key Input
    api_key = st.sidebar.text_input("🔑 Enter your API Key", type="password", value=os.environ.get('GROK_API_KEY'))
    if api_key:
        st.session_state.api_key = api_key
    
    # Name and Location Input
    name = st.sidebar.text_input("🧑 Full Name", value=st.session_state.get("name", ""))
    location =st.sidebar.text_input("📍 Location (coordinates)", value=st.session_state.get("location", ""))
    if name and location:
        st.session_state.name = name
        st.session_state.location = location

    # Validate API Key
    if "api_key" not in st.session_state:
        st.sidebar.error("Please enter a valid API Key.")
        st.stop()
    
    # ------------------ MAIN PAGE ------------------ #
    st.title("👩‍💼 Welcome to AgentKaren.gov")
    st.image("sources/agent_doge_5.jpg", use_column_width=True, caption="Agent Karen in Action!")

    # Karen's Story
    st.subheader("📖 The Story of Karen")
    st.markdown("""
    Once upon a time, **Karen** was notorious in her neighborhood for complaining about everything: traffic, potholes, customer service, and even the weather 🌧️.  
    One day, the **U.S. Government** decided to give her an **official role as a Citizen Complaints Agent**.  
    Now, Karen **listens to the citizens' problems**, **proposes solutions**, and understands the importance of being **empathetic** and **efficient**.  

    Thanks to **AgentKaren.gov**, Karen uses the latest in Artificial Intelligence technology to:
    - **Listen to citizens** 🗣️
    - Analyze issues using advanced models (like **Grok AI** 🤖)
    - Provide clear and effective solutions 💡
    """)

    st.image("sources/structure.png", use_column_width=True, caption="Operational Structure 🛠️")
    
    # Platform Explanation
    st.subheader("🚀 How Does AgentKaren.gov Work?")
    st.markdown("""
    1. **Enter your information**: Your name and location help personalize your experience.
    2. **Describe your problem**: Karen is ready to hear any complaint or suggestion.
    3. **Intelligent Processing**: The system analyzes the text using **Grok AI** to detect **sentiment** and **topic**.
    4. **Get a response**: Receive solutions or recommendations that can help resolve your issue.  

    Karen is no longer just a complainer! Now she's an **Agent of Positive Change** 🚀.
    """)

    # Start Message
    st.info("💡 **Tip**: Use the sidebar to enter your API Key, name, and location before you start.")

if __name__ == "__main__":
    main()