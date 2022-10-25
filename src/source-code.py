# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
from tkinter import messagebox
#from tkinter import simpledialog

connection = None
cursor = None

def choose():
    chooseWindow = Tk()
    chooseMessage = Label(chooseWindow)
    
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

def passwordValidate(ID, p):
    global connection, cursor
    
    print(ID.get(), p.get())
    
#this function will create and take the user id and password
def login():
    buttons = {}
    loginWindow = Tk()
    loginWindow.geometry("400x250")
    loginWindow.title("Music is cool") #title of the page
    
    # initiate variables to save the values of password and ID
    username = tkinter.StringVar()
    password = tkinter.StringVar()

    #create the username input box 
    usernameLabel = Label(loginWindow, text = "ID").grid(row=0, column=0)
    usernameEntry = Entry(loginWindow, textvariable = username).grid(row=0, column=1)
    
    #creating the password input box 
    passwordLabel = Label(loginWindow, text = "Password").grid(row=1, column=0)
    # make sure the password appears as * to the user
    passwordEntry = Entry(loginWindow, textvariable = password, show="*").grid(row=1, column=1)
    
    #creating the login button to press after having written the user ID and the password
    buttons["login"] = Button(loginWindow, text = "login", command=lambda: [passwordValidate(username, password), loginWindow.destroy()]).grid(row=4, column=0)
    buttons["register"] = Button(loginWindow, text = "register", command= loginWindow.destroy()).grid(row=5, column=0)
    loginWindow.mainloop()
    return


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