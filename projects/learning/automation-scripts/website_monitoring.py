
#Website Monitoring

import requests

def check_website_status(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Website is up and running!")
    else:
        print("Website is down!")

check_website_status("https://www.phoenixtbird.com")