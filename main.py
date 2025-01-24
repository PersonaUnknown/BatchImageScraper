import os, os.path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# From: https://blog.apify.com/save-image-python/
def download_image(image_url, file_dir):
    response = requests.get(image_url)

    if response.status_code == 200:
        directory = os.path.dirname(file_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_dir, "wb") as fp:
            fp.write(response.content)
        print("Image downloaded successfully.")
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

queries = []
licenses = [
    "Any",                # All Creative Commons
    "Public",             # Public Domain
    "Share",              # Free to Share and Use
    "ShareCommercially",  # Free to Share and Use Commercially
    "Modify",             # Free to Modify, Share, and Use
    "ModifyCommercially"  # Free to Modify, Share, and Use Commercially
]
option = 3
license = licenses[option]

with open('queries.txt', mode='r') as file:
    lines = file.readlines()
    for line in lines:
        queries.append(line)
driver = webdriver.Chrome()

for query in queries:
    # Query DuckDuckGo
    url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images&iaf=license%3A{license}"
    driver.get(url)
    for x in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    elems = driver.find_elements(By.CLASS_NAME, 'tile--img__img')
    images = []
    for elem in elems:
        src = elem.get_attribute("src")
        if src:
            images.append(src)
    driver.close()
    # Save images
    print(f"Saving images for \"{query}\"")
    dir = f"./output/{query}"
    if not os.path.exists(dir):
        os.mkdir(dir)
    for i, img in enumerate(images):
        path = f"{dir}/image{i}.png"
        download_image(img, path)
    
driver.quit()