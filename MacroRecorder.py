from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, Key
import logging

logging.basicConfig(filename="macro.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

mouse_controller = MouseController()

def on_move(x, y):
    logging.info("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

def on_press(key):
    logging.info('Key pressed: {0}'.format(key))
    if key == Key.esc:  # Stop listener
        mouse_listener.stop()  # Stop mouse listener
        keyboard_listener.stop()  # Stop keyboard listener

def on_release(key):
    logging.info('Key released: {0}'.format(key))

with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, KeyboardListener(on_press=on_press, on_release=on_release) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()

