#Download Images from URLs

import requests
def download_image(url, file_name):
    img_data = requests.get(url).content
    with open(file_name, 'wb') as handler:
        handler.write(img_data)
    print("Image downloaded successfully.")

download_image("https://www.example.com/image.jpg", "downloaded_image.jpg")

