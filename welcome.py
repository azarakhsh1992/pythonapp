import os
import time
import sys

def welcome_train():
    # ASCII art representation of "Welcome"
    ascii_message = [
        "W       W  EEEEE  L      CCCC  OOO  M     M  EEEEE       K   K  IIIII  M   M  IIIII  AAAAA",
        "W       W  E      L     C     O   O MM   MM  E           K  K     I    MM MM    I    A   A",
        "W   W   W  EEEEE  L     C     O   O M M M M  EEEEE       KKK      I    M M M    I    AAAAA",
        " W W W W   E      L     C     O   O M  M  M  E           K  K     I    M   M    I    A   A",
        "  W   W    EEEEE  LLLLL  CCCC  OOO  M     M  EEEEE       K   K  IIIII  M   M  IIIII  A   A"
    ]

    while True:
        width = os.get_terminal_size().columns

        for i in range(width + max(len(line) for line in ascii_message), -1, -1):
            sys.stdout.write("\r\n" * len(ascii_message))  # Move cursor up to start position
            for line in ascii_message:
                # Calculate the position to start printing the message
                start_pos = max(i - len(line), 0)
                # Determine the part of the message to print
                part_to_print = line[max(len(line) - i, 0):]
                # Print the message at the new position
                sys.stdout.write("\r" + " " * start_pos + part_to_print + "\n")
            # sys.stdout.flush()
            time.sleep(0.05)
            sys.stdout.write("\033[F" * len(ascii_message))  # Move cursor back up to overwrite

        # Clear the screen at the end of each full pass
        sys.stdout.write("\r" + "\n" * len(ascii_message) + "\033[F" * len(ascii_message))
        sys.stdout.flush()

welcome_train()
