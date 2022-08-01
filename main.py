import keyboard
import threading
import pyperclip as pc
import utils.local_utils as local_utils
import utils.global_var as global_var

def show_clipboard_history():
    db = local_utils.init_db(global_var.db_path)
    print("th2 db connect")

    while True:
        keyboard.wait(global_var.key_shortcut)
        print("Display ClipBoard-History")
        local_utils.disply_history(db)


def add_to_clipboard():
    db = local_utils.init_db(global_var.db_path)
    print("th1 db connect")

    while True:
        text = pc.waitForNewPaste()
        print("Copy New-Paste to ClipBoard-History ")
        local_utils.insert_data(db, text)


if __name__ == "__main__":
    print("start programme")
    th_show = threading.Thread(target=show_clipboard_history)
    th_show.setDaemon(True)
    th_show.start()
    th_add = threading.Thread(target=add_to_clipboard())
