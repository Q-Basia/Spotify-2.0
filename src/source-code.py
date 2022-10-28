# This will be our source code
import sqlite3
import tkinter 
from tkinter import *
import sys # used to access the command line arguments
#from tkinter import simpledialog

# For keywords-search in the database:
keywords = None

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
    
    
#add error when th id is longer than 4 characters
def registerPage():
    global window, connection, cursor, id, ps
    regFrame = Frame(window)
    regFrame.pack()
    
    def newId(i, p1, p2, n):
        cursor.execute(f"SELECT uid FROM users WHERE uid = '{i}';")
        inside = cursor.fetchone()
        if not i or not p1 or not p2 or not n:
            tooLong.grid_remove()
            noMatch.grid_remove()
            inUse.grid_remove()
            enterAll.grid(row=7, column =0)
        elif len(i) > 4:
            enterAll.grid_remove()
            enterAll.grid_remove()
            noMatch.grid_remove()
            tooLong.grid(row=7, column = 0)
        elif inside:
            tooLong.grid_remove()
            enterAll.grid_remove()
            noMatch.grid_remove()
            inUse.grid(row=7, column =0)
        elif p1 != p2:
            tooLong.grid_remove()
            enterAll.grid_remove()
            inUse.grid_remove()
            noMatch.grid(row=7, column =0)
        else:
            tooLong.grid_remove()
            noMatch.grid_remove()
            enterAll.grid_remove()
            inUse.grid_remove()
            values = [i, n, p1]
            cursor.execute("INSERT INTO users VALUES (?, ?, ?);", values)
            connection.commit()
            clearFrame(regFrame)
            userPage()
    
    # initiate variables to save the values of password and ID
    new_id = tkinter.StringVar()
    new_ps = tkinter.StringVar()
    new_ps2 = tkinter.StringVar()
    new_name = tkinter.StringVar()

    #create the id input box 
    Label(regFrame, text = "ID").grid(row=0, column=0)
    Entry(regFrame, textvariable = new_id).grid(row=0, column=1)
    
    #creating the password input box 
    Label(regFrame, text = "Password").grid(row=1, column=0)
    Entry(regFrame, textvariable = new_ps, show="*").grid(row=1, column=1)
    
    Label(regFrame, text = "Confirm password").grid(row=2, column=0)
    Entry(regFrame, textvariable = new_ps2, show="*").grid(row=2, column=1)
    
    Label(regFrame, text = "Name").grid(row=3, column=0)
    Entry(regFrame, textvariable = new_name).grid(row=3, column=1)
    
    noMatch = Label(regFrame, text = "passwords do not match, please try again", fg ='red')
    inUse = Label(regFrame, text="This id is already in use, please try another one", fg ='red')
    enterAll = Label(regFrame, text="Please enter a value for all available fields", fg='red')
    tooLong = Label(regFrame, text="ID cannot have more than have 4 characters, try another one", fg='red')
    Button(regFrame, text = "Register", command=lambda: [newId(new_id.get(), new_ps.get(), new_ps2.get(), new_name.get())]).grid(row=5, column=0)
    Button(regFrame, text = "Home", command=lambda: [clearFrame(regFrame), home()]).grid(row=6, column=0)

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
    Button(artistFrame, text = "EXIT", command=lambda: [reset(), window.destroy()]).grid(row=6, column=0, pady=(20,0))

