import requests
from bs4 import BeautifulSoup
import os

class PinterestScrapper():

    def __init__(self, table_url):

        self.save_directory = "./dataScrappedFromSocialMedia/Pictures"
        os.makedirs(self.save_directory, exist_ok=True)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
        }
        self.table_url = table_url
        self.scrap_pinterest()

    def scrap_pinterest(self):
        response = requests.get(self.table_url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            images = soup.find_all("img")

            # Loop through each image and save it
            for idx, img in enumerate(images):
                try:
                    img_url = img["src"]  # Get the image URL
                    if img_url:
                        # Download the image
                        img_data = requests.get(img_url).content
                        img_filename = os.path.join(self.save_directory, f"pinterest_image_{idx}.jpg")
                        # Save the image
                        with open(img_filename, "wb") as file:
                            file.write(img_data)
                        print(f"Saved image {idx + 1}")
                except Exception as e:
                    print(f"Could not save image {idx + 1}: {e}")
        else:
            print(f"Failed to retrieve Pinterest board. Status code: {response.status_code}")
