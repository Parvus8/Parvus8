import re
import sys
import requests
import random
from bs4 import BeautifulSoup

def fetch_random_image_url(base_url):
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {response.status_code}")
        sys.exit(1)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

    if not img_urls:
        print("No images found on the page.")
        sys.exit(1)
    
    random_img_url = random.choice(img_urls)
    return random_img_url

def update_image(readme_path, old_image_url, new_image_url):
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()

    updated_content = re.sub(re.escape(old_image_url), new_image_url, content)

    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_image.py <README.md> <old_image_url> <base_url>")
        sys.exit(1)

    readme_path = sys.argv[1]
    old_image_url = sys.argv[2]
    base_url = sys.argv[3]

    new_image_url = fetch_random_image_url(base_url)
    update_image(readme_path, old_image_url, new_image_url)
    print("Image URL updated successfully!")
