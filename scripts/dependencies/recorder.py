import os
import json
import time
from pynput import mouse, keyboard

events = []

last_event_time = None
shift_pressed = False
shift_key = None


def record_event(event):
    global last_event_time

    current_time = time.perf_counter()

    if last_event_time is None:
        delay = 0
    else:
        delay = current_time - last_event_time

    last_event_time = current_time

    event["time"] = round(delay, 6)

    events.append(event)


# ------------------------
# Mouse
# ------------------------

def on_move(x, y):
    record_event({
        "type": "move",
        "x": x,
        "y": y
    })


def on_click(x, y, button, pressed):
    record_event({
        "type": "click",
        "x": x,
        "y": y,
        "button": str(button),
        "pressed": pressed
    })


def on_scroll(x, y, dx, dy):
    record_event({
        "type": "scroll",
        "x": x,
        "y": y,
        "dx": dx,
        "dy": dy
    })


# ------------------------
# Keyboard
# ------------------------

def make_key_event(event_type, key):
    event = {"type": event_type}

    if isinstance(key, keyboard.KeyCode):
        event["vk"] = key.vk
    else:
        event["key"] = str(key)

    return event


def on_press(key):
    global shift_pressed
    global shift_key

    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = True
        shift_key = str(key)

    record_event(make_key_event("key_press", key))


def on_release(key):
    global shift_pressed
    global shift_key

    # Shift+Esc stops recording
    record_event(make_key_event("key_release", key))

    if shift_pressed and key == keyboard.Key.esc:
        print("\nRecording stopped.\n")
        return False

    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = False
        shift_key = None


# ------------------------
# Listener
# ------------------------

def save_recording(filename="recordings.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)




def start_listening():
    global events
    global last_event_time
    global shift_pressed
    global shift_key

    events = []
    last_event_time = None
    shift_pressed = False
    shift_key = None

    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )

    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )

    mouse_listener.start()
    keyboard_listener.start()

    keyboard_listener.join()
    mouse_listener.stop()

    print(f"\nRecorded {len(events)} events.")

    save_recording()

    return events