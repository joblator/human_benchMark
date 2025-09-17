from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pyautogui
import keyboard
import time
import numpy as np
import cv2
import mss
def detect_target():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        screenshot_np = np.array(img)
        img = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
                # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur (to reduce noise)
        blurred = cv2.GaussianBlur(gray, (5,5), 0)

        # Use Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by circularity and area
        detected_circles = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * (area / (perimeter * perimeter))
            
            # Adjust these parameters based on your circle size and shape
            if area > 10000 and circularity > 0.7:
                detected_circles.append(cnt)
        
        # Draw detected circles on the original image
        output = img.copy()
        for circle in detected_circles:
            (x, y), radius = cv2.minEnclosingCircle(circle)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(output, center, radius, (0, 255, 0), 2)
            cv2.circle(output, center, 2, (0, 0, 255), 3)
            return True,int(x),int(y),int(radius), output
        
        
        
        return False,-1,-1,-1,output

def find_target(driver):
    src = driver.page_source
    soup = BeautifulSoup(src,"html.parser")
    div = soup.find("div",class_= "css-7173fr")
    target_div = div.select_one('div[style*="matrix3d"]')
    style = target_div.get('style', '')
    matrix = style.split("matrix3d")[1]
    matrix_list = []
    add_text = ""
    for index in range(len(matrix)-2):
        if 47 < ord(matrix[index]) < 58 and 47 < ord(matrix[index + 1]) < 58:
            add_text += matrix[index]
        elif 47 < ord(matrix[index]) < 58 and (48 > ord(matrix[index + 1]) or  ord(matrix[index + 1]) > 57):
            add_text += matrix[index]
            matrix_list.append(int(add_text))
            add_text = ''
    print(matrix)
    print(matrix_list)
    return matrix_list
def click_target(matrix_list):
    pyautogui.click(matrix_list[12],matrix_list[13])
def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://humanbenchmark.com/tests/aim")
    while keyboard.is_pressed("tab") == False:
        pass
    for i in range(31):
        found,x,y,rad,img = detect_target()
        while not found:
            found,x,y,rad,img = detect_target()
        pyautogui.click(x,y)
        print(f"pressed at {x,y}")
    

main()
