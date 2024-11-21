from streamlit_monaco import st_monaco
import streamlit as st
from utils import list_files_in_directory, get_collecting_script_list, SCRIPT_FILES_DIR

st.title("Manage Data Collecting Scripts")

def read_script_file(path='./examples/collecting_script_template.py'):
    with open(path) as f:
        return f.read()
    return "error reading template file"

def build_Main_UI():
    col1, col2, col3 = st.columns(3)
    with col1: 
        operator = st.radio(
            "",
            ["Create a new script", "Edit a script", "Run a script"],
            
        )
    with col2:
        extension = st.radio("Choose program language", ["Python", "Bash"])
    if operator == 'Create a new script':
        script_path = './examples/collecting_script_template.py'
        with col3: 
            st.text_input('File name:')
    else:
        with col3:
            script_name = st.selectbox('Choose the script', options=get_collecting_script_list())
            script_path = SCRIPT_FILES_DIR + '/' + script_name
    content = st_monaco(value=read_script_file(script_path), height="600px", language="python")

    with col3:
        if st.button("Save"):
            st.write(content)
    with col2:
        if st.button("Run"):
            st.error("Not yet constructed")
        
build_Main_UI()

