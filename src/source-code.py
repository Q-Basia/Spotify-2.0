# This will be our source code
from ast import Delete, Pass
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
sno = 0
listening = False

# create the app window using 'Tk()', which is a function form tkinter
window = Tk()
window.configure(bg='gray')
# set the title of the window
window.title("Spotify 2.0") #title of the page
 
    # connect to the database
def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return      
    
# this function removes all widgets that were created for the specified page
# to leave space for a new page
#arguments:
#   frame: the page that we want to remove from the window
def clearFrame(frame):
    global window
    frame.forget()
        
def setID(i):
    global id
    id = i.get()
def setPs(p):
    global ps
    ps = p.get()
    
# resets the values of id and password to null
# called when a user logs out of the app
def reset():
    global id, ps, sno
    id = ""
    ps = ""
    sno = 0
    
    
#add error when th id is longer than 4 characters
def registerPage():
    global window, connection, cursor, id, ps
    regFrame = Frame(window, bg='gray')
    regFrame.pack()
    
    def newId(i, p1, p2, n):
        cursor.execute("SELECT uid FROM users WHERE uid = ?;",(i,))
        inside = cursor.fetchone()
        if not i or not p1 or not p2 or not n:
            tooLong.grid_remove()
            noMatch.grid_remove()
            inUse.grid_remove()
            enterAll.grid(row=7, columnspan=2)
        elif len(i) > 4:
            enterAll.grid_remove()
            enterAll.grid_remove()
            noMatch.grid_remove()
            tooLong.grid(row=7, columnspan=2)
        elif inside:
            tooLong.grid_remove()
            enterAll.grid_remove()
            noMatch.grid_remove()
            inUse.grid(row=7, columnspan=2)
        elif p1 != p2:
            tooLong.grid_remove()
            enterAll.grid_remove()
            inUse.grid_remove()
            noMatch.grid(row=7, columnspan=2)
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
    Label(regFrame, text = "user ID", font=('Arial',15), bg='gray').grid(row=0, column=0)
    Entry(regFrame, textvariable = new_id, font=('Arial',15), fg='green').grid(row=0, column=1)
    
    #creating the password input box 
    Label(regFrame, text = "Password", font=('Arial',15), bg='gray').grid(row=1, column=0)
    Entry(regFrame, textvariable = new_ps, show="*", font=('Arial',15), fg='green').grid(row=1, column=1)
    
    Label(regFrame, text = "Confirm password", font=('Arial',15), bg='gray').grid(row=2, column=0)
    Entry(regFrame, textvariable = new_ps2, show="*", font=('Arial',15), fg='green').grid(row=2, column=1)
    
    Label(regFrame, text = "Name", font=('Arial',15), bg='gray').grid(row=3, column=0)
    Entry(regFrame, textvariable = new_name, font=('Arial',15), fg='green').grid(row=3, column=1)
    
    noMatch = Label(regFrame, text = "passwords do not match, please try again", font=('Arial',15), fg ='red', bg='gray')
    inUse = Label(regFrame, text="This id is already in use, please try another one", fg ='red', font=('Arial',15), bg='gray')
    enterAll = Label(regFrame, text="Please enter a value for all available fields", fg='red', font=('Arial',15), bg='gray')
    tooLong = Label(regFrame, text="ID cannot have more than have 4 characters, try another one", fg='red', font=('Arial',15), bg='gray')
    Button(regFrame, text = "Register", bg='gray', fg='turquoise', command=lambda: [newId(new_id.get(), new_ps.get(), new_ps2.get(), new_name.get())], font=('Arial',15)).grid(row=5, columnspan=2)
    Button(regFrame, text = "Home", bg='gray', fg='red', command=lambda: [clearFrame(regFrame), home()], font=('Arial',15)).grid(row=6, columnspan=2)

# creates a page that will display all actions for an artist
# no argument or return value
def artistPage():
    global window 
        
    # create page
    artistFrame = Frame(window)
    artistFrame.pack()
    
    # buttons to add the song, find top users and top playlists, logout and exit the program
    Button(artistFrame, text = "New song", font=('Arial',15), command=lambda: [clearFrame(artistFrame), addnewSong()]).grid(row=2, column=0, pady=(0,20))
    Button(artistFrame, text = "Find Top 3's", font=('Arial',15), command=lambda: [clearFrame(artistFrame), findTop()]).grid(row=3, column=0)
    Button(artistFrame, text = "Logout", font=('Arial',15), command=lambda: [clearFrame(artistFrame), reset(), home()]).grid(row=5, column=0, pady=(20,0))
    Button(artistFrame, text = "EXIT", font=('Arial',15), command=lambda: [reset(), window.destroy()]).grid(row=6, column=0, pady=(20,0))

