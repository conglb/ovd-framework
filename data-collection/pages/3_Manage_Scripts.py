import concurrent
import subprocess
from streamlit_monaco import st_monaco
import streamlit as st
from utils import list_files_in_directory, get_collecting_script_list, SCRIPT_FILES_DIR
from os.path import join

st.title("Manage Data Collecting Scripts")

def read_script_file(path='./examples/collecting_script_template.py'):
    with open(path) as f:
        return f.read()
    return "error reading template file"

def run_collecting_script(script_name, extension, output_file_path):
    try:
        if extension == 'Python':
            process = subprocess.run(['python', join("collecting_scripts/", script_name+'.py'), output_file_path], check=True, capture_output=True, text=True)
            output = process.stdout
            if output:
                return {'status': 1, 'message': output}
            else:
                return {'status':0, 'message':output}
    except subprocess.CalledProcessError as e:
        return {'status':0, 'message':e}


@st.fragment
def build_Main_UI():
    col1, col2, col3 = st.columns(3)
    with col1: 
        function = st.radio("",["Create a new script", "Edit a script", "Run a script"],)

    with col2:
        extension = st.radio("Choose program language", ["Python", "Bash"])
        clickRun = st.button("Run")

    if function == 'Create a new script':
        script_path = './examples/collecting_script_template.py'
        with col3: 
            script_name = st.text_input('File name:')
    else:
        with col3:
            script_name = st.selectbox('Choose the script', options=get_collecting_script_list())
            script_path = SCRIPT_FILES_DIR + '/' + script_name
    content = st_monaco(value=read_script_file(script_path), height="600px", language="python")

    with col3:
        if st.button("Save"):
            if script_name:
                script_path = SCRIPT_FILES_DIR + '/' + script_name
                with open(script_path, "w") as file:
                    file.write(content)
            else:
                with st.sidebar:
                    st.error("Please fill in name for new script")
    
    if clickRun:
        with open('./collecting_scripts/_draft.py', "w") as file:
            file.write(content)
        with concurrent.futures.ThreadPoolExecutor() as executor:
                st.text(f"Running script ...")
                future = executor.submit(run_collecting_script, '_draft', extension=extension, output_file_path='./raw_files/')
                result = future.result() 

                if result['status']:
                    st.success(f"File runned successfully \n\n Output: {result['message']}.")
                else:
                    st.error(f"File runned with error \n\n Error: {result['message']}.")

build_Main_UI()

