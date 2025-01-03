from os.path import join, isdir
import os

SCRIPT_FILES_DIR = "./storing_scripts"


def get_file_list(path):
    files = [x for x in os.listdir(path) if x.endswith('.csv')]
    return files

def get_folder_list(path):
    folders = [x for x in os.listdir(path) if isdir(join(path,x))]
    return folders

def get_storing_scripts():
    scripts = [f for f in os.listdir(SCRIPT_FILES_DIR) if f.endswith('.py')]
    return scripts