# creates a page that contains all the actions a user can take on the app
def userPage():
    global window, listening, sno, id
    # Variable used to store the keywords
    musicKeywords = tkinter.StringVar()
    artistKeywords = tkinter.StringVar()   
    
    #cursor.execute()
    #create page
    userFrame = Frame(window, borderwidth=0)
    userFrame.pack()
    
    def startSession():
        global listening, connection, cursor, sno, id
        if listening == True:
            notListening.grid_remove()
            alreadyL.grid(row=1, column=0)
        else:
            notListening.grid_remove()
            alreadyL.grid_remove()
            listening = True 
            cursor.execute(f'''SELECT MAX(sno) FROM sessions WHERE uid = '{id}';''')
            top_sno = cursor.fetchone()
            if not top_sno[0]:
                sno = 1
            else:
                sno = top_sno[0] + 1
            cursor.execute(f'''INSERT INTO sessions VALUES ('{id}', {sno}, date(), null);''')
            connection.commit()
            
    def endSession():
        global listening, connection, cursor, sno, id
        if listening == False:
            alreadyL.grid_remove()
            notListening.grid(row=9, column = 0)
        else:
            notListening.grid_remove()
            alreadyL.grid_remove()
            listening = False
            cursor.execute(f'''UPDATE sessions SET end = date() WHERE uid = '{id}' AND sno = {sno};''')
            connection.commit()
            
    # initiate error labels
    alreadyL = Label(userFrame, text = "you are already in a listening session", font=('Arial',15), fg='red')
    notListening = Label(userFrame, text="you are not currently in a listening session", font=('Arial',15), fg='red')
        
    # button to start the session
    Button(userFrame, text = "start session", fg='white', bg='green', command=lambda: startSession(), font=('Arial',15)).grid(row=0, column=0)
    # message to indicate where to enter keywords and the button to search
    Label(userFrame, text = "enter song/playlist", font=('Arial',15)).grid(row=2, column=0, pady=(20,0))
     # We store the keywords in a string variable
    Entry(userFrame, textvariable = musicKeywords).grid(row=3, column=0)
    # Button to search songs/playlists with keywords
    Button(userFrame, text = "search for songs or playlists", command=lambda:[clearFrame(userFrame), displaySongsPlaylist(searchSongsAndPlaylists(musicKeywords.get().split()),0)]).grid(row=4, column=0)
    
    # message to enter keywords to search for artist
    Label(userFrame, text = "enter artist name").grid(row=6, column=0, pady=(20,0))
    # We store the keywords in a string variable
    Entry(userFrame, textvariable = artistKeywords).grid(row=7, column=0)
    # Button to search artists with the keywords
    Button(userFrame, text = "search for artists", command=lambda:[clearFrame(userFrame), displayArtists(searchArtists(artistKeywords.get().split()),0)]).grid(row=8, column=0)
    # button to end the session
    Button(userFrame, text = "end session", fg='white', bg='red', command=lambda: endSession(), font=('Arial',15)).grid(row=10, column=0, pady=(20,0))
    # button to logout
    Button(userFrame, text = "logout", command=lambda: [endSession(), clearFrame(userFrame), home()], font=('Arial',15)).grid(row=11, column=0, pady=(20,0))
    Button(userFrame, text = "EXIT", font=('Arial',15), command=lambda: [endSession(), reset(), window.destroy()]).grid(row=12, column=0, pady=(20,0))

def choose():
    global window
    chooseF = Frame(window, bg='gray')
    chooseF.pack()
    Label(chooseF, text = "would you to to login as a user or an artist", bg='gray',font=('Arial',15)).grid(row=3)
    Button(chooseF, text = "artist", command=lambda: [clearFrame(chooseF), Validate("artist")], bg='gray', font=('Arial',15)).grid(row=5)
    Button(chooseF, text = "user", bg='gray',command=lambda:[clearFrame(chooseF), Validate("user")], font=('Arial',15)).grid(row=4)
    Button(chooseF, text="back", fg='red', bg='gray',command=lambda: [clearFrame(chooseF), home()], font=('Arial',15)).grid(row=6)
    
