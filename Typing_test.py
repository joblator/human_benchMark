from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time
def get_text_to_write(driver):
    src = driver.page_source
    soup = BeautifulSoup(src,"html.parser")
    div = soup.find("div",class_= "letters notranslate")
    span  =div.find_all("span")
    text = ""
    index = 0
    for letter in span:
        text += letter.text
    return text
def write_text(text):
    pyautogui.write(text,)

def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://humanbenchmark.com/tests/typing")
    while  False == keyboard.is_pressed("tab"):
        pass
    write_text( get_text_to_write(driver))
    while True:
        time.sleep(1)

main()






