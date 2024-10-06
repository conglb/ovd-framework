from flask import Flask, jsonify
import threading

DATA_SOURCES_FILE = '../data/data_sources.json'

def BACKEND():
    app = Flask(__name__)
    @app.route('/new_file', methods=['GET'])
    def new_file():
        # Trả về dữ liệu dạng JSON
        return jsonify(data.to_dict(orient='records'))
    
    @app.route('/data_sources', methods=['GET'])
    def get_data_sources():
        # Trả về dữ liệu dạng JSON
        return jsonify(data.to_dict(orient='records'))

    # Chạy Flask API trong một luồng riêng biệt
    def start_flask():
        app.run(host='0.0.0.0', port=8881)

    # Chạy Flask API trong luồng riêng
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()