def Validate(u):
    global window, id, ps
    passP = Frame(window)
    passP.pack()
    new_ps = tkinter.StringVar()
    Label(passP, text="enter your password below", font=('Arial',15)).grid(row=1, columnspan=3)
    wP = Label(passP, text="Password is incorrect, please try again", fg='red')
    Label(passP, text = "password", font=('Arial',15)).grid(row=2, column=0)
    Entry(passP, textvariable=new_ps, show="*", font=('Arial',15)).grid(row=2, column=1)
    Button(passP, text="login", command=lambda:[setPs(new_ps), test()], font=('Arial',15)).grid(row=3, column=0)
    Button(passP, text="back", command=lambda: [clearFrame(passP), choose()], font=('Arial',15)).grid(row=4, column=0)
    def test():
        if u == "artist":
            cursor.execute('''SELECT 'True'
                        FROM artists
                        WHERE aid = ? AND pwd = ?;''', (id, ps),)
            val = cursor.fetchone()
            if not val:
                wP.grid(row =0, column = 0)
            else :
                clearFrame(passP)
                artistPage()
        else:
            cursor.execute('''SELECT 'True'
                    FROM users
                    WHERE uid = ? AND pwd = ?;''', (id,ps),)
            val = cursor.fetchone()
            if not val:
                wP.grid(row =0, column = 0)
            else :
                clearFrame(passP)
                userPage() 
                        
     
def home():
    global window, connection, cursor, id, ps
    signinFrame = Frame(window, bg='gray')
    signinFrame.pack()
    signinBottom = Frame(window, bg='gray')
    signinBottom.pack(side =BOTTOM)
    Label(signinFrame, text="Log in", font=('Arial',15), bg='gray').pack()#.grid(row=0, columnspan=3)
    noID = Label(signinBottom, text = "ID does not match any account, please try again", font=('Arial',15), fg ='red', bg='gray')
    
    def notList():  
        noID.pack(side = TOP)
            
   

    def check():
        cursor.execute(f'''SELECT u.uid, 'both' FROM users u, artists a
                    WHERE u.uid = a.aid AND u.uid = '{id}'
                    UNION
                    SELECT u.uid, 'user' FROM users u
                    WHERE u.uid = '{id}' AND u.uid NOT IN(SELECT u.uid FROM users u, artists a
                                                         WHERE u.uid = a.aid AND u.uid = '{id}')
                    UNION 
                    SELECT a.aid, 'artist' FROM artists a
                    WHERE a.aid = '{id}' AND a.aid NOT IN(SELECT u.uid FROM users u, artists a
                                                         WHERE u.uid = a.aid AND u.uid = '{id}');''')
        idType = cursor.fetchone()
        if not idType:
            notList()
        elif idType[1] == 'both':
            clearFrame(signinFrame)
            clearFrame(signinBottom)
            choose()
        elif idType[1] == 'user':
            clearFrame(signinFrame)
            clearFrame(signinBottom)
            Validate("user")
        elif idType[1] == 'artist':
            clearFrame(signinFrame)
            clearFrame(signinBottom)
            Validate("artist")
        
    new_id = tkinter.StringVar()
    Label(signinFrame, text = "ID",font=('Arial',15), bg='gray').pack(side = LEFT)#.grid(row=1, column=0)
    Entry(signinFrame, textvariable = new_id, font=('Arial',15), fg='green').pack(side = LEFT)#.grid(row=1, column=1)   

    Button(signinBottom, text="exit", bg='gray', fg='red', command=lambda: window.destroy(), font=('Arial',15)).pack(side = BOTTOM)#.grid(row=6, column=0, pady=30)
    Button(signinBottom, text = "register", command=lambda: [clearFrame(signinFrame), clearFrame(signinBottom), registerPage()], font=('Arial',15), bg='gray').pack(side = BOTTOM)#.grid(row=4, column=0)
    Button(signinBottom, text = "next", command=lambda: [setID(new_id), check()], fg='turquoise', bg='gray', font=('Arial',15)).pack(side = BOTTOM)#.grid(row=3, column=0)
    
    window.mainloop()



def searchSongsAndPlaylists(currentKeywords):
    # Arguments: 
    #   currentKeywords: an array of string containing the keywords of the search
    # Returns:
    #   result: a sorted list of tuples
   
    global cursor

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
        result.append(("Song",row[0],row[1], row[2], row[3]))

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
    
    global cursor

    # Update the keywords for the countKeywords function
    global keywords
    keywords = currentKeywords

    # Initialize the function that will calculate the keywords in sql
    connection.create_function('countKeywords', 1, countKeywords )
    # Create the list of tuples that we will return and contains all the artists
    result = []

    # Find matching artists
    cursor.execute('''
    SELECT a.name, a.nationality, COUNT(s.sid), countKeywords(title), a.aid
    FROM artists a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(a.name) > 0
    GROUP BY a.name, a.nationality
    ''')

    # Store all matching artists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Artist",row[0],row[1], row[2], row[3], row[4]))

    # Find matching songs of artists
    cursor.execute('''
    SELECT a.name, a.nationality, COUNT(s.sid), countKeywords(title), a.aid
    FROM artists a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE countKeywords(s.title) > 0
    GROUP BY a.name, a.nationality
    ''')

    # Store all matching artists in the result
    rows = cursor.fetchall()
    for row in rows:
        result.append(("Artist",row[0],row[1], row[2], row[3], row[4]))

    # Order them from highest number of keywords to lowest
    result.sort(key=artistTupleGetKeyWord,reverse=True)

    # We return the result
    # Format of each entry of result: (Type, Name, Nationality, Number of songs, Number of Keywords, Artist ID)
    return result

