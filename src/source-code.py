# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
from tkinter import messagebox
#from tkinter import simpledialog

connection = None
cursor = None

def startSession():
    root = tkinter.Tk() 
    root.title("welcome")
    root.geometry("200x100")
    s = Button(root, text = "Start session", command = startSession, activeforeground="red", activebackground="pink", pady=10)
    s.pack(side = "top")
    root.mainloop()

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return

def passwordValidate():
    print("you're in")
    
#this function will create and take the user id and password
def login():
    loginWindow = Tk()
    loginWindow.geometry("400x250")
    loginWindow.title("Music is cool") #title of the page
    
    #create the username input box 
    usernameLabel = Label(loginWindow, text = "User ID").grid(row=0, column=0)
    username = StringVar();
    usernameEntry = Entry(loginWindow, textvariable = username).grid(row=0, column=1)
    
    #creating the password input box 
    passwordLabel = Label(loginWindow, text = "Password").grid(row=1, column=0)
    password = StringVar();
    passwordEntry = Entry(loginWindow, textvariable = password, show="*").grid(row=1, column=1)
    
    #creating the login button to press after having written the user ID and the password
    loginButton = Button(loginWindow, text = "login", command=lambda: [passwordValidate, loginWindow.destroy()]).grid(row=4, column=0)
    loginWindow.mainloop()
    return

def startSession():
    tkinter.messagebox.showinfo("session", "A new listening session has been started")





def main():
    '''
    #prompt the name of the database
    path_in = input() 
    #set the path to the database
    path = "./" + path_in 
    #connect to the database
    connect(path) 
    '''
    login()
    
if __name__ == "__main__":
    main()