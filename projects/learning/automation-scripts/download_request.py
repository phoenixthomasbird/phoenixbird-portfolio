import requests

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"File {filename} downloaded successfully.")

download_file("https://sample.com/file.zip", "file.zip")

