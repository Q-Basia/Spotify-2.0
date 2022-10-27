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
    Button(userFrame, text = "search for songs or playlists", command=lambda:[clearFrame(userFrame), displaySongsPlaylist(searchSongsAndPlaylists(musicKeywords.get().split()))]).grid(row=4, column=0)
    
    # messge to enter keywords to search for artist
    Label(userFrame, text = "enter artist name").grid(row=6, column=0, pady=(20,0))
    # We store the keywords in a string variable
    Entry(userFrame, textvariable = artistKeywords).grid(row=7, column=0)
    # Button to search artists with the keywords
    Button(userFrame, text = "search for artists", command=lambda:displayArtists(searchArtists(artistKeywords.split()))).grid(row=8, column=0)
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
    result.sort(key=tupleGetKeyWord,reverse=True)

    # Return all of the matching songs and playlists
    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    return result

# Small function to return the number of keywords from a tuple of result
def tupleGetKeyWord(tuple):
    return tuple[3]    

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
    WHERE countKeywords(a.title) > 0
    GROUP BY a.name, a.nationality
    ORDER BY countKeywords(a.title) DESC;
    ''')

    # Store all matching artists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Songs",row[0],row[1], row[2], row[3]))

    # We return the result
    # Format of each entry of result: (Name, Nationality, Number of songs, Number of Keywords)
    return result

def countKeywords(title):
    # Arguments:
    #   title: A string indicating the title of a song
    #   keywords: an array of strings containing the keywords of a search
    # Returns:
    #   count: number of keywords in the title

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

def displaySongsPlaylist(musicArray):
    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    
    pageIndex = 0
    print(musicArray)
    size = len(musicArray)
    # Can scroll through 5 playlist/songs each time

    # Our window
    global window

    #create display page
    displayFrame = Frame(window, borderwidth=0)
    displayFrame.pack()

    # button to return to user page
    Button(displayFrame, text = "Return", command=lambda: [clearFrame(displayFrame), userPage()]).grid(row=0, column=0)

    # Create the 5 slots for the 5 music
    if(size > 0):
        b1 = Button(displayFrame, text = musicTupleToString(musicArray[pageIndex])).grid(row=1, column=1)
    if(size > 1):
        b2 = Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+1])).grid(row=2, column=1)
    if(size > 2):
        b3 = Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+2])).grid(row=3, column=1)
    if(size> 3):
        b4 = Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+3])).grid(row=4, column=1)
    if(size > 4):
        b5 = Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+4])).grid(row=5, column=1)
    
    # Scroll down button
    Button(displayFrame, text = "Scroll Down", command=lambda: scrollDown()).grid(row=6, column=1)
    # Scroll up button
    Button(displayFrame, text = "Scroll Up", command=lambda: scrollUp()).grid(row=0, column=1)
   
    def scrollDown():
        print("Page index is: " + pageIndex)
        if(pageIndex != (size-size%5)):
            pageIndex = 5+pageIndex
            if(pageIndex < size):
                b1['text'] = musicTupleToString(musicArray[pageIndex])
            if(pageIndex +1 < size):
                b2['text'] = musicTupleToString(musicArray[pageIndex+1])
            if(pageIndex + 2< size):
                b3['text'] = musicTupleToString(musicArray[pageIndex+2])
            if(pageIndex + 3< size):
                b4['text'] = musicTupleToString(musicArray[pageIndex+3])
            if(pageIndex + 4 < size):
                b5['text'] = musicTupleToString(musicArray[pageIndex+4])

    def scrollUp():
        if(pageIndex != 0):
            pageIndex = pageIndex - 5
            if(pageIndex < size):
                b1['text'] = musicTupleToString(musicArray[pageIndex])
            if(pageIndex +1 < size):
                b2['text'] = musicTupleToString(musicArray[pageIndex+1])
            if(pageIndex + 2< size):
                b3['text'] = musicTupleToString(musicArray[pageIndex+2])
            if(pageIndex + 3< size):
                b4['text'] = musicTupleToString(musicArray[pageIndex+3])
            if(pageIndex + 4 < size):
                b5['text'] = musicTupleToString(musicArray[pageIndex+4])



def musicTupleToString(tuple):
    # Takes the tuple of an array of songs/playlist and transform it into a complete string 
    # Argument:
        # Tuple: the tuple of a song
    # Returns: The tuple as a single string 

    # Format of each entry of result: (Type, id, title, duration, number of keywords)
    string = tuple[0] + " | " + str(tuple[1]) + " | " + tuple[2] + " | " + str(tuple[3])
    return string
    

def displayArtists(artistArray):
    # Format of each entry of artistArray: (Name, Nationality, Number of songs, Number of Keywords)
    return 0


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
