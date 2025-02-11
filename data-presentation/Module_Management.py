import streamlit as st


# Streamlit App
st.set_page_config(
        page_title="Data Presentation Module",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
st.markdown("##### 1. [Data Collection Module](http://localhost:8511) &emsp; &emsp; [2. Data Cleaning Module](http://localhost:8512) &emsp; &emsp; [3. Data Storage Module](http://localhost:8513) &emsp; &emsp; [4. Data Presentation Module]")

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">',
                unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)    
local_css("style.css")

# Statistics
table_scorecard = """
<div class="ui two small statistics">
<div class="grey statistic">
    <div class="value">"""+"34"+"""
    </div>
    <div class="grey label">
    Dashboard
    </div>
</div>

<div class="grey statistic">
    <div class="value">
    """+"dlkf"+"""
    </div>
    <div class="label">
    Database Size
    </div>
</div>
</div>"""
table_scorecard += """<br><br>"""
st.markdown(table_scorecard, unsafe_allow_html=True)