# Small function to return the Number of Keyworsd from an artist tuple (for ordering purposes)
def artistTupleGetKeyWord(tuple):
    return tuple[4]  

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
        # If the title is empty (or only has whitespace), we simply say that it has the keyword
        if(not (title and title.strip())):
            count += 1
        elif(keyword.lower() in title.lower()):
            # Count number of times keyword appears in title
            count += title.lower().count(keyword.lower())

    # return how many keywords were in title
    return count


def displaySongsPlaylist(musicArray, pageIndex):
    # We display as buttons all of the playlist and songs that were passed, offering additional options for each type
    # Arguments: 
    #   musicArray: an array containing both playlist and song tuples

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
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex]), command = lambda: determineContent(musicArray[pageIndex], displayFrame)).grid(row=1, column=1, pady = 4)
    if(0 <= pageIndex +1 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+1]), command = lambda: determineContent(musicArray[pageIndex+1], displayFrame)).grid(row=2, column=1, pady = 4)
    if(0 <= pageIndex +2 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+2]), command = lambda: determineContent(musicArray[pageIndex+2], displayFrame)).grid(row=3, column=1, pady = 4)
    if(0 <= pageIndex + 3 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+3]), command = lambda: determineContent(musicArray[pageIndex+3], displayFrame)).grid(row=4, column=1, pady = 4)
    if(0 <= pageIndex + 4 < size):
        Button(displayFrame, text = musicTupleToString(musicArray[pageIndex+4]), command = lambda: determineContent(musicArray[pageIndex+4], displayFrame)).grid(row=5, column=1, pady = 4)
    
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
    # We display all of the artist tuples in the artist array as buttons, each allowing more options regarding the artist
        # Arguments: 
    #   artistArray: an array containing artist tuples

    # Format of each entry of artistArray: (Type, Name, Nationality, Number of songs, Number of Keywords, Artist ID)
    size = len(artistArray)
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
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex]), command = lambda: determineContent(artistArray[pageIndex], displayFrame)).grid(row=1, column=1, pady = 4)
    if(0 <= pageIndex +1 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+1]), command = lambda: determineContent(artistArray[pageIndex+1], displayFrame)).grid(row=2, column=1, pady = 4)
    if(0 <= pageIndex +2 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+2]), command = lambda: determineContent(artistArray[pageIndex+2], displayFrame)).grid(row=3, column=1, pady = 4)
    if(0 <= pageIndex + 3 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+3]), command = lambda: determineContent(artistArray[pageIndex+3], displayFrame)).grid(row=4, column=1, pady = 4)
    if(0 <= pageIndex + 4 < size):
        Button(displayFrame, text = artistTupleToString(artistArray[pageIndex+4]), command = lambda: determineContent(artistArray[pageIndex+4], displayFrame)).grid(row=5, column=1, pady = 4)
    
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

    # Format of each entry of artistArray: (Type, Name, Nationality, Number of songs, Number of Keywords, Artist ID)
    string = tuple[1] + " | " + tuple[2] + " | " + str(tuple[3]) 
    return string

def songsOfArtist(artist):
    # Get all songs of an artist
    # Arguments:
    #   artist: A string indicating the aid of the artist
    # Returns:
    #   songs: An array of tuples containing all the songs of artist and its information

    global cursor

    songs = []

    # Get the songs and their information with SQL
    cursor.execute('''
    SELECT s.sid, s.title, s.duration
    FROM artists a
    LEFT OUTER JOIN perform p USING(aid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE a.aid LIKE :num;
    ''', {"num":artist})

    # Store all the songs of the artist in the array songs
    rows = cursor.fetchall()
    for row in rows:
        songs.append(("Song",str(row[0]),row[1], str(row[2])))  

    return songs

