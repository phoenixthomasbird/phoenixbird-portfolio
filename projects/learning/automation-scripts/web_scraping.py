
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for title in soup.find_all('h3'):
        print(title.get_text())

scrape_website("https://phoenixtbird.com")