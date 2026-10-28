
from selenium import webdriver

def automate_browser():
    driver = webdriver.Chrome()
    driver.get("https://example.com")
    login_button = driver.find_element_by_name("login")
    login_button.click()

automate_browser()