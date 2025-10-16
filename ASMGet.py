"""
Author: Rory Cameron
Date: 16/10/2025
Description: Gets URIs from Google ASM
"""

import os
from dotenv import load_dotenv
import requests
from time import sleep


load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
PROJECT_ID = os.getenv("PROJECT_ID") #Note: If >1 projects, implement GET request for /asm/projects, then iterate over each project with type:Uri


headers = {
    "accept": "application/json",
    "x-apikey": API_KEY,
    "PROJECT-ID": PROJECT_ID
}


# Get entity URI's

# Create URL
path = "search/entities/"
search_string = "type:Uri"
url = BASE_URL + path + search_string


all_uris = []
next_page = None


while True: # Checks if next_page_token exists, if so moves onto next page

    params = {"page_size": 100} # 100 entities per page

    if next_page:
        params["page_token"] = next_page

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200: # If Success
        data = response.json()
        uris = [entity.get("attributes", {}).get("name") for entity in data.get("data", [])]
        all_uris.extend([u for u in uris if u]) # Filters out none values

        print(f"[SUCCESS] Retrieved {len(data.get('data',[]))} URI's")

        next_page = data.get("meta", {}).get("next_page_token")
        if not next_page:
            break
    
        sleep(0.5)

    else:
        print(f"[ERROR] {response.status_code}: {response.text}")
        break


# Print URI's
for uri in all_uris:
    print(uri)

print(f"[SUCCESS] Retrieved {len(all_uris)} URI's")