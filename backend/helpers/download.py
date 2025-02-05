import requests
from fastapi import HTTPException

def download_file(url: str, filename: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename
    else:
        raise HTTPException(status_code=404, detail=f"Failed to download {url}. Status code: {response.status_code}")