def songsOfPlaylist(playlist):
    # Get all songs of a laylist
    # Arguments:
    #   playlist: A string indicating the pid of the playlist
    # Returns:
    #   songs: An array of tuples containing all the songs of playlist and its information
    global cursor

    songs = []
    # Get the songs and their information with SQL
    cursor.execute('''
    SELECT s.sid, s.title, s.duration
    FROM playlists p
    LEFT OUTER JOIN plinclude pl USING(pid)
    LEFT OUTER JOIN songs s USING(sid)
    WHERE p.pid = :num;
    ''', {"num":playlist})

    # Store all the songs of the playlist in the array songs
    rows = cursor.fetchall()
    for row in rows:
        songs.append(("Song",str(row[0]),row[1], str(row[2])))  

    return songs

def determineContent(tuple,frame):
    # We find out if the tuple is 1) a Song, 2) an Artist or 3) a Playlist
    # Then, we call the right function depending on which it is
    # Argument:
        # tuple: the tuple containing the information
    if(tuple[0] == "Song"):
        clearFrame(frame)
        # Display options for the song
        songMenu(tuple, frame)
    elif(tuple[0]== "Playlist"): 
        clearFrame(frame)
        # We display all songs of playlist
        displaySongs(songsOfPlaylist(tuple[1]), 0, frame)
    elif(tuple[0] == "Artist"):
        clearFrame(frame)
        # Display all songs of artist
        displaySongs(songsOfArtist(tuple[5]), 0, frame)


def displaySongs(songsArray, pageIndex, frame):
    # We display each song as a button, with 5 songs max per page (we can scroll up or down if there is more). Each button allow for more options regarding the song
    # Arguments:
        # songsArray: array containing all the song tuples
        # pageIndex: Indicates which page (of 5 songs) we are displaying in respect to the list of songs
        # frame: The frame on which we were on previously, before displaying all the songs

    size = len(songsArray)

    # Our window
    global window

    #create display page
    displayFrame = Frame(window, borderwidth=0)
    displayFrame.pack()

    # button to return to user page
    Button(displayFrame, text = "Return", command=lambda: [clearFrame(displayFrame), frame.pack()]).grid(row=0, column=0, padx = 15)

    # Create the 5 slots for the 5 songs
    if(0 <= pageIndex< size):
        song = songsArray[pageIndex]
        Button(displayFrame, text = song[1] + " | " + song[2] + " | " + song[3], command = lambda: songMenu(song,displayFrame)).grid(row=1, column=1, pady = 4)
    if(0 <= pageIndex +1 < size):
        song = songsArray[pageIndex+1]
        Button(displayFrame, text = song[1] + " | " + song[2] + " | " + song[3], command = lambda: songMenu(song,displayFrame)).grid(row=2, column=1, pady = 4)
    if(0 <= pageIndex +2 < size):
        song = songsArray[pageIndex+2]
        Button(displayFrame, text = song[1] + " | " + song[2] + " | " + song[3], command = lambda: songMenu(song,displayFrame)).grid(row=3, column=1, pady = 4)
    if(0 <= pageIndex + 3 < size):
        song = songsArray[pageIndex+3]
        Button(displayFrame, text = song[1] + " | " + song[2] + " | " + song[3], command = lambda: songMenu(song,displayFrame)).grid(row=4, column=1, pady = 4)
    if(0 <= pageIndex + 4 < size):
        song = songsArray[pageIndex+4]
        Button(displayFrame, text = song[1] + " | " + song[2] + " | " + song[3], command = lambda: songMenu(song,displayFrame)).grid(row=5, column=1, pady = 4)
    
    # Scroll down button
    if(pageIndex + 5 < size):
        Button(displayFrame, text = "Scroll Down", command=lambda: [clearFrame(displayFrame),displaySongs(songsArray,pageIndex+5, frame)]).grid(row=6, column=1, pady = 15)
    # Scroll up button
    if(pageIndex - 5 >= 0):
        Button(displayFrame, text = "Scroll Up", command=lambda: [clearFrame(displayFrame),displaySongs(songsArray,pageIndex-5, frame)]).grid(row=0, column=1, pady = 15)

    # If size = 0, we indicate that no songs returned
    if(size == 0):
        Label(displayFrame, text = "No songs to display!").grid(row=1, column=1)

