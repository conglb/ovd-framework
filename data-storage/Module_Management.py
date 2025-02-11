import streamlit as st
from utils import get_file_list
from timesclaedb_adapter import get_database_info

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
num_tables, num_rows, db_size = get_database_info()
table_scorecard = """
<div class="ui four small statistics">
<div class="grey statistic">
    <div class="value">"""+str(num_tables)+"""
    </div>
    <div class="grey label">
    Tables
    </div>
</div>

<div class="grey statistic">
    <div class="value">"""+str(num_rows)+"""
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
    Data Storing Scripts
    </div>
</div>

<div class="grey statistic">
    <div class="value">
    """+str(db_size)+"""
    </div>
    <div class="label">
    Database Size
    </div>
</div>
</div>"""
table_scorecard += """<br><br><br>"""
st.markdown(table_scorecard, unsafe_allow_html=True)

st.markdown('###### Logs')
with st.container(height=320):
    tab1, tab2 = st.tabs(["Error", "Stored files"])
with tab1:
    with open('error_log.log', "r") as f:
        st.write(f.read())
with tab2:
    with open('stored_files.log', "r") as f:
        st.write(list(f))

