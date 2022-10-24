# This will be our source code
import tkinter as tk
from tkinter import simpledialog

ROOT = tk.TK()

ROOT.withdraw()

user_type = simple.askstring(title = "Song management", prompt = "Are you a user or an artist")