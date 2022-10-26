# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
import sys # used to access the command line arguments
#from tkinter import simpledialog

connection = None
cursor = None

# create global variables to store the is and password of the user
ps = ""
id = ""

# create the app window using 'Tk()', which is a function form tkinter
window = Tk()
# set the title of the window
window.title("Spotify 2.0") #title of the page

# this function removes all widgets that were created for the specified page
# to leave space for a new page
#arguments:
#   frame: the page that we want to remove from the window
def clearFrame(frame):
    global window
    frame.forget()
 
# Creates a page that displays a message to tell the user that the password is incorrect
#   Also has a button to return to the home page
def wrongPass():
    global window
    
    # create the page and pack it
    wrong = Frame(window)
    wrong.pack()
    
    # create a label to display the error message
    Label(wrong, text="password is incorrest, please return to home page and try again", fg='red').grid(row = 0, column = 0)
    
    # create the button to return to the home page
    Button(wrong, text="return", command=lambda: [clearFrame(wrong), home()]).grid(row = 1, column= 0)
    
# creates a page that displays a message to tell the user the id doesn;t exist in the database    
# with a button to return to the home page
def notInList():
    global window
    
    #create the page
    er = Frame(window)
    er.pack()
    
    # create a label to display the message
    Label(er, text = "ID does not match a user or artist, please return to the home page to try again or register", fg ='red').grid(row = 0, column = 0)
    
    # create a button to return to the home page
    Button(er, text="return", command=lambda: [clearFrame(er), home()]).grid(row = 1, column= 0)
    
# Sets the values of the id and password that were taken from the input box
# argument:
#   i: the id that was entered in the input
#   p: the password value that was entered in the input 
def setGlobals(i, p):
    global ps, id
    id = i.get()
    ps = p.get()
    
# resets the values of id and password to null
# called when a user logs out of the app
def reset():
    global id, ps
    id = ""
    ps = ""
    
# creates a page that will display all actions for an artist
# no argument or return value
def artistPage():
    global window 
    
    # initiate value for if the artist wants to add a song
    new_song = ""
    
    # create page
    artistFrame = Frame(window)
    artistFrame.pack()
    
    # label to tell the artist where to enter values of new song
    Label(artistFrame, text="please enter name and duration of song in seconds, respectively").grid(row=0, column=0)
    # input box for the song details, must be name followed by suration
    Entry(artistFrame, textvariable = new_song).grid(row=1, column=0)
    
    # buttons to add the song, find top users and top playlists
    Button(artistFrame, text = "add song").grid(row=2, column=0, pady=(0,20))
    Button(artistFrame, text = "find top users", command=lambda: [clearFrame(artistFrame)]).grid(row=3, column=0)
    Button(artistFrame, text = "find top playlists", command=lambda: [clearFrame(artistFrame)]).grid(row=4, column=0)
    # button to logout and return to home page
    Button(artistFrame, text = "logout", command=lambda: [clearFrame(artistFrame), reset(), home()]).grid(row=5, column=0, pady=(20,0))

# creates a page that contains all the actions a user can take on the app
def userPage():
    global window
    # create variable to store the keywords the user might look for
    keywords = "" 
    #create page
    userFrame = Frame(window, borderwidth=0)
    userFrame.pack()
    # button to start the session
    Button(userFrame, text = "start session", fg='white', bg='green').grid(row=0, column=0)
    # message to indicate where to enter keywords and the button to search
    Label(userFrame, text = "enter song/playlist").grid(row=2, column=0, pady=(20,0))
    Entry(userFrame, textvariable = keywords).grid(row=3, column=0)
    Button(userFrame, text = "search for songs or playlists").grid(row=4, column=0)
    # messge to enter keywords to search for artist
    Label(userFrame, text = "enter artist name").grid(row=6, column=0, pady=(20,0))
    Entry(userFrame, textvariable = keywords).grid(row=7, column=0)
    Button(userFrame, text = "search for artists").grid(row=8, column=0)
    # button to end the session
    Button(userFrame, text = "end session", fg='white', bg='red').grid(row=10, column=0, pady=(20,0))
    # button to logout
    Button(userFrame, text = "logout", command=lambda: [clearFrame(userFrame), home()]).grid(row=11, column=0, pady=(20,0))
    
# creates a page to ask the user if they want to login as a user or an artist
def choose():
    global window
    # create page
    chooseFrame = Frame(window)
    chooseFrame.pack()
    # message and buttons to choose from
    Label(chooseFrame, text="would you like to login as a user or an artist").grid(row=0, column = 0)
    Button(chooseFrame, text = "artist", command=lambda: [clearFrame(chooseFrame), artistValidate()]).grid(row=1, column=0)
    Button(chooseFrame, text = "user", command=lambda: [clearFrame(chooseFrame), userValidate()]).grid(row=2, column=0)

# connect to the database
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return

# verifies if the password is correct for the user
def userValidate():
    global id, ps, connection, cursor
    cursor.execute('''SELECT 'True'
                    FROM users
                    WHERE uid = ? AND pwd = ?;''', (id,ps),)
    val = cursor.fetchone()
    if not val:
        wrongPass()
    else :
        userPage()
    
# verifies if the password is correct for an artist
def artistValidate():
    global id, ps, connection, cursor
    cursor.execute('''SELECT 'True'
                    FROM artists
                    WHERE aid = ? AND pwd = ?;''', (id, ps),)
    val = cursor.fetchone()
    if not val:
        wrongPass()
    else :
        artistPage()
    
# checks if the id exist and waht kind of id it is
def idValidate():
    global connection, cursor, id
    cursor.execute(f'''SELECT u.uid, 'both' FROM users u, artists a
                    WHERE u.uid = a.aid AND u.uid = {id}
                    UNION
                    SELECT u.uid, 'user' FROM users u
                    WHERE u.uid = {id} AND u.uid NOT IN(SELECT u.uid FROM users u, artists a
                                                         WHERE u.uid = a.aid AND u.uid = {id})
                    UNION 
                    SELECT a.aid, 'artist' FROM artists a
                    WHERE a.aid = {id} AND a.aid NOT IN(SELECT u.uid FROM users u, artists a
                                                         WHERE u.uid = a.aid AND u.uid = {id});''')
    idType = cursor.fetchone()
    if not idType:
        notInList()
    elif idType[1] == 'both':
        choose()
    elif idType[1] == 'user':
        userValidate()
    elif idType[1] == 'artist':
        artistValidate()
    
# creates the home page of the app
def home():
    
    global window
    homeFrame = Frame(window)
    homeFrame.pack()
    
    # initiate variables to save the values of password and ID
    username = tkinter.StringVar()
    password = tkinter.StringVar()

    
    #create the username input box 
    Label(homeFrame, text = "ID").grid(row=0, column=0)
    Entry(homeFrame, textvariable = username).grid(row=0, column=1)
    
    #creating the password input box 
    Label(homeFrame, text = "Password").grid(row=1, column=0)
    # make sure the password appears as * to the user
    Entry(homeFrame, textvariable = password, show="*").grid(row=1, column=1)
    
    #creating the login button to press after having written the user ID and the password
    Button(homeFrame, text = "login", command=lambda: [setGlobals(username, password), clearFrame(homeFrame), idValidate()]).grid(row=4, column=0)
    Button(homeFrame, text = "Register", command=lambda: [setGlobals(username, password), clearFrame(homeFrame), idValidate()]).grid(row=5, column=0)
    window.mainloop()
    return

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
    home()
    
if __name__ == "__main__":
    main()
