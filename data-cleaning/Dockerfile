FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các file trong thư mục hiện tại vào container

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir streamlit pandas requests flask streamlit_monaco plotly

# Expose cổng 8501 cho Streamlit
EXPOSE 8012
EXPOSE 8512

# Chạy Streamlit
CMD ["streamlit", "run", "Module_Management.py", "--server.port=8512"]