def songMenu(song, frame):
    # We display the different options that we can with a song
    # Argument:
        # Song: song with which we want to interact
        # frame: the frame from which the song was called

    # Our window
    global window

    # remove precedent page
    clearFrame(frame)

    #create menu page
    MenuFrame = Frame(window, borderwidth=0)
    MenuFrame.pack()
    
    Button(MenuFrame, text = "Return", command=lambda: [clearFrame(MenuFrame), frame.pack()]).grid(row=0, column=0, padx = 15)

    Button(MenuFrame, text = "Listen to the Song", command=lambda: [listenToSong(song)]).grid(row=0, column=1, pady = 15)
    Button(MenuFrame, text = "More information about the Song", command=lambda: [clearFrame(MenuFrame), infoAboutSong(song,frame)]).grid(row=1, column=1, pady = 15)
    Button(MenuFrame, text = "Add the Song to a playlist", command=lambda: [clearFrame(MenuFrame), addSongToPlaylist(song,frame)]).grid(row=2, column=1, pady = 15)

def listenToSong(song):
    # We store it in our database when a user listens to a song (what time, which song)
    # Argument:
        # song: the song tuple the user wants to listen to

    # Our window
    global window

    # Check if a listening session has been started.
    # If yes; continue. If not, start a session
    global listening, connection, cursor, sno, id
    if listening == False:
        listening = True 
        cursor.execute('''SELECT MAX(sno) FROM sessions WHERE uid = :num;''', {"num": id})
        top_sno = cursor.fetchone()
        if not top_sno[0]:
            sno = 1
        else:
            sno = top_sno[0] + 1
        cursor.execute('''INSERT INTO sessions VALUES (:id, :sno, date(), null);''', {"id":id, "sno": sno})
        connection.commit()

    # Check if the song was previously listened by user in the same session
    # (Find it in listen table)
    # If not, create a new row. If yes, augment count by 1
    cursor.execute('''
    SELECT cnt from listen WHERE uid = :uid AND sno = :sno AND sid = :sid
    ''', {"uid": id, "sno": sno, "sid": song[1]})

    songCount = cursor.fetchone()
    if(songCount == None):
            cursor.execute(''' 
            INSERT INTO listen VALUES (:uid, :sno, :sid, 1);
            ''', {"uid": id, "sno": sno, "sid": song[1]})
    else:
        cursor.execute('''
        UPDATE listen
        SET count = count + 1
        WHERE uid = :uid AND sno = :sno AND sid = :sid
        ''', {"uid": id, "sno": sno, "sid": song[1]})
    
    # Save result in DB
    connection.commit()

def infoAboutSong(song,frame):
    # Gives more info about a song that the user selected
    # Arguments:
        # song: the song tuple on which we want more information
        # frame: the frame on which we were on previously

    # Our window
    global window
    global cursor

    # Format of song: (Type, id, title, duration, number of keywords)

    #create menu page
    infoFrame = Frame(window, borderwidth=0)
    infoFrame.pack()
    
    # Return to the different options for the song
    Button(infoFrame, text = "Return", command=lambda: [clearFrame(infoFrame), songMenu(song,frame)]).grid(row=0, column=0, padx = 15)

    # Get following info about the song: artists, id, title, duration, name of playlists it appears in
    
    # Get artists names
    cursor.execute('''
    SELECT a.name
    FROM songs s
    LEFT OUTER JOIN perform p USING(sid)
    LEFT OUTER JOIN artists a USING(aid)
    WHERE s.sid LIKE :num;
    ''', {"num":song[1]})

    artistRows = cursor.fetchall()

    artistString = ""
    if(cursor.rowcount == 0): artistString = "No Artists"
    else:
        artistString += "Artists:\n"
        for row in artistRows:
            artistString += row[0] + ", "
        artistString = artistString[:-2]

    # Get all playlists names
    cursor.execute('''
    SELECT p.title
    FROM songs s
    LEFT OUTER JOIN plinclude pl USING(sid)
    LEFT OUTER JOIN playlists p USING(pid)
    WHERE s.sid LIKE :num;
    ''', {"num":song[1]})

    playlistRows = cursor.fetchall()

    playlistString = ""
    if(cursor.rowcount == 0): playlistString = "No Playlists"
    else:
        playlistString += "Playlists:\n"
        for row in playlistRows:
            playlistString += row[0] + ", "
        playlistString = playlistString[:-2]

    # Display information

    # Display artists
    Label(infoFrame, text = artistString).grid(row=2, column=1)

    # Display id, title & duration
    Label(infoFrame, text = "Id:\n" + str(song[1])).grid(row=3, column=1)
    Label(infoFrame, text = "Title:\n" + song[2]).grid(row=4, column=1)
    Label(infoFrame, text = "Duration:\n" + str(song[3]) + " seconds").grid(row=5, column=1)

    # Display playlists
    Label(infoFrame, text = playlistString).grid(row=6, column=1)