# creates a page that contains all the actions a user can take on the app
def userPage():
    global window

    # Variable used to store the keywords
    musicKeywords = tkinter.StringVar()
    artistKeywords = tkinter.StringVar()

    #create page
    userFrame = Frame(window, borderwidth=0)
    userFrame.pack()
    # button to start the session
    Button(userFrame, text = "start session", fg='white', bg='green').grid(row=0, column=0)
    # message to indicate where to enter keywords and the button to search
    Label(userFrame, text = "enter song/playlist").grid(row=2, column=0, pady=(20,0))
    # We store the keywords in a string variable
    Entry(userFrame, textvariable = musicKeywords).grid(row=3, column=0)
    # Button to search songs/playlists with keywords
    Button(userFrame, text = "search for songs or playlists", command=lambda:[clearFrame(userFrame), displaySongsPlaylist(searchSongsAndPlaylists(musicKeywords.get().split()),0)]).grid(row=4, column=0)
    
    # messge to enter keywords to search for artist
    Label(userFrame, text = "enter artist name").grid(row=6, column=0, pady=(20,0))
    # We store the keywords in a string variable
    Entry(userFrame, textvariable = artistKeywords).grid(row=7, column=0)
    # Button to search artists with the keywords
    Button(userFrame, text = "search for artists", command=lambda:[clearFrame(userFrame), displayArtists(searchArtists(artistKeywords.get().split()),0)]).grid(row=8, column=0)
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
    Button(chooseFrame, text = "artist", command=lambda: [clearFrame(chooseFrame), login("artist")]).grid(row=1, column=0)
    Button(chooseFrame, text = "user", command=lambda: [clearFrame(chooseFrame), login("user")]).grid(row=2, column=0)
    Button(chooseFrame, text = "Back", command=lambda: [clearFrame(chooseFrame), home()]).grid(row=3, column=0)
    
def login(type):
    global window
    loginFrame = Frame(window)
    loginFrame.pack()
    # initiate variables to save the values of password and ID
    userID = tkinter.StringVar()
    password = tkinter.StringVar()

    
    #create the username input box
    if type == "user":
        Label(loginFrame, text = "user ID").grid(row=0, column=0)
    else:
        Label(loginFrame, text = "artist ID").grid(row=0, column=0)
    Entry(loginFrame, textvariable = userID).grid(row=0, column=1)
    
    #creating the password input box 
    Label(loginFrame, text = "Password").grid(row=1, column=0)
    # make sure the password appears as * to the user
    Entry(loginFrame, textvariable = password, show="*").grid(row=1, column=1)
    
    Button(loginFrame, text = "login", command=lambda: [setGlobals(userID, password), clearFrame(loginFrame), idValidate(type)]).grid(row=4, column=0)
    
    Button(loginFrame, text = "Back", command=lambda: [clearFrame(loginFrame), choose()]).grid(row=6, column=0)

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
def idValidate(type):
    global connection, cursor, id
    if type == "user":
        cursor.execute(f'''SELECT u.uid FROM users u
                    WHERE u.uid = '{id}'; ''')
        idType = cursor.fetchone()
        if not idType:
            notInList()
        else:
            userValidate()
    elif type == "artist":
        cursor.execute(f'''SELECT a.aid FROM artists a
                    WHERE a.aid = '{id}';''')
        idType = cursor.fetchone()
        if not idType:
            notInList()
        else: 
            artistValidate()
    
# creates the home page of the app
def home():
    global window
    homeFrame = Frame(window)
    homeFrame.pack()
    
    #creating the login button to press after having written the user ID and the password
    Button(homeFrame, text = "sign-in", command=lambda: [clearFrame(homeFrame), choose()]).grid(row=4, column=0)
    Button(homeFrame, text = "sign-up", command=lambda: [clearFrame(homeFrame), registerPage()]).grid(row=5, column=0)
    Button(homeFrame, text="EXIT", bg='red', fg='white', command=lambda: window.destroy()).grid(row=6, column=0, pady=30)
    window.mainloop()
    return

def searchSongsAndPlaylists(currentKeywords):
    # Arguments: 
    #   currentKeywords: an array of string containing the keywords of the search
    # Returns:
    #   result: a sorted list of tuples
   
    # Update the keywords for the countKeywords function
    global keywords
    keywords = currentKeywords

    # Initialize the function that will calculate the keywords in sql
    connection.create_function('countKeywords', 1, countKeywords )
    # Create the list of tuples that we will return and contains all the songs and playlists
    result = []

    # Find matching songs
    cursor.execute('''
    SELECT sid, title, duration, countKeywords(title)
    FROM songs s
    WHERE countKeywords(title) > 0
    ORDER BY countKeywords(title) desc;
    ''')

    # Store all matching songs in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Songs",row[0],row[1], row[2], row[3]))

    # Find matching playlists 
    cursor.execute('''
    SELECT p.pid, p.title, SUM(s.duration), countKeywords(p.title)
    FROM playlists p
    LEFT OUTER JOIN plinclude pl USING(pid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(p.title) > 0
    GROUP BY p.pid, p.title
    ORDER BY countKeywords(p.title) desc;
    ''')

    # Store all matching playlists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Playlist",row[0],row[1], row[2], row[3]))

    # Order them from highest number of keywords to lowest
    result.sort(key=musicTupleGetKeyWord,reverse=True)

    # Return all of the matching songs and playlists
    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    return result

