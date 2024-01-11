from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, Key

class Macro:
    def __init__(self, events):
        self.events = events
        self.current_event = 0

    def play(self):
        for event in self.events:
            if event.type == "mouse_move":
                mouse_controller.position = event.position
            elif event.type == "mouse_click":
                mouse_controller.click(event.button, event.position)
            elif event.type == "key_press":
                keyboard_controller.press(event.key)
            elif event.type == "key_release":
                keyboard_controller.release(event.key)

            time.sleep(event.duration)

    def record(self):
        def on_mouse_move(x, y):
            self.events.append(Event("mouse_move", (x, y), 0))

        def on_mouse_click(x, y, button, pressed):
            if pressed:
                self.events.append(Event("mouse_click", button, (x, y), 0))

        def on_key_press(key):
            self.events.append(Event("key_press", key, 0))

        def on_key_release(key):
            self.events.append(Event("key_release", key, 0))

        with MouseListener(on_move=on_mouse_move, on_click=on_mouse_click) as mouse_listener, KeyboardListener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()

class Event:
    def __init__(self, type, value, position=None, duration=0):
        self.type = type
        self.value = value
        self.position = position
        self.duration = duration

# Example usage:

macro = Macro([])

# Record a macro.
macro.record()

# Play the macro.
macro.play()
