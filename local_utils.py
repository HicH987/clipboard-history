import os
import pandas as pd
import tkinter as tk
import pyperclip as pc
from tkinter import messagebox, ttk

csv_file = "./data/clipboard_data.csv"
cols_name = ["text"]
sima = 0


class ClipboardUI:
    def display_ui(self, df):

        self.ws = tk.Tk()
        self.ws.title("Clipboard-History")
        self.ws.geometry("550x350")

        self.tv = ttk.Treeview(
            self.ws, columns=(1, 2), show="headings", height=20, selectmode="browse"
        )

        self.tv.pack(side=tk.LEFT, fill=tk.BOTH)
        self.tv.heading(1, text="Index")
        self.tv.column(1, minwidth=30, width=50, stretch=tk.NO)
        self.tv.heading(2, text=cols_name[0])
        self.tv.column(2, minwidth=0, width=485, stretch=tk.NO)

        self.sb = tk.Scrollbar(self.ws)
        self.sb.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.__append_df_row(df)
        self.tv.bind("<Double-1>", self.__on_doubleClick)

        self.tv.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.tv.yview)

        self.ws.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.ws.resizable(width=False, height=True)
        s = ttk.Style()
        s.configure(
            "Treeview",
            rowheight=100,
            font=("Calibri", 10),
            bg="#1E1E1E",
            fg="#FFFFFF",
            selectmode=tk.SINGLE,
        )
        self.__update_tv()
        self.ws.mainloop()

    def __append_df_row(self, df):
        for i in range(1, len(df) + 1):
            val = (len(df) + 1 - i, df.iloc[-i][cols_name[0]])
            self.tv.insert(parent="", index=0, values=val)

    def __on_doubleClick(self, event):
        item = self.tv.identify("item", event.x, event.y)
        text = self.tv.item(item)["values"][0]
        print("you clicked on", text)
        pc.copy(text)
        messagebox.showinfo("ShowInfo", "Text Copied")

    def __on_closing(self):
        self.ws.destroy()

    def __update_tv(self):
        global sima
        if sima == 1:
            txt = pc.paste()
            self.tv.insert(parent="", index=0, values=(1, txt))
            x = self.tv.get_children()

            for i, item in enumerate(x):
                if i != 0:
                    idx, text = self.tv.item(item)["values"]
                    self.tv.item(item, values=(idx + 1, text))
            sima = 0
        self.ws.after(1, self.__update_tv)


def init_empty_csv(csv_file, cols_name):
    if not os.path.exists(csv_file):
        data = pd.DataFrame([], columns=cols_name).set_index(cols_name[0])
        data.to_csv(csv_file)


def add_to_csv(add_data, csv_file):
    data = pd.read_csv(csv_file)
    top_row = pd.DataFrame({"text": [add_data]})
    data = pd.concat([top_row, data]).reset_index(drop=True)
    data.drop_duplicates(subset="text", keep="last", inplace=True)
    data.to_csv(csv_file, index=False)
