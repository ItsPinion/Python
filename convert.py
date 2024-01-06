import json

key_mappings = {
    "cmd": "win",
    "alt_l": "alt",
    "alt_r": "alt",
    "ctrl_l": "ctrl",
    "ctrl_r": "ctrl"
}

def read_json_file():
    with open('recording.json') as f:
        recording = json.load(f)
    def excluded_actions(object):
        return "released" not in object["action"] and "scroll" not in object["action"]
    recording = list(filter(excluded_actions, recording))
    return recording

def convert_to_pyautogui_script(recording):
    if not recording: 
        return
    output = open("play.py", "w")
    output.write("import time\n")
    output.write("import pyautogui\n\n")
    for i, step in enumerate(recording):
        not_first_element = (i - 1) > 0
        if not_first_element:
            pause_in_seconds = (step["_time"] - recording[i - 1]["_time"]) * 1.1 
            output.write(f"time.sleep({pause_in_seconds})\n\n")
        else:
            output.write("time.sleep(1)\n\n")
        if step["action"] == "pressed_key":
            key = step["key"].replace("Key.", "") if "Key." in step["key"] else step["key"]
            if key in key_mappings.keys():
                key = key_mappings[key]
            output.write(f"pyautogui.press('{key}')\n")
        if step["action"] == "clicked":
            output.write(f"pyautogui.moveTo({step['x']}, {step['y']})\n")
            if step["button"] == "Button.right":
                output.write("pyautogui.mouseDown(button='right')\n")
            else:
                output.write("pyautogui.mouseDown()\n")
        if step["action"] == "unclicked":
            output.write(f"pyautogui.moveTo({step['x']}, {step['y']})\n")
            if step["button"] == "Button.right":
                output.write("pyautogui.mouseUp(button='right')\n")
            else:
                output.write("pyautogui.mouseUp()\n")
    print("Recording converted. Saved to 'play.py'")

if __name__ == "__main__":
    recording = read_json_file()
    convert_to_pyautogui_script(recording)
