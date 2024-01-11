import pyautogui
import time
import keyboard
import subprocess

# subprocess.call(["xhost", "+SI:localuser:root"])

# Define a flag to control the loop
running = False

def start_loop(e):
    global running
    running = True

def stop_loop(e):
    global running
    running = False

# Bind the 'w' key to start the loop
keyboard.on_press_key('F6', start_loop)

# Bind the 'q' key to stop the loop
keyboard.on_press_key('q', stop_loop)


while True:
    if running:
        pyautogui.press('backspace')  # press 'backspace' first
        pyautogui.typewrite('/beg')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
#        pyautogui.typewrite('/crime')
#        time.sleep(2)
#        pyautogui.press('enter')
#        time.sleep(2)
#        pyautogui.press('enter')
#        time.sleep(2)
#        pyautogui.click(x=114, y=658)
#        time.sleep(2)
        pyautogui.typewrite('/dig')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.typewrite('/highlow')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.click(x=114, y=658)
#        time.sleep(2)
#        pyautogui.typewrite('/hunt')
#        time.sleep(2)
#        pyautogui.press('enter')
#        time.sleep(2)
#        pyautogui.press('enter')
#        time.sleep(2)
#        pyautogui.typewrite('/search')
#        time.sleep(2)
#        pyautogui.press('enter')
#        time.sleep(2)
#        pyautogui.press('enter')
#
#        time.sleep(2)
#        pyautogui.click(x=114, y=658)
        time.sleep(30)



