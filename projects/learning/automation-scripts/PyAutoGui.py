
import pyautogui
import time

#FailSafe is True by default, set here for clarity
pyautogui.FAILSAFE = True

#Add a 2-second pause after each pyautogui command
pyautogui.PAUSE = True

pyautogui.write("Hello, world")

