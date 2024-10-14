import streamlit as st
import pandas as pd
import os
from os.path import join, isdir
import subprocess
import concurrent.futures

# Thư mục lưu file chưa làm sạch và đã làm sạch
RAW_FILES_DIR = "../data/raw_files"
CLEANED_FILES_DIR = "../data/cleaned_files"
SCRIPT_FILES_DIR = "./cleaning_scripts"

# Tạo các thư mục nếu chưa có
os.makedirs(CLEANED_FILES_DIR, exist_ok=True)

# Hàm lấy danh sách các file dữ liệu thô
def get_file_list(path):
    files = [x for x in os.listdir(path) if x.endswith('.csv')]
    return files

def get_folder_list(path):
    folders = [x for x in os.listdir(path) if isdir(join(path,x))]
    return folders

# Hàm lấy danh sách các script làm sạch
def get_cleaning_scripts():
    scripts = [f for f in os.listdir(SCRIPT_FILES_DIR) if f.endswith('.py')]
    return scripts

# Hàm chạy script làm sạch với subprocess
def run_cleaning_script(script_name, raw_file_path, output_file_path):
    try:
        # Gọi subprocess để chạy script với argument là FILE_PATH
        subprocess.run(['python', os.path.join(SCRIPT_FILES_DIR, script_name), raw_file_path, output_file_path], check=True)
        
        # Đọc lại file đã làm sạch sau khi script hoàn tất
        #cleaned_file_path = os.path.join(CLEANED_FILES_DIR, f"cleaned_{os.path.basename(raw_file_path)}")
        #cleaned_df = pd.read_csv(cleaned_file_path)

        return output_file_path
    except subprocess.CalledProcessError as e:
        st.error(f"Error running script: {e}")
        return None

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
st.markdown("[1. Data Collection Module](http://localhost:8501) &emsp; &emsp; [2. Data Cleaning Module] &emsp; &emsp; [3. Data Storage Module](http://localhost:8503) &emsp; &emsp; [4. Data Presentation Module](http://localhost:8504)")
st.title("Data Cleaning Module")

# Lấy danh sách các file dữ liệu
st.sidebar.header("Select a File and Cleaning Script")

folder_list = get_folder_list(RAW_FILES_DIR)
selected_folder = st.sidebar.selectbox("Choose a folder", folder_list)
if selected_folder:
    file_list = get_file_list(os.path.join(RAW_FILES_DIR, selected_folder))
    if file_list:
        selected_file = st.sidebar.selectbox("Choose a file to clean", file_list)

        # Lấy danh sách các script làm sạch
        script_list = get_cleaning_scripts()
        selected_script = st.sidebar.selectbox("Choose a cleaning script", script_list)

        # Biến để lưu trạng thái xử lý
        cleaning_in_progress = st.sidebar.empty()
        #cleaned_data_placeholder = st.empty()

        if st.sidebar.button("Clean Data"):
            # Create folder if not exists 
            output_dir_path = join(CLEANED_FILES_DIR, selected_folder)
            os.makedirs(output_dir_path, exist_ok=True)

            raw_file_path = os.path.join(RAW_FILES_DIR,selected_folder, selected_file)
            output_file_path = join(CLEANED_FILES_DIR, selected_folder, f"cleaned_{selected_file}")

            # Sử dụng ThreadPoolExecutor để thực hiện việc chạy script trong nền
            with concurrent.futures.ThreadPoolExecutor() as executor:
                cleaning_in_progress.text(f"Cleaning file '{selected_file}' using script '{selected_script}'...")
                future = executor.submit(run_cleaning_script, selected_script, raw_file_path, output_file_path)
                cleaned_file_path = future.result()  # Chờ quá trình làm sạch hoàn tất

                if cleaned_file_path is not None:
                    cleaned_df = pd.read_csv(cleaned_file_path)
                    st.success(f"File '{selected_file}' cleaned successfully.")
                    st.markdown("### Data after cleaning")
                    st.write("Number of columns: {}".format(len(cleaned_df.columns)))
                    st.write("Number of rows: {}".format(len(cleaned_df)))
                    st.dataframe(cleaned_df)
                else:
                    st.error("Error occurs when running script")

    else:
        st.warning("No CSV file in chosen folder")
else:
    st.warning("No folders found in raw_files")