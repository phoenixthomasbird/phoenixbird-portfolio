
from PIL import Image
import os

def resize_images(folder_path, new_width):
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            img = Image.open(os.path.join(folder_path, filename))
            width_percent = new_width / float(img.size[0])
            height = int((float(img.size[1]) * width_percent))
            img = img.resize((new_width, height), Image.ANTIALIAS)
            img.save(os.path.join(folder_path, f"resized_{filename}"))

resize_images("path/to/images/", 800)