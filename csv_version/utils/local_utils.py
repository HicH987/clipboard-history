import os
import pandas as pd
import tkinter as tk
import pyperclip as pc
from tkinter import messagebox, ttk
import utils.global_var as global_var


def init_empty_csv(csv_file, cols_name):
    if not os.path.exists(csv_file):
        data = pd.DataFrame([], columns=cols_name).set_index(cols_name[0])
        data.to_csv(csv_file)


def add_to_csv(add_data, csv_file):
    data = pd.read_csv(csv_file)
    top_row = pd.DataFrame({"text": [add_data]})
    data = pd.concat([top_row, data]).reset_index(drop=True)
    data.drop_duplicates(subset="text", keep="first", inplace=True)
    data.to_csv(csv_file, index=False)


def disply_history(df):
    def append_df_row(df):
        for i in range(1, len(df) + 1):
            val = (len(df) + 1 - i, df.iloc[-i]['text'])
            tv.insert(parent="", index=0, values=val)
        
        # for i in range(len(df)):
        #     val = (i+1, df.iloc[i][global_var.cols_name[0]])
        #     tv.insert(parent="", index='end', values=val)
            # if (i + 1)% 2 == 0:
            #     tv.insert(parent="", index='end', values=val, tags=('evenrow',))
            # else:
            #     tv.insert(parent="", index='end', values=val, tags=("oddrow",))

    def on_doubleClick(event):
        item = tv.identify("item", event.x, event.y)
        text = tv.item(item)["values"][1]
        print("you clicked on", text)
        pc.copy(text)
        messagebox.showinfo("ShowInfo", "Text Copied")
        
    def on_closing():
        for after_id in ws.tk.eval('after info').split():
            ws.after_cancel(after_id)
        ws.destroy()

    def update_tv():
        if global_var.sima == 1:
            txt = pc.paste()
            # tv.insert(parent="", index=0, values=(1, txt), tags=("oddrow",))
            tv.insert(parent="", index=0, values=(1, txt))
            x = tv.get_children()

            for i, item in enumerate(x):
                if i != 0:
                    idx, text = tv.item(item)["values"]
                    tv.item(item, values=(idx + 1, text))
                    # if (idx + 1)% 2 == 0:     
                    #     tv.item(item, values=(idx + 1, text), tags=('evenrow',))
                    # else:
                    #     tv.item(item, values=(idx + 1, text), tags=("oddrow"))
                        
            global_var.sima = 0
            
        ws.after(1, update_tv)


    ws = tk.Tk()
    # ws = tk.Toplevel()
    ws.title("Clipboard-History")
    ws.geometry("550x390")

    tv = ttk.Treeview(
        ws, columns=(1, 2), show="headings", height=20, selectmode="browse"
    )

    tv.pack(side=tk.LEFT, fill=tk.BOTH)
    tv.heading(1, text="Index")
    tv.column(1, minwidth=30, width=50, stretch=tk.NO)
    tv.heading(2, text="text")
    tv.column(2, minwidth=0, width=485, stretch=tk.NO)

    sb = tk.Scrollbar(ws)
    sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    
    # tv.tag_configure("oddrow", background="#272626")
    # tv.tag_configure("evenrow", background="#161515")
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
        # fg="#FFFFFF",
        selectmode=tk.SINGLE,
    )

    style.map('Treeview', 
        background=[('selected', '#5E5E5E')])

    update_tv()
    ws.mainloop()
