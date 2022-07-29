import os
import subprocess
import tkinter as tk
import sqlite3 as sql
from tkinter import messagebox

import pyperclip as pc
from tkinter import ttk
import utils.global_var as global_var


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
    search_on = False

    def append_df_row(df, sql, term=None):
        if term is None:
            cur = df.execute(sql).fetchall()
        else:
            cur = df.execute(sql, ("%" + term + "%",)).fetchall()
        for i in range(len(cur)):
            txt = cur[i][0]
            if len(cur[i][0]) > 30:
                txt = txt[:30] + "..."
            val = (len(cur) + 1 - (i + 1), txt, cur[i][0])
            if (len(cur) + 1 - (i + 1)) % 2 == 0:
                tv.insert(parent="", index=0, values=val, tags=("evenrow",))
            else:
                tv.insert(parent="", index=0, values=val, tags=("oddrow",))

    def on_doubleClick(event):
        try:
            item = tv.identify("item", event.x, event.y)
            text = tv.item(item)["values"][2]
            print("you clicked on", text)
            pc.copy(text)
            ws.destroy()
        except:
            pass

    def resetDb():
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

    def get_db_file():
        allPath = os.path.realpath(global_var.db_path)
        subprocess.Popen(f"explorer /select,{allPath}")

    def search():
        nonlocal search_on
        name = ws_ent.get()
        if len(name) > 0:
            search_on = True
            for record in tv.get_children():
                tv.delete(record)
            sql = f"select Text from Clipboard where Text like ?"
            append_df_row(df, sql, term=name)
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

    def lossfocus(event):
        if event.widget is ws:
            # check which widget getting the focus
            w = ws.tk.call('focus')
            if not w:
                # not widget in this window
                ws.destroy()

# -------------MAIN-------------
# root win
    ws = tk.Tk()
    ws.title("Clipboard-History")
    ws.geometry("550x437")
    ws.attributes("-topmost", True)
    ws.protocol("WM_DELETE_WINDOW", lambda: ws.destroy())
    ws.resizable(width=False, height=False)
    ws.focus_set()
# treeview
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

# scroll bar
    sb = tk.Scrollbar(ws)
    sb.pack(side=tk.RIGHT, fill=tk.BOTH, pady=30)
    sb.config(command=tv.yview)
    tv.config(yscrollcommand=sb.set)

# search bar
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

# Creating Menubar
    menubar = tk.Menu(ws)
    # Adding Edit Menu and commands
    edit = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit)
    edit.add_command(label="reset database", command=resetDb)
    # display Menu
    ws.config(menu=menubar)
    edit.add_command(label="get to db file", command=get_db_file)

# add data to tv
    append_df_row(df, sql="SELECT Text FROM Clipboard")
    try:
        child_id = tv.get_children()[0]
        tv.focus(child_id)
        tv.selection_set(child_id)
    except:
        pass

# tv style
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


    ws.bind("<FocusOut>",lossfocus)
    ws.after(1, lambda: ws.focus_force())
    ws.mainloop()
