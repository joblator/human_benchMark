import mss
import cv2
import pyautogui
import numpy as np
import time
import keyboard
click_color = (106,219,75)
monitor = {"top":409,"left":322,"width":1,"height":1}
time.sleep(5)
with mss.mss() as sct:
    while True:
        img = np.array(sct.grab(monitor))[:,:, :3]
        tolerance = 10
        mask = np.all(np.abs(img - click_color) <= tolerance, axis=2)
        if np.any(mask):
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.click()
        if keyboard.is_pressed('q'):  # Press 'q' to quit
            break
quit()