import os
import sys
import pprint
import keyboard
import fileinput
import subprocess
import regex as re
import tkinter as tk
import sqlite3 as sql
import pyperclip as pc
from tkinter import ttk
from tkinter import messagebox
import utils.global_var as global_var

# Global Variable
msgb_on = False


def init_db(db_path):
    if not os.path.exists(db_path):
        db = sql.connect(db_path)
        db.execute(
            """CREATE TABLE Clipboardk
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Text TEXT NOT NULL);"""
        )
    else:
        db = sql.connect(db_path)

    return db


def insert_data(db, txt):
    cur = db.execute("SELECT Text From Clipboard where Text = ? ", (txt,)).fetchall()
    len_data = len(cur)

    if len_data > 0:
        db.execute("DELETE FROM Clipboard  WHERE Text = ?", (txt,))
        print("delete")
    db.execute("INSERT INTO Clipboard (Text) VALUES (?)", (txt,))
    db.commit()
    print("add")


def disply_history(df):
#!----------------GLOBAL VARIABLE-------------
    search_on = False
    
#!----------------MAIN WINDOW---------------
    ws = tk.Tk()
    ws.title("Clipboard-History")
    ws.geometry("550x437")
    ws.iconbitmap(global_var.icon_path)
    ws.attributes("-topmost", True)
    ws.protocol("WM_DELETE_WINDOW", lambda: ws.destroy())
    ws.resizable(width=False, height=False)
    ws.focus_set()

#!----------------TREEVIEW-------------------
    def on_doubleClick(event):
        try:
            item = tv.identify("item", event.x, event.y)
            text = tv.item(item)["values"][2]
            print("you clicked on", text)
            pc.copy(text)
            ws.destroy()
        except:
            pass
    
    tv = ttk.Treeview(
        ws, columns=(1, 2, 3), show="headings", height=20, selectmode="browse"
    )
    tv.pack(side=tk.LEFT, fill=tk.BOTH, pady=30)
    tv.heading(1, text="Index")
    tv.column(1, minwidth=30, width=50, stretch=tk.NO)
    tv.heading(2, text=global_var.cols_name[0])
    tv.column(2, minwidth=0, width=485, stretch=tk.NO)
    tv.column(3, minwidth=0, width=0, stretch=tk.NO)
    tv.tag_configure("oddrow", background="#272626")
    tv.tag_configure("evenrow", background="#161515")
    tv.bind("<Double-1>", on_doubleClick)
    

#!----------------SCROLL BAR-------------------
    sb = tk.Scrollbar(ws)
    sb.pack(side=tk.RIGHT, fill=tk.BOTH, pady=30)
    sb.config(command=tv.yview)
    tv.config(yscrollcommand=sb.set)
    
#!----------------TREEVIEW-TEXT HOVER-------------------
    def highlight_row(event):
        tree = event.widget
        item = tree.identify_row(event.y)
        try:
            lbl.config(text=tree.item(item)["values"][2])
            lbl.place(x=event.x, y=event.y + 50)
            tree.tk.call(tree, "tag", "add", "highlight", item)
            ws.after(9000, lambda: lbl.place_forget())
        except:
            pass
    
    lbl = tk.Label(ws, bg="#383838")
    tv.tag_configure("highlight", background="lightblue")
    tv.bind("<Motion>", highlight_row)

#!----------------ADD DATA TO TREEVIEW-------------------
    def append_df_row(df, sql, lst_term=None):
        if lst_term is None:
            cur = df.execute(sql).fetchall()
        else:
            cur = df.execute(sql, lst_term).fetchall()
        for i in range(len(cur)):
            txt = cur[i][0]
            if len(cur[i][0]) > 30:
                txt = txt[:30] + "..."
            val = (len(cur) + 1 - (i + 1), txt, cur[i][0])
            if (len(cur) + 1 - (i + 1)) % 2 == 0:
                tv.insert(parent="", index=0, values=val, tags=("evenrow",))
            else:
                tv.insert(parent="", index=0, values=val, tags=("oddrow",))
            tv.tag_bind(i, "<Motion>", highlight_row)
    
    append_df_row(df, sql="SELECT Text FROM Clipboard")
    try:
        child_id = tv.get_children()[0]
        tv.focus(child_id)
        tv.selection_set(child_id)
    except:
        pass

