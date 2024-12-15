import streamlit as st
import pandas as pd
import sqlite3
import time

st.title("📊 Summary of Citizen Complaints")
st.subheader("Complaints Map")

# Filters
topic_filter = st.sidebar.text_input("Filter by Topic")
emotion_filter = st.sidebar.selectbox("Filter by Sentiment", ["All", "High", "Medium", "Low"])
state_filter = st.sidebar.text_input("Filter by State (Location)")

query = "SELECT * FROM complaints WHERE 1=1"
params = []
if topic_filter:
    query += " AND topic LIKE ?"
    params.append(f"%{topic_filter}%")
if emotion_filter != "All":
    query += " AND emotion_level = ?"
    params.append(emotion_filter)
if state_filter:
    query += " AND location LIKE ?"
    params.append(f"%{state_filter}%")

conn = sqlite3.connect("complaints.db")
try:
    df = pd.read_sql_query(query, conn, params=params)
    
    # Display statistics
    if not df.empty:
        # Assuming 'location' is a column in format "latitude, longitude"
        df[['latitude', 'longitude']] = df['location'].str.split(',', expand=True).astype(float)
        st.map(df.rename(columns={'latitude': 'lat', 'longitude': 'lon'}))
        st.dataframe(df)
    else:
        st.write("No data available with the selected filters.")
except sqlite3.Error as e:
    st.error(f"Error accessing the database: {e}")
finally:
    conn.close()