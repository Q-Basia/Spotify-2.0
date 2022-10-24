# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
from tkinter import messagebox
#from tkinter import simpledialog

connection = None
cursor = None

root = tkinter.Tk() 
root.title("welcome")
root.geometry("200x100")

    
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return

def startSession():
    tkinter.messagebox.showinfo("session", "A new listening session has been started")


s = Button(root, text = "Start session", command = startSession, activeforeground="red", activebackground="pink", pady=10)
s.pack(side = "top")
root.mainloop()


def main():
    '''
    #prompt the name of the database
    path_in = input() 
    #set the path to the database
    path = "./" + path_in 
    #connect to the database
    connect(path) 
    '''
    
    #page.withdraw()

    #user_type = simpledialog.askstring(title = "Song management", prompt = "Are you a user or an artist")
    #print(user_type)
    
