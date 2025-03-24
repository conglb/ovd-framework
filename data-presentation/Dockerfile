FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# Expose cổng 8501 cho Streamlit
EXPOSE 8014
EXPOSE 8514

# Chạy Streamlit
CMD ["streamlit", "run", "Module_Management.py", "--server.port=8514"]