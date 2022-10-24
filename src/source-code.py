# This will be our source code
import sqlite3
import tkinter as tk
from tkinter import simpledialog

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return

def main():
    path_in = input()
    path = "./" + path_in
    connect(path)
    ROOT = tk.Tk()

    ROOT.withdraw()

    user_type = simpledialog.askstring(title = "Song management", prompt = "Are you a user or an artist")
    print(user_type)
    
if __name__ == "__main__":
    main()