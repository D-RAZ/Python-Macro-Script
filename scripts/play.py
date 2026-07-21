from dependencies.player import play_recording

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