#!----------------TREEVIEW STYLE-------------------
    style = ttk.Style()
    style.configure(
        "Treeview",
        rowheight=50,
        font=("Calibri", 10, "bold"),
        bg="#1E1E1E",
        fg="#1E1E1E",
        selectmode=tk.SINGLE,
    )
    style.map("Treeview", background=[("selected", "#5E5E5E")])

#!----------------SEARCHBAR-------------------
    def search():
        nonlocal search_on
        name = ws_ent.get()
        if len(name) > 0:
            search_on = True
            for record in tv.get_children():
                tv.delete(record)
            sql = f"select Text from Clipboard where Text like ?"
            append_df_row(df, sql, lst_term=(f"%name%",))
            try:
                child_id = tv.get_children()[0]
                tv.focus(child_id)
                tv.selection_set(child_id)
            except:
                pass
    
    def reset():
        nonlocal search_on
        if len(tv.get_children()) <= 0 or search_on:
            append_df_row(df, "SELECT Text FROM Clipboard")
            search_on = False
    
    ws_ent = tk.Entry(ws, width=20, font=("Arial", 10, "bold"))
    ws_ent.place(x=5, y=6)
    ws_btn1 = tk.Button(
        ws, text="Search", width=5, font=("calibri", 10, "normal"), command=search
    )
    ws_btn1.place(x=200, y=3)
    ws_btn2 = tk.Button(
        ws, text="Reset", width=5, font=("calibri", 10, "normal"), command=reset
    )
    ws_btn2.place(x=300, y=3)
    
#!----------------MENUBAR-------------------
    def clear_db():
        global msgb_on
        msgb_on = True
        MsgBox = messagebox.askquestion(
            "Delet clipbord db", "Are You Sure ?", icon="warning"
        )
        if MsgBox == "yes":
            cur = df.cursor()
            cur.execute("DELETE FROM Clipboard")
            df.commit()
            for record in tv.get_children():
                tv.delete(record)
            print("delete table")
        msgb_on = False
    
    def get_db_file():
        allPath = os.path.realpath(global_var.db_path)
        subprocess.Popen(f"explorer /select,{allPath}")
    
    def exit_pgm():
        global msgb_on
        msgb_on = True
        msgbox = messagebox.askquestion("Exit", "Are You Sure ?", icon="warning")
        if msgbox == "yes":
            try:
                df.close()
            except:
                pass
            try:
                ws.destroy()
            except:
                pass
            os._exit(0)
        else:
            msgb_on = False
    
    menubar = tk.Menu(ws)
    # Adding Edit Menu and commands
    edit = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit)
    edit.add_command(label="Clear Db", command=clear_db)
    # display Menu
    ws.config(menu=menubar)
    edit.add_command(label="Show Db File", command=get_db_file)
    edit.add_separator()
    edit.add_command(label="Keyboard Shortcut", command=keyShortcut)
    edit.add_separator()
    edit.add_command(label="Exit", command=exit_pgm)
    
#!----------------EXIT & MAINLOOP-------------------
    def lossfocus(event):
        global msgb_on
        if not msgb_on:
            if event.widget is ws:
                # check which widget getting the focus
                w = ws.tk.call("focus")
                if not w:
                    # not widget in this window
                    ws.destroy()
    
    ws.bind("<FocusOut>", lossfocus)
    ws.after(1, lambda: ws.focus_force())
    ws.mainloop()
    