def addSongToPlaylist(song,frame):
    # A user selects a song and adds it to a playlist of their choice
    # Arguments:
        # song:  the song the user wants to add to a playlist
        # frame: the frame we were on previously, before wanting to add a playlist
        
    # Our window
    global window 
    # ID of user
    global id
    # To access SQL
    global cursor
    global connection

    #create menu page
    addFrame = Frame(window, borderwidth=0)
    addFrame.pack()

    # Variable to store new playlist name
    playlistName = tkinter.StringVar()

    # Return to the different options for the song
    Button(addFrame, text = "Return", command=lambda: [clearFrame(addFrame), songMenu(song,frame)]).grid(row=0, column=0, padx = 15)


    # Can choose to add to own playlist
    buttonIndex = 0 # keep count of all buttons
    # Find user's playlists
    cursor.execute('''
    SELECT p.pid, p.title
    FROM users u
    LEFT OUTER JOIN playlists p USING(uid)
    WHERE u.uid = :uid;
    ''', {"uid": id})

    playlistRows = cursor.fetchall()

    # We verify that there is at least one playlist assigned to the user, then create a button for each playlist
    if(playlistRows[0][0] != None):
        Label(addFrame, text = "Add to existing playlist:").grid(row=0, column=1)
        for pRow in playlistRows:
            print(pRow[0])
            Button(addFrame, text = pRow[1], command = lambda pRow = pRow: [insertSongIntoPlaylist(song, pRow[0])] ).grid(row=1+buttonIndex, column =1)
            buttonIndex += 1

    # Let user create new playlist if they want
    
    Label(addFrame, text = "Add to new playlist:").grid(row=1 +buttonIndex, column=1) #prompt
    Entry(addFrame, textvariable = playlistName).grid(row= 2 +buttonIndex, column=1)
    Button(addFrame, text = "Add", command = lambda: [insertSongIntoNewPlaylist()]).grid(row= 2 +buttonIndex, column=2)

    def insertSongIntoNewPlaylist():
        # to insert a song into a new playlist

        name = playlistName.get()
        # If an empty string, we don't consider it as an acceptable name
        if(name == ""): Label(addFrame, text = "Not an accepted name for the new playlist", fg='red').grid(row= 3 +buttonIndex, column=1)
        else:
            # Get maximum pid
            cursor.execute("SELECT MAX(p.pid) FROM playlists p")
            maxPid = cursor.fetchone()[0]+1
            # Insert in two necessary tables
            cursor.execute("INSERT INTO playlists VALUES (:pid, :title, :uid) ", {"pid": maxPid, "title": name, "uid": id})
            cursor.execute("INSERT INTO plinclude VALUES (:pid, :sid, 1)", {"pid": maxPid, "sid": song[1]})
            
            connection.commit()


def insertSongIntoPlaylist(song, playlist):
    # We add a song into an already existing playlist
    # Arguments:
        # song: song tuple that we want to add to a playlist
        # playlist: playlist id to whom we want to add a song

    global cursor
    global connection

    # Get next "sorder" of playlist
    cursor.execute("SELECT MAX(pl.sorder) FROM plinclude pl WHERE pl.pid = :pid", {"pid": playlist})
    order = cursor.fetchone()[0] + 1

    # Verify that this song was not inserted before
    cursor.execute("SELECT pl.sid FROM plinclude pl WHERE pl.pid = :pid AND pl.sid = :sid", {"pid": playlist, "sid": song[1]})
    if(cursor.fetchone() == None):
        cursor.execute("INSERT INTO plinclude VALUES (:pid, :sid, :sorder)", {"pid": playlist, "sid": song[1], "sorder": order})
    else:
        print("Already in playlist!")

    # Save to DB
    connection.commit() 
    
def addnewSong():
    global window, connection
    new = Frame(window)
    new.pack()

    new_song = tkinter.StringVar()

    # label to tell the artist where to enter values of new song
    Label(new, text="Please enter name and duration of song in seconds, seperated by a comma", font=('Arial',15)).grid(row=0, column=0)
    # input box for the song details, must be name followed by suration
    Entry(new, textvariable = new_song, font=('Arial',15)).grid(row=1, column=0)
    Button(new,text="Add Song", font = ('Arial',15), command=lambda:[clearFrame(new), addSong(new_song)]).grid(row=2, column=0)
    Button(new, text="Back", fg='red', bg='gray',command=lambda: [clearFrame(new), artistPage()], font=('Arial',15)).grid(row=6)

