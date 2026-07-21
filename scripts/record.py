from dependencies.recorder import start_listening

if __name__ == "__main__":

    print("Recording...")
    print("Press Shift+ESC to stop.\n")

    events = start_listening()

    print("\nDone.")