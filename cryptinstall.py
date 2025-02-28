from googleapiclient.discovery import build
import urllib.request
import os
import re

API_KEY = 'ENTER YOUR API_KEY FOR GOOGLE API CLIENT HERE'
FOLDER_ID = '1ElVOO_4Plr24xEOmdqsINmIRM_y4M3_n'

# Function to download a file
def download_file(url, folder_path, default_name):
    
    file_path = os.path.join(folder_path, default_name)

    if os.path.exists(file_path):
        print(f"File '{default_name}' already exists, skipping download.")
        return
    try:
        # Send a request to fetch the file
        response = urllib.request.urlopen(url)

        # Attempt to determine the file name from the Content-Disposition header
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            # Extract the filename from the header
            file_name_match = re.findall('filename="(.+)"', content_disposition)
            if file_name_match:
                file_name = file_name_match[0]
            else:
                file_name = default_name
        else:
            # Fallback to default name
            file_name = default_name

        file_path = os.path.join(folder_path, file_name)

        # Write the content to the file
        with open(file_name, 'wb') as file:
            file.write(response.read())

        print(f"File downloaded successfully as '{file_name}'!")
    except Exception as e:
        print(f"Failed to download '{default_name}': {e}")

def main():    
    # Folder where files are installed
    folder_path = '.crypt_files'

    # Build the service
    service = build('drive', 'v3', developerKey=API_KEY)

    # Query to list files in the folder
    query = f"'{FOLDER_ID}' in parents and trashed=false"

    # List files
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=query,
            fields='nextPageToken, files(id, name)',
            pageSize=1000,
            pageToken=page_token
        ).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
        
    # Download each file
    for file in files:
        file_id = file['id']
        file_name = file['name']

        file_path = os.path.join(folder_path, file_name)

        # Check if file already exists
        if os.path.exists(file_path):
            print(f"File '{file_name}' already exists, skipping download.")
            continue

        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        # Call the download function
        download_file(download_url, folder_path, file_name)