def keyShortcut():
#!----------------GLOBAL VARIABLE-------------
    global msgb_on
    msgb_on = True
    
    in_msgBox = False
    key = ""
    txt = ""
    nb_key = 3
    last_key = None

#!----------------WINDOW---------------
    def key_pressed(event):
        nonlocal key
        key = keyboard.read_key()
        lbl_key.config(text=key)
        lbl_key.place(x=120, y=40)
    
    root = tk.Tk()
    root.title("Shortcut")
    root.geometry("240x240")
    root.attributes("-topmost", True)
    root.iconbitmap(global_var.icon_path)
    root.bind("<Key>", key_pressed)
    
#!----------------LABELS---------------
    lbl_title = tk.Label(
        root, text="Enter Key Shortcut", font=("Calibri", 15, "bold"), justify="center"
    )
    lbl_title.place(x=40, y=5)
    lbl_currentKey = tk.Label(
        root, text="- Current Key:  ", font=("Calibri", 12, "bold"), justify="center"
    )
    lbl_currentKey.place(x=20, y=40)
    lbl_currentKey = tk.Label(
        root, text="- Shortcut:  ", font=("Calibri", 12, "bold"), justify="center"
    )
    lbl_currentKey.place(x=20, y=120)
    lbl_key = tk.Label(root, font=("Calibri", 12, "bold"), justify="center")
    lbl_shortKey = tk.Label(root, font=("Calibri", 12, "bold"), justify="center")

#!----------------BUTTONS-------------------
    def remplace_initVal(var_name, remplace_val, file_name):
        patt = f"(?<=(^{var_name}\s*=\s*)).*"
        change = False
        for line in fileinput.input(file_name, inplace=1):
            if var_name in line:
                rep_line, nb_car = re.subn(patt, remplace_val, line)
                if nb_car > 0:
                    change = True
                    line = rep_line
            sys.stdout.write(line)
        return change
    
    def plus_key():
        nonlocal key, last_key, txt, nb_key, in_msgBox
        print("last_key: ", last_key)
        print("key: ", key)
        if key != "" and last_key != key:
            if nb_key > 0:
                if txt == "":
                    txt = key
                else:
                    txt = txt + " + " + key
                last_key = key
                key = ""
                lbl_shortKey.config(text=txt, bg="#4D4D4D")
                lbl_shortKey.place(x=60, y=143)
                lbl_key.place_forget()
                nb_key -= 1
            else:
                in_msgBox = True
                m = messagebox.showwarning(
                    "showwarning", "shortcut's lenght greater than 3"
                )
                if m in ("ok", "yes"):
                    pass
                root.focus_force()
                in_msgBox = False
        print(txt)
    
    def save_key():
        nonlocal txt, nb_key, in_msgBox
        global msgb_on
        if nb_key <= 1:
            print("in save")
            global_var.key_shortcut = txt
            globalVar_path = os.path.realpath(global_var.file_path)
            remplace_initVal("key_shortcut", pprint.pformat(txt), globalVar_path)
            root.destroy()
            msgb_on = False
    
    btn_confirm = tk.Button(
        root,
        text="confirm key",
        width=10,
        font=("calibri", 10, "normal"),
        command=plus_key,
    )
    btn_confirm.place(x=34, y=75)
    btn_save = tk.Button(
        root, text="Save", width=7, font=("calibri", 13, "normal"), command=save_key
    )
    btn_save.place(x=65, y=180)
    
#!----------------EXIT & MAINLOOP-------------------
    def lossfocus(event):
        global msgb_on
        nonlocal in_msgBox
        if not in_msgBox:
            if event.widget is root:
                # check which widget getting the focus
                w = root.tk.call("focus")
                if not w:
                    # not widget in this window
                    root.destroy()
                    msgb_on = False
    
    root.after(1, lambda: root.focus_force())
    root.bind("<FocusOut>", lossfocus)
    root.mainloop()
    msgb_on = False


