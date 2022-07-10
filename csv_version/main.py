import keyboard
import threading
import pandas as pd
import pyperclip as pc
import utils.global_var as global_var
import utils.local_utils as local_utils


def show_clipboard_history():
    while True:
        keyboard.wait("shift+ctrl+<")
        print("Display ClipBoard-History")

        df = pd.read_csv(global_var.csv_file)
        local_utils.disply_history(df)


def add_to_clipboard():
    while True:
        text = pc.waitForNewPaste()
        global_var.sima = 1
        print("Copy New-Paste to ClipBoard-History ")
        local_utils.add_to_csv(text, global_var.csv_file)

if __name__ == "__main__":
    print("start programme")
    local_utils.init_empty_csv(global_var.csv_file, global_var.cols_name)

    th_add = threading.Thread(target=add_to_clipboard)
    th_add.setDaemon(True)
    th_add.start()

    th_show = threading.Thread(target=show_clipboard_history())
