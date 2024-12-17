import os
from os.path import join, isdir


# Thư mục lưu file chưa làm sạch và đã làm sạch
RAW_FILES_DIR = "../data/raw_files/"
CLEANED_FILES_DIR = "../data/cleaned_files/"
SCRIPT_FILES_DIR = "./cleaning_scripts/"

# Tạo các thư mục nếu chưa có
os.makedirs(CLEANED_FILES_DIR, exist_ok=True)

# Hàm lấy danh sách các file dữ liệu thô
def get_file_list(path):
    files = [x for x in os.listdir(path) if x.endswith('.csv')]
    return files

def get_folder_list(path):
    folders = [x for x in os.listdir(path) if isdir(join(path,x))]
    return folders

# Hàm lấy danh sách các script làm sạch
def get_cleaning_scripts():
    scripts = [f for f in os.listdir(SCRIPT_FILES_DIR) if f.endswith('.py')]
    return scripts

# Function to list all files and sub-files in a directory
def list_files_in_directory(directory):
    file_structure = {}
    for root, dirs, files in os.walk(directory):
        folder_name = os.path.relpath(root, directory)
        file_structure[folder_name] = files + dirs
    return file_structure