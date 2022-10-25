# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
from tkinter import messagebox
import sys # used to access the command line arguments
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

def startSession():
    tkinter.messagebox.showinfo("session", "A new listening session has been started")

def searchInDB(keywords):
    # Arguments: 
    #   keywords: an array of string containing the keywords of the search
    # Returns:
    #   result: a sorted list of tuples

    # Initialize the function that will calculate the keywords in sql
    connection.create_function('countKeywords', 2, countKeywords )
    # Create the list of tuples that we will return and contains all the songs and playlists
    result = []

    # Find matching songs
    cursor.execute('''
    SELECT sid, title, duration, countKeywords(title,:keywords)
    FROM songs s
    WHERE countKeywords(title,:keywords) > 0;
    ''',{"keywords":keywords})

    # Store all matching songs in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Songs",row[0],row[1], row[2], row[3]))

    # Find matching playlists 
    cursor.execute('''
    SELECT p.pid, p.title, SUM(l.cnt*s.duration), countKeywords(title, :keywords)
    FROM playlists p
    LEFT OUTER JOIN plinclude pl USING(pid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(title, :keywords) > 0
    GROUP BY p.pid, p.title;
    ''', {"keywords":keywords})

    # Store all matching playlists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Playlist",row[0],row[1], row[2], row[3]))

    # Return all of the matching songs and playlists
    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    return result
    

def countKeywords(title, keywords):
    # Arguments:
    #   title: A string indicating the title of a song
    #   keywords: an array of strings containing the keywords of a search
    # Returns:
    #   count: number of keywords in the title

    count = 0 # number of keywords

    # For each keyword, we check if it appears in the title
    # Note: the comparison is not case-sensitive
    for keyword in keywords:
        for word in title.split():
            if(keyword.lower() == word.lower()):
                count += 1

    # return how many keywords were in title
    return count




def main():
    '''
    #prompt the name of the database
    path_in = input() 
    #set the path to the database
    path = "./" + path_in 
    #connect to the database
    connect(path) 
    '''
    # We connect to the database
    # We assumes that the database is in the same folder as the program
    connect("./" + sys.argv[1])
    login()
    
if __name__ == "__main__":
    main()