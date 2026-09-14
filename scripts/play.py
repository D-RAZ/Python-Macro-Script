import ctypes
import os

from dependencies.player import play_recording

def play_done_sound():
    sound_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "dependencies",
        "done.mp3"
    )

    winmm = ctypes.windll.winmm

    winmm.mciSendStringW(
        f'open "{sound_file}" type mpegvideo alias done_sound',
        None,
        0,
        None
    )

    winmm.mciSendStringW(
        "play done_sound wait",
        None,
        0,
        None
    )

    winmm.mciSendStringW(
        "close done_sound",
        None,
        0,
        None
    )

if __name__ == "__main__":

    while True:
        try:
            repeat_count = int(
                input("How many times would you like to replay the recording? ")
            )

            if repeat_count < 1:
                print("Please enter a number greater than 0.\n")
                continue

            break

        except ValueError:
            print("Please enter a valid integer.\n")

    play_recording(repeat_count=repeat_count)
    play_done_sound()
