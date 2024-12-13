import streamlit as st
import pandas as pd
import numpy as np
import os

# Giả lập các dữ liệu ban đầu
data_collection_status = {"sources": [], "status": []}
cleaned_data = None
stored_data = {}

# Sidebar để chọn bước trong lifecycle
st.sidebar.title("Data Lifecycle Management")
lifecycle_step = st.sidebar.radio("Select Step", ("Data Collection", "Data Cleaning", "Data Storage", "Data Presentation"))

# Hàm để hiển thị các bước của từng giai đoạn trong lifecycle

# 1. Data Collection
if lifecycle_step == "Data Collection":
    st.title("Data Collection")
    
    # Cho phép thêm nguồn dữ liệu
    st.subheader("Add a Data Source")
    data_name = st.text_input("Data Source Name")
    data_url = st.text_input("Data Source URL (or Path)")
    
    if st.button("Add Source"):
        data_collection_status["sources"].append({"name": data_name, "url": data_url})
        data_collection_status["status"].append("Pending")
        st.success(f"Source '{data_name}' added successfully.")
    
    # Hiển thị các nguồn dữ liệu hiện tại
    st.subheader("Current Data Sources")
    if len(data_collection_status["sources"]) > 0:
        for i, source in enumerate(data_collection_status["sources"]):
            st.write(f"{i+1}. {source['name']} ({source['url']}) - Status: {data_collection_status['status'][i]}")
    else:
        st.write("No data sources added yet.")

    # Button để bắt đầu thu thập dữ liệu
    if st.button("Start Collection"):
        # Giả lập quá trình thu thập dữ liệu
        for i in range(len(data_collection_status["sources"])):
            data_collection_status["status"][i] = "Collected"
        st.success("Data collection completed.")

# 2. Data Cleaning
elif lifecycle_step == "Data Cleaning":
    st.title("Data Cleaning")
    
    # Giả lập dữ liệu từ quá trình thu thập
    raw_data = pd.DataFrame({
        "Name": ["John", "Jane", "Jim", "Jake", None],
        "Age": [28, 34, None, 45, 38],
        "Gender": ["Male", "Female", "Male", None, "Female"]
    })

    st.subheader("Raw Data")
    st.write(raw_data)
    
    # Cho phép người dùng chọn các bước làm sạch dữ liệu
    st.subheader("Data Cleaning Options")
    remove_nulls = st.checkbox("Remove Null Values")
    remove_duplicates = st.checkbox("Remove Duplicates")
    
    if st.button("Clean Data"):
        cleaned_data = raw_data.copy()
        
        if remove_nulls:
            cleaned_data = cleaned_data.dropna()
        if remove_duplicates:
            cleaned_data = cleaned_data.drop_duplicates()
        
        st.write("Cleaned Data:")
        st.write(cleaned_data)

# 3. Data Storage
elif lifecycle_step == "Data Storage":
    st.title("Data Storage")
    
    if cleaned_data is not None:
        st.subheader("Cleaned Data Ready for Storage")
        st.write(cleaned_data)
        
        storage_option = st.selectbox("Select Storage Option", ["Local File System", "SQLite Database"])
        
        if st.button("Store Data"):
            if storage_option == "Local File System":
                cleaned_data.to_csv("cleaned_data.csv", index=False)
                stored_data["cleaned_data.csv"] = "Local File System"
                st.success("Data stored in 'cleaned_data.csv'")
            elif storage_option == "SQLite Database":
                import sqlite3
                conn = sqlite3.connect('data.db')
                cleaned_data.to_sql('cleaned_data', conn, if_exists='replace', index=False)
                stored_data['cleaned_data'] = "SQLite Database"
                st.success("Data stored in SQLite database")
    else:
        st.warning("No data available for storage. Please clean data first.")

# 4. Data Presentation
elif lifecycle_step == "Data Presentation":
    st.title("Data Presentation")
    
    st.subheader("Stored Data")
    if len(stored_data) > 0:
        for data_name, location in stored_data.items():
            st.write(f"{data_name} - Stored in: {location}")
        
        # Giả lập việc đọc dữ liệu đã lưu
        data_to_present = pd.read_csv("cleaned_data.csv")
        st.write("Data Preview:")
        st.write(data_to_present)
        
        # Hiển thị dữ liệu dưới dạng biểu đồ
        st.subheader("Data Visualization")
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot"])
        x_axis = st.selectbox("Select X-axis", data_to_present.columns)
        y_axis = st.selectbox("Select Y-axis", data_to_present.columns)
        
        if st.button("Generate Chart"):
            if chart_type == "Bar Chart":
                st.bar_chart(data_to_present[[x_axis, y_axis]].set_index(x_axis))
            elif chart_type == "Line Chart":
                st.line_chart(data_to_present[[x_axis, y_axis]].set_index(x_axis))
            elif chart_type == "Scatter Plot":
                st.scatter_chart(data_to_present[[x_axis, y_axis]])
    else:
        st.warning("No stored data available.")
