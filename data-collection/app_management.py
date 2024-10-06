import streamlit as st
import pandas as pd
import json
import os
from flask import Flask
import threading
from api import BACKEND
from utils import list_files_in_directory


# Giao diện Streamlit chính
def FRONTEND():
    st.set_page_config(
        page_title="Data Collection Module",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
    st.markdown("[1. Data Collection Module] &emsp; &emsp; [2. Data Cleaning Module](http://localhost:8502) &emsp; &emsp; [3. Data Storage Module](http://localhost:8503) &emsp; &emsp; [4. Data Presentation Module](http://localhost:8504)")

    st.title("Data Collection Module")

    # Listing files in folder raw_files
    file_structure = list_files_in_directory('../data/raw_files')
    for folder, files in file_structure.items():
        with st.expander(f"Folder: {folder}", expanded=True):
            if files:
                for file in files:
                    st.write(file)
            else:
                st.write("No files found in this folder.")

    
if __name__ == '__main__':

    FRONTEND()

    if not hasattr(st, 'already_started_server'):
        st.already_started_server = True
        BACKEND()