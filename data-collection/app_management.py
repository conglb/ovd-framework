import streamlit as st
import pandas as pd
import json
import os
from flask import Flask
import threading

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


# Đường dẫn lưu trữ các nguồn dữ liệu
DATA_SOURCES_FILE = 'data_sources.json'

# Load các nguồn dữ liệu từ file JSON
def load_data_sources():
    if os.path.exists(DATA_SOURCES_FILE):
        with open(DATA_SOURCES_FILE, 'r') as f:
            return json.load(f)
    return []

# Lưu các nguồn dữ liệu vào file JSON
def save_data_sources(data_sources):
    with open(DATA_SOURCES_FILE, 'w') as f:
        json.dump(data_sources, f, indent=4)

# Thêm một nguồn dữ liệu mới
def add_data_source(name, url, description):
    data_sources = load_data_sources()
    data_sources.append({
        "name": name,
        "url": url,
        "description": description
    })
    save_data_sources(data_sources)

# Xóa một nguồn dữ liệu
def delete_data_source(index):
    data_sources = load_data_sources()
    if 0 <= index < len(data_sources):
        del data_sources[index]
    save_data_sources(data_sources)

# Chỉnh sửa nguồn dữ liệu
def edit_data_source(index, name, url, description):
    data_sources = load_data_sources()
    if 0 <= index < len(data_sources):
        data_sources[index] = {
            "name": name,
            "url": url,
            "description": description
        }
    save_data_sources(data_sources)

# Giao diện Streamlit chính
def FRONTEND():
    st.title("Data Collection Management")
    
    # Lựa chọn hiển thị thêm nguồn dữ liệu hoặc quản lý
    menu = ["Add Data Source", "Manage Data Sources"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Data Source":
        st.subheader("Add a New Data Source")

        # Nhập thông tin nguồn dữ liệu
        name = st.text_input("Source Name")
        url = st.text_input("Source URL")
        description = st.text_area("Source Description")

        # Thêm nguồn dữ liệu vào file JSON khi người dùng nhấn nút
        if st.button("Add Source"):
            if name and url:
                add_data_source(name, url, description)
                st.success(f"Source '{name}' has been added successfully!")
            else:
                st.error("Please enter both a name and URL for the data source.")
    
    elif choice == "Manage Data Sources":
        st.subheader("Manage Data Sources")
        
        # Load danh sách các nguồn dữ liệu
        data_sources = load_data_sources()
        if len(data_sources) == 0:
            st.warning("No data sources available.")
        else:
            # Hiển thị danh sách các nguồn dữ liệu dưới dạng bảng
            df = pd.DataFrame(data_sources)
            st.dataframe(df)

            # Xóa nguồn dữ liệu
            st.write("### Delete or Edit a Data Source")
            index_to_delete = st.number_input("Select the index of the source to delete", min_value=0, max_value=len(data_sources) - 1, step=1)

            if st.button("Delete Source"):
                delete_data_source(index_to_delete)
                st.success("Data source deleted.")
                st.experimental_rerun()

            # Chỉnh sửa nguồn dữ liệu
            st.write("### Edit a Data Source")
            index_to_edit = st.number_input("Select the index of the source to edit", min_value=0, max_value=len(data_sources) - 1, step=1)
            
            if st.checkbox("Edit this source"):
                edited_name = st.text_input("Edit Name", value=data_sources[index_to_edit]["name"])
                edited_url = st.text_input("Edit URL", value=data_sources[index_to_edit]["url"])
                edited_description = st.text_area("Edit Description", value=data_sources[index_to_edit]["description"])

                if st.button("Save Changes"):
                    edit_data_source(index_to_edit, edited_name, edited_url, edited_description)
                    st.success("Data source updated.")
                    st.experimental_rerun()

if __name__ == '__main__':

    FRONTEND()

    if not hasattr(st, 'already_started_server'):
        st.already_started_server = True
        BACKEND()