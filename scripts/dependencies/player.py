import os
import json
import time
#import winsound

from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import (
    Controller as KeyboardController,
    Key,
    KeyCode,
)

mouse = MouseController()
keyboard = KeyboardController()


def load_recording(filename="recordings.json"):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_mouse_button(button_name):
    mapping = {
        "Button.left": Button.left,
        "Button.right": Button.right,
        "Button.middle": Button.middle,
    }
    return mapping.get(button_name)




def get_key(event):

    # Regular key stored by virtual-key code
    if "vk" in event:
        return KeyCode.from_vk(event["vk"])

    # Special key stored by name
    key_name = event["key"]




    if key_name.startswith("Key."):
        attribute = key_name.split(".", 1)[1]
        return getattr(Key, attribute)

    return key_name


def play_recording(repeat_count=1, filename="recordings.json"):

    events = load_recording(filename)

    print(f"Loaded {len(events)} events.")
    print("Playback starting in...\n")

    '''
    sound_file = os.path.join(os.path.dirname(__file__), "sound", "countdown.wav")
    winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
    '''
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    print()

    for current_repeat in range(repeat_count):

        print(f"\nPlayback {current_repeat + 1} of {repeat_count}")

        for event in events:

            time.sleep(event["time"])

            event_type = event["type"]

            if event_type == "move":
                mouse.position = (event["x"], event["y"])

            elif event_type == "click":
                mouse.position = (event["x"], event["y"])

                button = get_mouse_button(event["button"])

                if button is not None:
                    if event["pressed"]:
                        mouse.press(button)
                    else:
                        mouse.release(button)

            elif event_type == "scroll":
                mouse.position = (event["x"], event["y"])
                mouse.scroll(event["dx"], event["dy"])

            elif event_type == "key_press":
                key = get_key(event)
                keyboard.press(key)

            elif event_type == "key_release":
                key = get_key(event)
                keyboard.release(key)

        keyboard.release(Key.shift)
        keyboard.release(Key.ctrl)
        keyboard.release(Key.alt)

    print("\nPlayback finished.")