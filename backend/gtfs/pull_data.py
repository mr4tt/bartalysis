import requests
import zipfile
import os

def download_and_unzip(url, target_directory):
    # Temporary file path
    temp_zip_path = "temp.zip"
    
    # Download the file
    with requests.get(url, allow_redirects=True, stream=True) as r:
        r.raise_for_status()
        with open(temp_zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    
    # Unzip the file
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_directory)
    
    # Clean up: Remove the temporary file
    os.remove(temp_zip_path)

url = "https://www.bart.gov/dev/schedules/google_transit.zip"
target_directory = "/workspaces/bartalysis/backend/gtfs/data/"
download_and_unzip(url, target_directory)