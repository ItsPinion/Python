from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController, Key
from datetime import datetime
import time

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

def replay_events():
    with open("macro.txt", "r") as file:
        previous_timestamp = None
        for line in file:
            event = line.strip().split(": ")
            if len(event) == 2:
                timestamp, action = event
                current_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S,%f")
                if previous_timestamp is not None:
                    time_difference = (current_timestamp - previous_timestamp).total_seconds()
                    time.sleep(time_difference)  # Wait for the time difference between events

                if action.startswith("Mouse moved"):
                    _, x, y = action.split(" ")[3:]
                    x = int(x[1:-1])
                    y = int(y[:-1])
                    mouse_controller.position = (x, y)  # Move the mouse to the specified position

                elif action.startswith("Mouse clicked"):
                    _, *args = action.split(" ")
                    if len(args) >= 4:
                        x, y, button = args[3:6]
                        x = int(x[1:-1])
                        y = int(y[:-1])
                        button = button[5:-1]
                        mouse_controller.position = (x, y)  # Move the mouse to the specified position
                        mouse_controller.press(button)  # Press the mouse button
                        mouse_controller.release(button)  # Release the mouse button

                elif action.startswith("Mouse scrolled"):
                    _, x, y, dx, dy = action.split(" ")
                    x = int(x[1:-1])
                    y = int(y[:-1])
                    dx = int(dx[1:-1])
                    dy = int(dy[:-1])
                    mouse_controller.position = (x, y)  # Move the mouse to the specified position
                    mouse_controller.scroll(dx, dy)  # Scroll the mouse

                elif action.startswith("Key pressed"):
                    _, key = action.split(": ")
                    key = key[1:-1]
                    if key == "Key.esc":
                        break  # Stop replaying if the 'Esc' key is encountered
                    keyboard_controller.press(eval(key))  # Press the keyboard key

                elif action.startswith("Key released"):
                    _, key = action.split(": ")
                    key = key[1:-1]
                    keyboard_controller.release(eval(key))  # Release the keyboard key

                previous_timestamp = current_timestamp

replay_events()

