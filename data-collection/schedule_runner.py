import schedule
import subprocess
import time
import os
from datetime import datetime

# Đường dẫn tới các file download và logs
download_log_file = "downloaded_files.log"
error_log_file = "error_log.log"

# Hàm ghi log file download
def log_download(file_path):
    with open(download_log_file, "a") as f:
        f.write(f"{datetime.now()}: {file_path}\n")

# Hàm ghi log lỗi
def log_error(task_name, error_msg):
    with open(error_log_file, "a") as f:
        f.write(f"{datetime.now()} - {task_name} - ERROR: {error_msg}\n")

# Task 1: Chạy file T1.py
def task_1():
    try:
        result = subprocess.run(["python3", "T1.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Task 1 completed successfully.")
            downloaded_files = result.stdout.strip().split("\n")  # Giả sử file được download list trong stdout
            for file in downloaded_files:
                log_download(file)
        else:
            log_error("Task 1", result.stderr)
    except Exception as e:
        log_error("Task 1", str(e))

# Task 2: Chạy file T2.sh
def task_2():
    try:
        result = subprocess.run(["bash", "./runner/aishub.com.sh"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Task 2 completed successfully.")
            downloaded_files = result.stdout.strip().split("\n")  # Giả sử file được download list trong stdout
            for file in downloaded_files:
                log_download(file)
        else:
            log_error("Task 2", result.stderr)
    except Exception as e:
        log_error("Task 2", str(e))

# Task 3: Chạy file T3.py
def task_3():
    try:
        result = subprocess.run(["python3", "T3.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Task 3 completed successfully.")
            downloaded_files = result.stdout.strip().split("\n")  # Giả sử file được download list trong stdout
            for file in downloaded_files:
                log_download(file)
        else:
            log_error("Task 3", result.stderr)
    except Exception as e:
        log_error("Task 3", str(e))

# Lên lịch các tasks tuần tự
def schedule_tasks():
    print("Scheduling tasks...")
    #schedule.every().hour.at(":00").do(task_1)  # Chạy Task 1 đầu giờ
    schedule.every().hour.at(":18").do(task_2)  # Chạy Task 2 vào 20 phút
    #schedule.every().hour.at(":40").do(task_3)  # Chạy Task 3 vào 40 phút

# Vòng lặp chính để chạy tasks tuần tự
if __name__ == "__main__":
    # Tạo file log nếu chưa có
    if not os.path.exists(download_log_file):
        with open(download_log_file, "w") as f:
            f.write("Download log:\n")
    if not os.path.exists(error_log_file):
        with open(error_log_file, "w") as f:
            f.write("Error log:\n")
    
    # Lên lịch và chạy tasks
    schedule_tasks()

    while True:
        schedule.run_pending()
        time.sleep(1)
