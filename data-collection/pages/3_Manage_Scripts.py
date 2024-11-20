from streamlit_monaco import st_monaco
import streamlit as st
from utils import list_files_in_directory

st.title("Manage Data Collecting Scripts")

def read_script_file(path='./collecting_script_template.py'):
    with open(path) as f:
        return f.read()
    return "error reading template file"

def build_Main_UI():
    content = st_monaco(value=read_script_file(), height="600px", language="python")

    if st.button("Save"):
        st.write(content)

build_Main_UI()

