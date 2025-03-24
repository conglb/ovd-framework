import pandas as pd
import os
from os.path import join
import subprocess
import concurrent.futures
from utils import get_folder_list, get_file_list, get_storing_scripts
import streamlit as st
import time
from datetime import datetime

st.set_page_config(
        page_title="Data Storing Module",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/conglb',
            'Report a bug': "https://github.com/conglb",
        }
    )
st.markdown("##### 1. [Data Collection Module](http://localhost:8511) &emsp; &emsp; [2. Data Cleaning Module](http://localhost:8512) &emsp; &emsp; [3. Data Storage Module] &emsp; &emsp; [4. Data Presentation Module](http://localhost:8514)")

# Directories for data 
#RAW_FILES_DIR = "../data/raw_files"
CLEANED_FILES_DIR = "../data/cleaned_files/"
SCRIPT_FILES_DIR = "./storing_scripts/"

# Tạo các thư mục nếu chưa có
os.makedirs(CLEANED_FILES_DIR, exist_ok=True)

def show_dataframe(df):
    st.write("Number of columns: {}".format(len(df.columns)))
    st.write("Number of rows: {}".format(len(df)))
    #st.dataframe(df)

def log_store(file_path):
    with open('./stored_files.log', "a") as f:
        f.write(f"{datetime.now()}: stored a new file at {file_path}\n")

# Log file download error
def log_error(task_name, error_msg):
    with open('./error_log.log', "a") as f:
        f.write(f"{datetime.now()} - {task_name} - ERROR: {error_msg}\n")

def log_performance(file_size, time_spent):
    with open('./performance_log.log', 'a') as f:
        f.write(f"{file_size},{time_spent}\n")

# Hàm chạy script làm sạch với subprocess
def run_storing_script(script_name, cleaned_file_path):
    try:

        subprocess.run(['python', os.path.join(SCRIPT_FILES_DIR, script_name), cleaned_file_path],capture_output=True, text=True,  check=True)
        log_store(cleaned_file_path)
        return 1
    except subprocess.CalledProcessError as e:
        st.error(f"Error while running subprocess the script: {e}")
        log_error(script_name, f"while store {cleaned_file_path}")
        return e.stderr

# Lấy danh sách các file dữ liệu
st.sidebar.header("Select Data Files and Storing Script")
folder_list = get_folder_list(CLEANED_FILES_DIR)
selected_folder = st.sidebar.selectbox("Choose a data folder", folder_list)

# Hiển thị danh sách file để người dùng chọn
if folder_list:
    file_list = get_file_list(join(CLEANED_FILES_DIR, selected_folder))
    selected_files = st.sidebar.multiselect("Choose files to store", file_list)

    if len(selected_files) == 1:
        cleaned_file_path = [os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file) for selected_file in selected_files ]
        st.write("W12: this feature is disabled")
        #df = pd.read_csv(cleaned_file_path[0])
        #show_dataframe(df)
    elif len(selected_files) > 1:
        cleaned_file_path = [os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file) for selected_file in selected_files ]
        tabs = st.tabs(selected_files)
        for index, tab in enumerate(tabs):
            with tab:
                st.write("W11: this feature is disabled")
                #df = pd.read_csv(cleaned_file_path[index])
                #show_dataframe(df)

    # Lấy danh sách các script làm sạch
    script_list = get_storing_scripts()
    selected_script = st.sidebar.selectbox("Choose a storing script", script_list)

    # Biến để lưu trạng thái xử lý
    storing_in_progress = st.sidebar.empty()
    stored_data_placeholder = st.empty()

    if st.sidebar.button("Store Data"):
        for selected_file in selected_files:
            cleaned_file_path = os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file)

            # Sử dụng ThreadPoolExecutor để thực hiện việc chạy script trong nền
            with concurrent.futures.ThreadPoolExecutor() as executor:
                storing_in_progress.text(f"Storing file '{selected_file}' using script '{selected_script}'...")
                future = executor.submit(run_storing_script, selected_script, cleaned_file_path)
                result = future.result()  # Chờ quá trình làm sạch hoàn tất

                if result==1:
                    st.success(f"File '{selected_file}' stored successfully.")
                else:
                    st.error(f"Error occurs when running script: \n {result}")
else:
    st.warning("No files available to clean.")