# Small function to return the number of keywords from a tuple of result
def musicTupleGetKeyWord(tuple):
    return tuple[4]    

def searchArtists(currentKeywords):
    # Arguments: 
    #   currentKeywords: an array of string containing the keywords of the search
    # Returns:
    #   result: a sorted list of tuples
   
    # Update the keywords for the countKeywords function
    global keywords
    keywords = currentKeywords

    # Initialize the function that will calculate the keywords in sql
    connection.create_function('countKeywords', 1, countKeywords )
    # Create the list of tuples that we will return and contains all the artists
    result = []

    # Find matching artists
    cursor.execute('''
    SELECT a.name, a.nationality, COUNT(s.sid), countKeywords(title)
    FROM artists a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(a.name) > 0
    GROUP BY a.name, a.nationality
    ''')

    # Store all matching artists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Artist",row[0],row[1], row[2], row[3]))

    # Find matching songs of artists
    cursor.execute('''
    SELECT a.name, a.nationality, COUNT(s.sid), countKeywords(title)
    FROM artists a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(s.title) > 0
    GROUP BY a.name, a.nationality
    ''')

    # Store all matching artists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Artist",row[0],row[1], row[2], row[3]))

    # Order them from highest number of keywords to lowest
    result.sort(key=artistTupleGetKeyWord,reverse=True)

    # We return the result
    # Format of each entry of result: (Type, Name, Nationality, Number of songs, Number of Keywords)
    return result

def artistTupleGetKeyWord(tuple):
    return tuple[4]  

def countKeywords(title):
    # Arguments:
    #   title: A string indicating the title of a song
    #   keywords: an array of strings containing the keywords of a search
    # Returns:
    #   count: number of keywords in the title

    # Testing Purpose [DELETE]
    global keywords

    count = 0 # number of keywords

    # For each keyword, we check if it appears in the title
    # Note: the comparison is not case-sensitive
    for keyword in keywords:
        for word in title.split():
            if(keyword.lower() == word.lower()):
                count += 1

    # return how many keywords were in title
    return count


def songsOfArtist(artist):
    # Arguments:
    #   artist: A string indicating the aid of the artist
    # Returns:
    #   songs: An array of tuples containing all the songs of artist and its information

    songs = []

    # Get the songs and their information with SQL
    cursor.execute('''
    SELECT s.sid, s.title, s.duration
    FROM artist a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    ''')

    # Store all the songs of the artist in the array songs
    rows = cursor.fetchall()
    for row in rows:
        songs.append(("Songs",row[0],row[1], row[2], row[3]))  

    return songs

def songsOfPlaylist(playlist):
    # Arguments:
    #   playlist: A string indicating the pid of the playlist
    # Returns:
    #   songs: An array of tuples containing all the songs of playlist and its information

    songs = []

    # Get the songs and their information with SQL
    cursor.execute('''
    SELECT s.sid, s.title, s.duration
    FROM playlist p
    LEFT OUTER JOIN plinclude pl USING(pid)
    LEFT OUTER JOIN songs s USING(sid)
    ''')

    # Store all the songs of the playlist in the array songs
    rows = cursor.fetchall()
    for row in rows:
        songs.append(("Songs",row[0],row[1], row[2], row[3]))  

    return songs

