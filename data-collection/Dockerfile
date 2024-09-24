FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các file trong thư mục hiện tại vào container
#COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir streamlit pandas requests flask

# Expose cổng 8501 cho Streamlit
EXPOSE 5011
EXPOSE 8511

# Chạy Streamlit
CMD ["streamlit", "run", "app_management.py", "--server.port=8511"]