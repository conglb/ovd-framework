import streamlit as st
from utils import add_data_source

st.title("Add a New Data Source")

# Input for new data source details
name = st.text_input("Source Name")
url = st.text_input("Source URL")
description = st.text_area("Source Description")
file_format = st.selectbox("File format", ['XML', 'API', 'HTTP', 'FTP', 'CSV', 'Path'])
collecting_script_name = st.selectbox("Collecting script", ['s1.py', 's2.py'])
category = st.selectbox("Category", ['AIS data', 'High frequency data', 'Middle frequency data', "Low frequency data"])

# Add the data source when the button is clicked
if st.button("Add Source"):
    if name and url:
        add_data_source(name, url, description)
        st.success(f"Source '{name}' has been added successfully!")
    else:
        st.error("Please enter both a name and URL for the data source.")
