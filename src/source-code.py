# This will be our source code
import sqlite3
import tkinter as tk
from tkinter import simpledialog

ROOT = tk.TK()

ROOT.withdraw()

user_type = simpledialog.askstring(title = "Song management", prompt = "Are you a user or an artist")
print("Testing GitHub")