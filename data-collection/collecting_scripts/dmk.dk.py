import os
from os import listdir, getcwd
from os.path import isfile, join, isdir
import requests
from datetime import datetime
import zipfile
from bs4 import BeautifulSoup
import re

# Base URL of the data repository
BASE_URL = "http://web.ais.dk/aisdata/"

# Directory to save downloaded files
DOWNLOAD_DIR = "./data/DMA.dk"

FILE_NAME_PATTERN = r"aisdk-(\d{4})-(\d{2})-(\d{2}).zip"

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Define the year and month for the download
year = 2024
month = 7 


def parse_file_name(file_name):
    # Search for the pattern in the URL
    match = re.search(FILE_NAME_PATTERN, file_name)

    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return int(year), int(month), int(day)
    return 0,0,0

# Get list of files on URL
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

# Get list of new files locally
def get_ais_new_file_list(url):
    current_files = get_ais_file_list(url)
    previous_files = [BASE_URL + e for e in listdir('./')]
    new_files = list(set(current_files) - set(previous_files))  # Find new files

    if new_files:
        print(new_files)
        download_files(new_files)
    else:
        print("COLLECTOR: No new files found.")
    return new_files

def download_files(file_urls):
    for file_url in file_urls:
        try:
            file_name = file_url.split("/")[-1]
            
            local_file_path = os.path.join(DOWNLOAD_DIR, f"{file_name}")

            if not os.path.exists(local_file_path):
                # Make the HTTP request to download the file
                print(f"Download {file_url} ...")
                response = requests.get(file_url, stream=True)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Write the downloaded content to a .zip file
                    with open(local_file_path, 'wb') as zip_file:
                        zip_file.write(response.content)
                    # Saved zip file to {local_file_path}
                    
                    """
                    # Extract the .zip file
                    print(f"Extracting {local_file_path} ...")
                    with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
                        zip_ref.extractall(DOWNLOAD_DIR)
                    print(f"Extracted to {DOWNLOAD_DIR}")
                    """
                else:
                    print(f"[COLLECTOR] Download failed: {file_url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading data for {date_str}: {str(e)}")

if __name__ == "__main__":
    get_ais_new_file_list(BASE_URL)

