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
    st.markdown("[1. Data Collection Module] &emsp; &emsp; [2. Data Cleaning Module](http://localhost:8512) &emsp; &emsp; [3. Data Storage Module](http://localhost:8513) &emsp; &emsp; [4. Data Presentation Module](http://localhost:8514)")

    st.title("Data Collection Module")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)     
    local_css("style.css")

    # Statistics
    table_scorecard = """
    <div class="ui five small statistics">
    <div class="grey statistic">
        <div class="value">"""+"34"+"""
        </div>
        <div class="grey label">
        Tables
        </div>
    </div>
        <div class="grey statistic">
            <div class="value">"""+"234"+"""
            </div>
            <div class="label">
            Views
            </div>
        </div>
        <div class="grey statistic">
            <div class="value">"""+"34"+"""
            </div>
            <div class="label">
            Materialized Views
            </div>
        </div>    
    <div class="grey statistic">
        <div class="value">
        """+"34"+"""
        </div>
        <div class="label">
        Rows
        </div>
    </div>

    <div class="grey statistic">
        <div class="value">
        """+"dlkf"+"""
        </div>
        <div class="label">
        Data Size
        </div>
    </div>
    </div>"""
    table_scorecard += """<br><br><br>"""
    st.markdown(table_scorecard, unsafe_allow_html=True)

    # Listing files in folder raw_files
    col1, col2, col3 = st.columns(3)
    file_structure = list_files_in_directory('../data/raw_files')
    for index, (folder, files) in enumerate(file_structure.items()):
        tmp = index%3
        if tmp == 0:
            col = col1
        elif tmp ==1:
            col = col2
        else:
            col = col3

        with col:
            with st.expander(f"Folder: {folder} \n\n Path: /data/raw_files/{folder} \n\n Number of files: {len(files)} \n\n Status: Active \n\n ", expanded=False):
                if files:
                    for file in files:
                        st.write(file)
                else:
                    st.write("No files found in this folder.")
    
    with st.expander("Collecting log:", expanded=False):
        with open('downloaded_files.log', "r") as f:
            st.write(f.read())

    
if __name__ == '__main__':

    FRONTEND()

    if not hasattr(st, 'already_started_server'):
        st.already_started_server = True
        BACKEND()