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
    
    @app.route('/data_sources', methods=['GET'])
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

# Giao diện Streamlit chính
def FRONTEND():
    st.title("Data Collection Module")

    
if __name__ == '__main__':

    FRONTEND()

    if not hasattr(st, 'already_started_server'):
        st.already_started_server = True
        BACKEND()