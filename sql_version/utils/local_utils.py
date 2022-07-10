import os
import tkinter as tk
import pyperclip as pc
from tkinter import messagebox, ttk
import sqlite3 as sql
import utils.global_var as global_var


def init_db(db_path):
    if not os.path.exists(db_path):
        print("ffffffff")
        db = sql.connect(db_path)
        db.execute(
            """CREATE TABLE Clipboard
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
    def append_df_row(df):
        cur = df.execute("SELECT Text FROM Clipboard").fetchall()
        for i in range(len(cur)):
            val = (len(cur) + 1 - (i + 1), cur[i][0])
            if (len(cur) + 1 - (i + 1)) % 2 == 0:
                tv.insert(parent="", index=0, values=val, tags=("evenrow",))
            else:
                tv.insert(parent="", index=0, values=val, tags=("oddrow",))

    def on_doubleClick(event):
        try:
            item = tv.identify("item", event.x, event.y)
            text = tv.item(item)["values"][1]
            print("you clicked on", text)
            pc.copy(text)
            messagebox.showinfo("ShowInfo", "Text Copied")
        except:
            pass

    def on_closing():
        ws.destroy()

    def update_tv():
        if global_var.sima_1 == 1:
            txt = pc.paste()
            tv.insert(parent="", index=0, values=(1, txt), tags=("oddrow",))
            x = tv.get_children()

            for i, item in enumerate(x):
                if i != 0:
                    idx, text = tv.item(item)["values"]
                    if (idx + 1)% 2 == 0:
                        tv.item(item, values=(idx + 1, text), tags=('evenrow',))
                    else:
                        tv.item(item, values=(idx + 1, text), tags=("oddrow"))
            global_var.sima_1 = 0
        ws.after(1, update_tv)

    ws = tk.Tk()
    ws.title("Clipboard-History")
    ws.geometry("550x350")

    tv = ttk.Treeview(
        ws, columns=(1, 2), show="headings", height=20, selectmode="browse"
    )

    tv.pack(side=tk.LEFT, fill=tk.BOTH)
    tv.heading(1, text="Index")
    tv.column(1, minwidth=30, width=50, stretch=tk.NO)
    tv.heading(2, text=global_var.cols_name[0])
    tv.column(2, minwidth=0, width=485, stretch=tk.NO)

    sb = tk.Scrollbar(ws)
    sb.pack(side=tk.RIGHT, fill=tk.BOTH)

    tv.tag_configure("oddrow", background="#272626")
    tv.tag_configure("evenrow", background="#161515")
    append_df_row(df)
    tv.bind("<Double-1>", on_doubleClick)

    tv.config(yscrollcommand=sb.set)
    sb.config(command=tv.yview)

    ws.protocol("WM_DELETE_WINDOW", on_closing)
    ws.resizable(width=False, height=True)

    style = ttk.Style()
    style.configure(
        "Treeview",
        rowheight=60,
        font=("Calibri", 10),
        bg="#1E1E1E",
        fg="#1E1E1E",
        selectmode=tk.SINGLE,
    )
    style.map("Treeview", background=[("selected", "#5E5E5E")])

    update_tv()
    ws.mainloop()
