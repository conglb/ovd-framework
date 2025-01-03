import streamlit as st
from utils import get_file_list


# Streamlit App
st.set_page_config(
        page_title="Data Storage Module",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
st.markdown("##### [1. Data Collection Module](http://localhost:8511) &emsp; &emsp; [2. Data Cleaning Module](http://localhost:8512) &emsp; &emsp; [3. Data Storage Module] &emsp; &emsp; [4. Data Presentation Module](http://localhost:8514)")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    
local_css("style.css")

# Statistics
table_scorecard = """
<div class="ui four small statistics">
<div class="grey statistic">
    <div class="value">"""+"4"+"""
    </div>
    <div class="grey label">
    Tables
    </div>
</div>

<div class="grey statistic">
    <div class="value">"""+"3474"+"""
    </div>
    <div class="label">
    Rows
    </div>
</div>

<div class="grey statistic">
    <div class="value">
    """+"2"+"""
    </div>
    <div class="label">
    Data Collecting Scripts
    </div>
</div>

<div class="grey statistic">
    <div class="value">
    """+"10 MB"+"""
    </div>
    <div class="label">
    Stored Data Size
    </div>
</div>
</div>"""
table_scorecard += """<br><br>"""
st.markdown(table_scorecard, unsafe_allow_html=True)


