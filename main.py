import os
import requests
from datetime import datetime

API_KEY = ''#                                                    <- API Key
BASE_URL = 'http://<ip>:2283/api'#                               <- Immich URL

UPLOAD_FOLDERS = [
    r'C:\Users\user\Pictures\Screenshots',#                      <- Folder Locations
    #r'C:\Users\user\some\folder',
]

UPLOADED_LIST_FILE = 'files.txt'

def load_uploaded():
    uploaded = {}
    if os.path.exists(UPLOADED_LIST_FILE):
        with open(UPLOADED_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                path, mtime = line.strip().split('|')
                uploaded[path] = float(mtime)
    return uploaded

def save_uploaded(uploaded):
    with open(UPLOADED_LIST_FILE, 'w', encoding='utf-8') as f:
        for path, mtime in uploaded.items():
            f.write(f'{path}|{mtime}\n')

def upload(file):
    stats = os.stat(file)
    headers = {
        'Accept': 'application/json',
        'x-api-key': API_KEY
    }
    data = {
        'deviceAssetId': f'{file}-{stats.st_mtime}',
        'deviceId': 'python-autoupload',
        'fileCreatedAt': datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'fileModifiedAt': datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'isFavorite': 'false',
    }
    files = {
        'assetData': open(file, 'rb')
    }
    try:
        response = requests.post(f'{BASE_URL}/assets', headers=headers, data=data, files=files)
        response.raise_for_status()
        json_response = response.json()
        return True, json_response
    except Exception as e:
        print(f"Error uploading {file}: {e}")
        return False, None
    finally:
        files['assetData'].close()

def find_images(folders):
    image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.gif', '.bmp', '.webp', '.mp4']
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            for name in files:
                if any(name.lower().endswith(ext) for ext in image_extensions):
                    yield os.path.join(root, name)

def main():
    uploaded = load_uploaded()
    all_images = list(find_images(UPLOAD_FOLDERS))
    to_upload = []
    for image_file in all_images:
        stats = os.stat(image_file)
        mtime = stats.st_mtime
        if image_file not in uploaded or uploaded[image_file] < mtime:
            to_upload.append(image_file)

    total = len(to_upload)
    if total == 0:
        print("No new or modified images found to upload.")
        return
    print(f"Start upload of {total} new/updated images...")
    for idx, image_file in enumerate(to_upload, start=1):
        success, resp = upload(image_file)
        if success:
            uploaded[image_file] = os.stat(image_file).st_mtime

        print(f"[{idx}/{total}] {os.path.basename(image_file)} uploaded.")

    save_uploaded(uploaded)
    print("Upload completed.")

if __name__ == '__main__':
    main()
