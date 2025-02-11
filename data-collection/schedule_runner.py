import schedule
import subprocess
import time
import os
from datetime import datetime
import json

# File paths for logs
download_log_file = "downloaded_files.log"
error_log_file = "error_log.log"
performance_log_file = "performance_log.log"
performance_log_file = "performance_log.log"
DATA_SOURCES_FILE = '../data/data_sources.json'
SCRIPT_FILES_DIR = "./collecting_scripts"

# Log file download
def log_download(file_path):
    with open(download_log_file, "a") as f:
        f.write(f"{datetime.now()}: collected a new file at {file_path}\n")

# Log file download error
def log_error(task_name, error_msg):
    with open(error_log_file, "a") as f:
        f.write(f"{datetime.now()} - {task_name} - ERROR: {error_msg}\n")

def log_performance(file_size, time_spent):
    with open(performance_log_file, 'a') as f:
        f.write(f"{file_size},{time_spent}\n")

# Load data sources from JSON configuration
def load_data_sources():
    if os.path.exists(DATA_SOURCES_FILE):
        with open(DATA_SOURCES_FILE, 'r') as f:
            return json.load(f)
    return []

# Task 1: Chạy file T1.py
def run_task(task_name, script_url):
    try:
        start_time = time.time()
        start_time = time.time()
        if script_url.endswith(".py"):
            result = subprocess.run(["python3", script_url], capture_output=True, text=True)
        elif script_url.endswith(".sh"):
            result = subprocess.run(["bash", script_url], capture_output=True, text=True)
        else:
            log_error(task_name, f"Unsupported script type: {script_url}")
            return 0
        if result.returncode == 0:
            print(f"Collect data from {task_name} completed successfully.")
            end_time = time.time()
            end_time = time.time()
            downloaded_files = result.stdout.strip().split("\n")  # Giả sử file được download list trong stdout
            for file in downloaded_files:
                log_download(file)
                log_performance(os.path.getsize(file), end_time-start_time)
        else:
            log_error(task_name, result.stderr)
    except Exception as e:
        log_error(task_name, str(e))

# Task 2: Chạy file T2.sh
def task_2():
    try:
        result = subprocess.run(["bash", "./collecting_scripts/aishub.com.sh"], capture_output=True, text=True)
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
    data_sources = load_data_sources()

    for source in data_sources:
        task_name = source.get("name", "Unnamed Task")
        collecting_script = source.get("collecting_script")
        script_url = SCRIPT_FILES_DIR + '/' + collecting_script
        collecting_frequency = source.get("collecting_frequency")
        schedule_time = source.get("schedule_time", "16:57")

        if not script_url or not collecting_frequency:
            log_error(task_name, "skipped this data source")
            continue

        if collecting_frequency == "Every 20 minutes":
            run_task(task_name, script_url)
            schedule.every(20).minutes.do(run_task, task_name=task_name, script_url=script_url)
        if collecting_frequency == "Hourly":
            schedule.every().hour.at(":59").do(run_task, task_name=task_name, script_url=script_url)
        elif collecting_frequency == "Daily":
            schedule.every().day.at(schedule_time).do(run_task, task_name=task_name, script_url=script_url)
        elif collecting_frequency == "Weekly":
            schedule.every().week.at(schedule_time).do(run_task, task_name=task_name, script_url=script_url)
        
    
    #schedule.every().hour.at(":49").do(task_2)  # Chạy Task 2 vào 20 phút
    #schedule.every().hour.at(":40").do(task_3)  # Chạy Task 3 vào 40 phút

def start_schedule():
    schedule_tasks()

    while True:
        schedule.run_pending()
        time.sleep(1)
        

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


