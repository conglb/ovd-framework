import streamlit as st
import pandas as pd
import os
from os.path import join, isdir
import subprocess
import concurrent.futures
from utlis import get_file_list, get_folder_list, get_cleaning_scripts, SCRIPT_FILES_DIR, CLEANED_FILES_DIR, RAW_FILES_DIR



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
table_scorecard = """
<div class="ui three small statistics">
    <div class="grey statistic">
        <div class="value">"""+"234"+"""
        </div>
        <div class="label">
        Data Folders
        </div>
    </div>
<div class="grey statistic">
    <div class="value">
    """+"34"+"""
    </div>
    <div class="label">
    Data Cleaning Scripts
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
table_scorecard += """<br><br>"""
st.markdown(table_scorecard, unsafe_allow_html=True)