def displaySongsPlaylist(musicArray, pageIndex):
    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    
    size = len(musicArray)
    # Can scroll through 5 playlist/songs each time

    # Our window
    global window

    #create display page
    displayFrame = Frame(window, borderwidth=0)
    displayFrame.pack()

    # button to return to user page
    Button(displayFrame, text = "Return", command=lambda: [clearFrame(displayFrame), userPage()]).grid(row=0, column=0, padx = 15)

    # Create the 5 slots for the 5 music
    if(0 <= pageIndex< size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex])).grid(row=1, column=1, pady = 4)
    if(0 <= pageIndex +1 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+1])).grid(row=2, column=1, pady = 4)
    if(0 <= pageIndex +2 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+2])).grid(row=3, column=1, pady = 4)
    if(0 <= pageIndex + 3 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+3])).grid(row=4, column=1, pady = 4)
    if(0 <= pageIndex + 4 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+4])).grid(row=5, column=1, pady = 4)
    
    # Scroll down button
    if(pageIndex + 5 < size):
        Button(displayFrame, text = "Scroll Down", command=lambda: [clearFrame(displayFrame),displaySongsPlaylist(musicArray,pageIndex+5)]).grid(row=6, column=1, pady = 15)
    # Scroll up button
    if(pageIndex - 5 >= 0):
        Button(displayFrame, text = "Scroll Up", command=lambda: [clearFrame(displayFrame),displaySongsPlaylist(musicArray,pageIndex-5)]).grid(row=0, column=1, pady = 15)

    # If size = 0, we indicate that no songs returned
    if(size == 0):
        Label(displayFrame, text = "No songs or playlist having those keywords!").grid(row=1, column=1)

def musicTupleToString(tuple):
    # Takes the tuple of an array of songs/playlist and transform it into a complete string 
    # Argument:
        # Tuple: the tuple of a song
    # Returns: The tuple as a single string 

    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    string = tuple[0] + " | " + str(tuple[1]) + " | " + tuple[2] + " | " + str(tuple[3])
    return string
    

def displayArtists(artistArray, pageIndex):
    # Format of each entry of artistArray: (Type, Name, Nationality, Number of songs, Number of Keywords)
    size = len(artistArray)
    # Can scroll through 5 playlist/songs each time
    print(artistArray)

    # Our window
    global window

    #create display page
    displayFrame = Frame(window, borderwidth=0)
    displayFrame.pack()

    # button to return to user page
    Button(displayFrame, text = "Return", command=lambda: [clearFrame(displayFrame), userPage()]).grid(row=0, column=0, padx = 15)

    # Create the 5 slots for the 5 music
    if(0 <= pageIndex< size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex])).grid(row=1, column=1, pady = 4)
    if(0 <= pageIndex +1 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+1])).grid(row=2, column=1, pady = 4)
    if(0 <= pageIndex +2 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+2])).grid(row=3, column=1, pady = 4)
    if(0 <= pageIndex + 3 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+3])).grid(row=4, column=1, pady = 4)
    if(0 <= pageIndex + 4 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+4])).grid(row=5, column=1, pady = 4)
    
    # Scroll down button
    if(pageIndex + 5 < size):
        Button(displayFrame, text = "Scroll Down", command=lambda: [clearFrame(displayFrame),displaySongsPlaylist(artistArray,pageIndex+5)]).grid(row=6, column=1, pady = 15)
    # Scroll up button
    if(pageIndex - 5 >= 0):
        Button(displayFrame, text = "Scroll Up", command=lambda: [clearFrame(displayFrame),displaySongsPlaylist(artistArray,pageIndex-5)]).grid(row=0, column=1, pady = 15)

    # If size = 0, we indicate that no songs returned
    if(size == 0):
        Label(displayFrame, text = "No songs or artists having those keywords!").grid(row=1, column=1)

def artistTupleToString(tuple):
    # Takes the tuple of an array of artist and transform it into a complete string 
    # Argument:
        # Tuple: the tuple of an artist
    # Returns: The tuple as a single string 

    # Format of each entry of artistArray: (Type, Name, Nationality, Number of songs, Number of Keywords)
    string = tuple[1] + " | " + tuple[2] + " | " + str(tuple[3]) 
    return string


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
