import streamlit as st
import pandas as pd
import os
import subprocess
import concurrent.futures

# Thư mục lưu file chưa làm sạch và đã làm sạch
RAW_FILES_DIR = "../data-collection/raw_files"
CLEANED_FILES_DIR = "./cleaned_files"
SCRIPT_FILES_DIR = "./cleaning_scripts"

# Tạo các thư mục nếu chưa có
os.makedirs(RAW_FILES_DIR, exist_ok=True)
os.makedirs(CLEANED_FILES_DIR, exist_ok=True)

# Hàm lấy danh sách các file dữ liệu thô
def get_file_list():
    files = os.listdir(RAW_FILES_DIR)
    return files

# Hàm lấy danh sách các script làm sạch
def get_cleaning_scripts():
    scripts = [f for f in os.listdir(SCRIPT_FILES_DIR) if f.endswith('.py')]
    return scripts

# Hàm chạy script làm sạch với subprocess
def run_cleaning_script(script_name, raw_file_path):
    try:
        # Gọi subprocess để chạy script với argument là FILE_PATH
        subprocess.run(['python', os.path.join(SCRIPT_FILES_DIR, script_name), raw_file_path], check=True)
        
        # Đọc lại file đã làm sạch sau khi script hoàn tất
        cleaned_file_path = os.path.join(CLEANED_FILES_DIR, f"cleaned_{os.path.basename(raw_file_path)}")
        cleaned_df = pd.read_csv(cleaned_file_path)

        return cleaned_df
    except subprocess.CalledProcessError as e:
        st.error(f"Error running script: {e}")
        return None

# Streamlit App
st.title("Data Cleaning Module")

# Lấy danh sách các file dữ liệu
st.sidebar.header("Select a File and Cleaning Script")
file_list = get_file_list()

# Hiển thị danh sách file để người dùng chọn
if file_list:
    selected_file = st.sidebar.selectbox("Choose a file to clean", file_list)

    # Lấy danh sách các script làm sạch
    script_list = get_cleaning_scripts()
    selected_script = st.sidebar.selectbox("Choose a cleaning script", script_list)

    # Biến để lưu trạng thái xử lý
    cleaning_in_progress = st.sidebar.empty()
    cleaned_data_placeholder = st.empty()

    if st.sidebar.button("Clean Data"):
        raw_file_path = os.path.join(RAW_FILES_DIR, selected_file)

        # Sử dụng ThreadPoolExecutor để thực hiện việc chạy script trong nền
        with concurrent.futures.ThreadPoolExecutor() as executor:
            cleaning_in_progress.text(f"Cleaning file '{selected_file}' using script '{selected_script}'...")
            future = executor.submit(run_cleaning_script, selected_script, raw_file_path)
            cleaned_df = future.result()  # Chờ quá trình làm sạch hoàn tất

            if cleaned_df is not None:
                st.success(f"File '{selected_file}' cleaned successfully.")
                cleaned_data_placeholder.dataframe(cleaned_df)

                # Lưu file đã làm sạch
                #cleaned_file_path = os.path.join(CLEANED_FILES_DIR, f"cleaned_{selected_file}")
                #cleaned_df.to_csv(cleaned_file_path, index=False)
else:
    st.warning("No files available to clean.")


def BACKEND():
    app = Flask(__name__)
    @app.route('/new_file', methods=['GET'])
    def new_file():
        # Trả về dữ liệu dạng JSON
        return jsonify(data.to_dict(orient='records'))

    # Chạy Flask API trong một luồng riêng biệt
    def start_flask():
        app.run(host='0.0.0.0', port=8011)

    # Chạy Flask API trong luồng riêng
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

if __name__=='__main__':
    BACKEND()
