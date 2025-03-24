import os
from os import listdir, getcwd
from os.path import isfile, join, isdir
import requests
from datetime import datetime
import zipfile
from bs4 import BeautifulSoup
import re
import sys

def parse_file_name(file_name):
    FILE_NAME_PATTERN = r"aisdk-(\d{4})-(\d{2})-(\d{2}).zip"
    match = re.search(FILE_NAME_PATTERN, file_name)

    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return int(year), int(month), int(day)
    return 0,0,0

def get_ais_file_list(url, in_year=2024, in_month=7):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    file_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        year, month, day = parse_file_name(href)
        if href.endswith('.zip') and year==in_year and month==in_month:  
            file_links.append(url + href)  
            
    return file_links

def download_files(file_urls, save_dir_path):
    for file_url in file_urls:
        file_name = file_url.split("/")[-1]
        
        local_file_path = os.path.join(save_dir_path, f"{file_name}")

        if not os.path.exists(local_file_path):
            response = requests.get(file_url, stream=True)

            if response.status_code == 200:
                with open(local_file_path, 'wb') as zip_file:
                    zip_file.write(response.content)
  

def collect(url, save_dir_path):
    print("collect in template.py")
    new_files = get_ais_file_list(url, in_year=2025, in_month=2)
    download_files(new_files, save_dir_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py save_dir_path")
    else:
        save_dir_path = sys.argv[1]
        collect("http://web.ais.dk/aisdata/", save_dir_path)