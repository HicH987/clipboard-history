from cgi import print_arguments
import os
import sqlite3 as sql


def create_connection(db_file):
    """create a database connection to a SQLite database"""
    db = None
    try:
        db = sql.connect(db_file)
        print(sql.version)
    except sql.Error as e:
        print(e)
    finally:
        if db:
            db.close()


def init_db(db_path):
    if not os.path.exists(db_path):
        print("not exist")
        db = sql.connect(db_path)
        db.execute(
            """CREATE TABLE Clipboard
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Text TEXT NOT NULL);"""
        )
    else:
        print("exist and connected")
        db = sql.connect(db_path)

    return db


def insert_data(db, txt):
    cur = db.execute("SELECT Text From Clipboard where Text = ? ", (txt,))
    len_data = len(list(cur))

    if len_data > 0:
        db.execute("DELETE FROM Clipboard  WHERE Text = ?", (txt,))
        # db.commit()
        print("delete")
    db.execute("INSERT INTO Clipboard (Text) VALUES (?)", (txt,))
    db.commit()
    print("add")


if __name__ == "__main__":
    db_path = "clipboard_database.db"
    db = init_db(db_path)
    # insert_data(
    #     db,
    #     "Google Sheets is a cloud-based spreadsheet application that can store data in a structured way just like most database management systems. We can connect Google Sheets with Python by enabling the API and downloading our credentials",
    # )

    # cur = db.execute("SELECT Text FROM Clipboard").fetchall()
    # for i in range(1, len(cur)+1):
    #     print(cur[-i][0]+"\n")

    cur = db.cursor()
    n = "sql"
    sql = "select Text from Clipboard where Text like ?"
    data = cur.execute(sql, ('%'+n+'%',)).fetchall()
    for d in data:
        print(d)
