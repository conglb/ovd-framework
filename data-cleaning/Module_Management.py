import streamlit as st
import pandas as pd
import os
from os.path import join, isdir
import subprocess
import concurrent.futures
from utlis import get_file_list, get_folder_list, get_cleaning_scripts, SCRIPT_FILES_DIR, CLEANED_FILES_DIR, RAW_FILES_DIR, list_files_in_directory



# Streamlit App
st.set_page_config(
        page_title="Data Cleaning Module",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
st.markdown("##### [1. Data Collection Module](http://localhost:8511) &emsp; &emsp; [2. Data Cleaning Module] &emsp; &emsp; [3. Data Storage Module](http://localhost:8513) &emsp; &emsp; [4. Data Presentation Module](http://localhost:8514)")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    
local_css("style.css")

# Statistics
table_scorecard = """<br>
<div class="ui three small statistics">
    <div class="grey statistic">
        <div class="value">"""+"2"+"""
        </div>
        <div class="label">
        Data Folders
        </div>
    </div>
<div class="grey statistic">
    <div class="value">
    """+"3"+"""
    </div>
    <div class="label">
    Data Cleaning Scripts
    </div>
</div>

<div class="grey statistic">
    <div class="value">
    """+"1.3 GB"+"""
    </div>
    <div class="label">
    Data Size
    </div>
</div>
</div>"""
table_scorecard += """<br><br>"""
st.markdown(table_scorecard, unsafe_allow_html=True)


# Listing files in folder raw_files
st.markdown('###### Cleaned data folders')
col1, col2, col3 = st.columns(3)
file_structure = list_files_in_directory('../data/cleaned_files')
for index, (folder, files) in enumerate(file_structure.items()):
    tmp = index%3
    if tmp == 0:
        col = col1
    elif tmp ==1:
        col = col2
    else:
        col = col3

    with col:
        with st.expander(f"Folder: {folder} \n\n Path: /data/cleaned_files/{folder} \n\n Number of files: {len(files)} \n\n  ", expanded=False):
            if files:
                for file in files:
                    st.write(file)
            else:
                st.write("No files found in this folder.")

# Show logs
col1, col2 = st.columns(2)
with col1:
    st.markdown('###### Logs')
with st.container(height=320):
    tab1, tab2 = st.tabs(["Cleaning log", "Error"])
    with tab1:
        with open('cleaned_files.log', "r") as f:
            st.write(f.read())