######
# If not, the song should be added with a unique id (assigned by your system) and any additional artist who may have 
# performed the song with their ids obtained from input
def addSong(new_song):
    global window
    global connection

    song = new_song.get().split(",")
    name = song[0]
    dur = song[1]
    cursor.execute(f"SELECT title FROM songs WHERE title = '{name}' AND duration = '{dur}';")
    row = cursor.fetchone()
    
    if not row:
        cursor.execute("SELECT max(sid) FROM songs;")
        s_idrow = cursor.fetchone()
        s_id = s_idrow[0] + 1
        values = [s_id, name, dur]
        cursor.execute("INSERT INTO songs VALUES (?, ?, ?);", values)
        connection.commit()
    
        #create the page
        er = Frame(window)
        er.pack()


        # message to enter keywords to search for artist
        Label(er, text = "Enter the artists that performed the song", font=('Arial',15)).grid(row=2, column=0, pady=(20,0))

        performers = tkinter.StringVar()
        # We store the keywords in a string variable
        Entry(er, textvariable = performers, font=('Arial',15)).grid(row=3, column=0)
        Button(er, text="Add Artist(s)", command=lambda: [clearFrame(er), addArtistPerform(performers, s_id)]).grid(row = 4, column = 0)        
    else:
        songExist()


def addArtistPerform(performs, s_id):
    global window, connection, cursor, id

    first_value = [id, s_id]
    cursor.execute("INSERT INTO perform VALUES (?, ?);", first_value)
    connection.commit()

    performers = performs.get().split(",")
    
    for artist in performers:
        values = [artist, s_id]

        if (artist == ""):
            Pass
        else:
            cursor.execute(f"INSERT INTO perform VALUES (?, ?);", values)
            connection.commit()

    connPerformer = Frame(window)
    connPerformer.pack()

    # create a label to display the message
    Label(connPerformer, text = "Song has been added", fg ='green', font=('Arial',15)).grid(row = 0, column = 0)

    # create a button to return to the home page
    Button(connPerformer, text="Return", command=lambda: [clearFrame(connPerformer), artistPage()]).grid(row = 1, column= 0)

def songExist():
    global window
    
    #create the page
    er = Frame(window)
    er.pack()
    
    # create a label to display the message
    Label(er, font=('Arial',15), text = "Song already exists", fg ='red').grid(row = 0, column = 0)
    
    # create a button to return to the home page
    Button(er, text="return", font=('Arial',15), command=lambda: [clearFrame(er), artistPage()]).grid(row = 1, column= 0)


def findTop():
    global window, connection
    new = Frame(window)
    new.pack()
    
    Button(new,text="Top Users", font = ('Arial',15), command=lambda:[clearFrame(new), displayTopusers()]).grid(row=0, column=0)

    Button(new,text="Top Playlists", font = ('Arial',15), command=lambda:[clearFrame(new), displayTopplaylists()]).grid(row=1, column=0)

    Button(new, text="Back", fg='red', bg='gray',command=lambda: [clearFrame(new), artistPage()], font=('Arial',15)).grid(row=6)


    # The artist should be able to list top 3 users who listen to their songs the longest time
def displayTopusers():
    global connection, cursor, id, window

    # cursor.execute(f"SELECT s.sid FROM songs s, perform p, artists a WHERE p.aid=a.aid AND p.sid=s.sid AND a.aid = '{id}' GROUP BY s.sid;")
    # s_idrow = cursor.fetchall()
    cursor.execute(f'''SELECT u.name FROM users u, listen l, songs s 
                    WHERE u.uid=l.uid AND l.sid IN (SELECT s1.sid FROM songs s1, perform p, artists a 
                                                    WHERE p.aid=a.aid AND p.sid=s1.sid AND a.aid = '{id}' GROUP BY s1.sid) 
                    GROUP BY u.name ORDER BY SUM(l.cnt*s.duration) DESC LIMIT 3;''')
    username = cursor.fetchall()

    # cursor.execute("SELECT distinct u.name FROM users u, listen l, song s, perform p WHERE ")


    #create display page
    displayFrame = Frame(window, borderwidth=0)
    displayFrame.pack()

    lenTop = [1, 2, 3]

    for i in range(0, len(username)):
        Label(displayFrame, text=username[i][0], font=('Arial',15)).grid(row=i, column=0)

    Button(displayFrame, text = "Return", command=lambda: [clearFrame(displayFrame), artistPage()]).grid(row=5, column=0, padx = 15)

    
#top 3 playlists that include the largest number of their songs
def displayTopplaylists():
    global connection, cursor, id

    cursor.execute('''  SELECT p.int, p.sid, p.uid 
                        FROM playlists p, plinclude pl, songs s, artist a 
                        WHERE pl. ''')



    

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
    
    # Save changes in database
    global connection
    connection.commit()
    
if __name__ == "__main__":
    main()
