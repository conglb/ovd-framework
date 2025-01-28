import pandas as pd
import os
from os.path import join
import subprocess
import concurrent.futures
from utils import get_folder_list, get_file_list, get_storing_scripts
import streamlit as st

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

# Thư mục lưu file chưa làm sạch và đã làm sạch
#RAW_FILES_DIR = "../data/raw_files"
CLEANED_FILES_DIR = "../data/cleaned_files/"
SCRIPT_FILES_DIR = "./storing_scripts/"

# Tạo các thư mục nếu chưa có
os.makedirs(CLEANED_FILES_DIR, exist_ok=True)

def show_dataframe(df):
    st.write("Number of columns: {}".format(len(df.columns)))
    st.write("Number of rows: {}".format(len(df)))
    st.dataframe(df)

# Hàm chạy script làm sạch với subprocess
def run_storing_script(script_name, raw_file_path):
    try:
        # Gọi subprocess để chạy script với argument là FILE_PATH
        subprocess.run(['python', os.path.join(SCRIPT_FILES_DIR, script_name), raw_file_path],capture_output=True, text=True,  check=True)
        
        return 1
    except subprocess.CalledProcessError as e:
        st.error(f"Error running the script: {e}")
        return e.stderr

# Lấy danh sách các file dữ liệu
st.sidebar.header("Select a File and Storing Script")
folder_list = get_folder_list(CLEANED_FILES_DIR)
selected_folder = st.sidebar.selectbox("Choose a folder", folder_list)

# Hiển thị danh sách file để người dùng chọn
if folder_list:
    file_list = get_file_list(join(CLEANED_FILES_DIR, selected_folder))
    selected_files = st.sidebar.multiselect("Choose a file to store", file_list)

    if len(selected_files) == 1:
        raw_file_path = [os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file) for selected_file in selected_files ]
        df = pd.read_csv(raw_file_path[0])
        show_dataframe(df)
    elif len(selected_files) > 1:
        raw_file_path = [os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file) for selected_file in selected_files ]
        tabs = st.tabs(selected_files)
        for index, tab in enumerate(tabs):
            with tab:
                df = pd.read_csv(raw_file_path[index])
                show_dataframe(df)

    # Lấy danh sách các script làm sạch
    script_list = get_storing_scripts()
    selected_script = st.sidebar.selectbox("Choose a storing script", script_list)

    # Biến để lưu trạng thái xử lý
    storing_in_progress = st.sidebar.empty()
    stored_data_placeholder = st.empty()

    if st.sidebar.button("Store Data"):
        for selected_file in selected_files:
            raw_file_path = os.path.join(CLEANED_FILES_DIR, selected_folder, selected_file)

            # Sử dụng ThreadPoolExecutor để thực hiện việc chạy script trong nền
            with concurrent.futures.ThreadPoolExecutor() as executor:
                storing_in_progress.text(f"Storing file '{selected_file}' using script '{selected_script}'...")
                future = executor.submit(run_storing_script, selected_script, raw_file_path)
                result = future.result()  # Chờ quá trình làm sạch hoàn tất

                if result==1:
                    st.success(f"File '{selected_file}' stored successfully.")
                else:
                    st.error(f"Error occurs when running script: \n {result}")
else:
    st.warning("No files available to clean.")


