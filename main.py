import keyboard
import threading
import pandas as pd
import pyperclip as pc
from local_utils import *


def show_clipboard_history():
    while True:
        keyboard.wait("shift+ctrl+<")
        print("Display ClipBoard-History")

        df = pd.read_csv(csv_file)
        clipboard_history_ui = ClipboardUI()
        clipboard_history_ui.display_ui(df)


def add_to_clipboard():
    global sima
    while True:
        text = pc.waitForNewPaste()
        sima = 1
        print("Copy New-Paste to ClipBoard-History ")
        add_to_csv(text, csv_file)


if __name__ == "__main__":
    print("start programme")
    init_empty_csv(csv_file, cols_name)

    th_add = threading.Thread(target=add_to_clipboard)
    th_add.setDaemon(True)
    th_add.start()

    th_show = threading.Thread(target=show_clipboard_history())
