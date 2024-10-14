import streamlit as st
from utils import add_data_source, get_collecting_script_list

st.title("Add a New Data Source")

# Input for new data source details
name = st.text_input("Source Name")
data_category = st.selectbox("Category", ['AIS data', 'High frequency data', 'Middle frequency data', "Low frequency data", "Other"])
url = st.text_input("Source URL")
description = st.text_area("Source Description")
file_format = st.selectbox("File format", ['XML', 'API', 'HTTP', 'FTP', 'CSV', 'Path'])
collecting_script = st.selectbox("Collecting script", get_collecting_script_list)
collecting_frequency = st.selectbox("Collecting frequency", ['Hourly', 'Daily', 'Weekly', 'Monthly'])

# Add the data source when the button is clicked
if st.button("Add Source"):
    if name and url:
        add_data_source(name, data_category, url, description, file_format, collecting_script, collecting_frequency)
        st.success(f"Source '{name}' has been added successfully!")
    else:
        st.error("Please enter both a name and URL for the data source.")
