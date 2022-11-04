# Mini-Project-1
This is our group Mini Project 1 for CMPUT 291

-------------
Contributors:
-------------
- Adrien
- Basia
- Gabriel

------------
Introduction
------------
- The goal of this assignment is twofolds: (1) to teach the use of SQL in a host programming language, and (2) to demonstrate some of the functionalities that result from combining SQL with a host programming language.
- The aim in this project is to build a system that keeps the enterprise data in a database and to provide services to users. 
- Data will be stored in a SQLite database and will be writing code in Python (or similarly Java/JDBC, C, etc.) to access it. 
- The code will implement a simple command line interface. 

--------------
Other Comments
--------------
- There is an option to implement a GUI interface instead but there will be no support nor bonus for doing that.  
- Code can be written in Python, Java, C, C++, Perl or any other language that is suited for the task. If you decide to use any language other than Python, you should let the instructor know in advance.
- Your project will be evaluated on the basis of 84% of the mark for implementing the functionalities listed in this specification; this component will be assessed in a demo session. 
- Another 12% of the mark will be assigned for both the documentation and the quality of your source code. 
- 4% of the mark is assigned for the quality of your group coordination and the project break-down between partners.

----------------------
Database Specification
----------------------
You are given the following relational schema.

- users(uid, name, pwd)
- songs(sid, title, duration)
- sessions(uid, sno, start, end)
- listen(uid, sno, sid, cnt)
- playlists(pid, title, uid)
- plinclude(pid, sid, sorder)
- artists(aid, name, nationality, pwd)
- perform(aid, sid)

These tables are derived from the specification of Assignment 1 and are identical to those in Assignment 2 except the tables users and artists, which have now a field for password (referred to as pwd). Use the given schema in your project and do not change any table/column names.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

**TASK!**
------------
Login Screen
------------
- The first screen of your system should provide options for both users and artists to login. 
- Both class of users should be able to login using a valid id (respectively denoted as uid and aid for users and artists) and a password, denoted with pwd.  
- After a successful login, the system should detect whether it is a user or an artist and provide the proper menus as discussed next. If the entered id is a valid id in both users and artists tables, then the user will be asked if they want to login as a user or as an artist.

- Unregistered users should be able to sign up by providing a unique uid and additionally a name, and a password. Passwords are not encrypted in this project. 
- After a successful signup, users should be able to perform the subsequent user operations (possibly chosen from a menu) as discussed next. 
- Artists cannot sign up through your system (and you assume they are already in the database).

- Users should be able to logout, which directs them to the first screen of the system. There must be also an option to exit the program directly. 
- When exiting the program, any session that is still open should be closed automatically.

----------------------
System Functionalities
----------------------
After a successful login, users should be able to perform all of the following tasks:

    1. Start a session. The user should be able to start a session. For each session, a session number unique for the user should be assigned by your system, the 
       session start date should be set to the current date and the session end date should be set to null.
    2. Search for songs and playlists. The user should be able to provide one or more unique keywords, and the system should retrieve all songs and playlists that have 
       any of those keywords in title. For each matching song, the id, the title and the duration, and 
       for each matching playlist, the id, the title and the total duration of songs in the playlist should be returned. Each row of the result should indicate if it 
       is a song or a playlist. The result should be ordered based on the number of matching keywords with 
       songs/playlists that match the largest number of keywords listed on top. If there are more than 5 matching songs/playlists, at most 5 matches will be shown at a 
       time, letting the user either select a match or see the rest of the matches in a paginated downward format. 
       If a playlist is selected, the id, the title and the duration of all songs in the playlist should be listed. Any time a list of songs are displayed, the user 
       should be able to select a song and perform a song action as discussed next. 
    3. Search for artists. The user should be able to provide one or more unique keywords, and the system should retrieve all artists that have any of those keywords 
       either in their names or in the title of a song they have performed. For each matching artist, the name, the 
       nationality and the number of songs performed are returned. The result should be ordered based on the number of matching keywords with artists that match the 
       largest number of keywords listed on top. If there are more than 5 matching artists, at most 5 matches will be 
       shown at a time, letting the user either select a match for more information or see the rest of the matches in a paginated downward format. The user should be 
       able to select an artist and see the id, the title and the duration of all their songs. Any time a list of songs 
       are displayed, the user should be able to select a song and perform a song action as discussed next. 
    4. End the session. The user should be able to end the current session. This should be recorded with the end date/time set to the current date/time. 
    

Song actions: 
  When a song is selected, the user can perform any of these actions: 
    (1) listen to it, 
    (2) see more information about it, or 
    (3) add it to a playlist. 
  More information for a song is the names of artists who performed it in addition to id, title and duration of the song as well as the names of playlists the song is in (if any). When a song is selected for listening, a listening event is recorded within the current session of the user (if a session has already started for the user) or within a new session (if not). When starting a new session, follow the steps given for starting a session. A listening event is recorded by either inserting a row to table listen or increasing the listen count in this table by 1. When adding a song to a playlist, the song can be added to an existing playlist owned by the user (if any) or to a new playlist. When it is added to a new playlist, a new playlist should be created with a unique id (created by your system) and the uid set to the id of the user and a title should be obtained from input. 

Artists should be able to perform the following actions:
  (1) Add a song. 
        The artists should be able to add a song by providing a title and a duration. 
        The system should check if the artists already has a song with the same title and duration. 
        If not, the song should be added with a unique id (assigned by your system) and any additional artist who may have performed the song with their ids obtained from input.
  (2) Find top fans and playlists. 
        The artist should be able to list top 3 users who listen to their songs the longest time and top 3 playlists that include the largest number of their songs. 
        If there are less than 3 such users or playlists, fewer number of users and playlists can be returned. 
        
---------------
String matching
---------------
  Except the password which is case-sensitive, all other string matches (include id, name, title, etc.) are case-insensitive. 
  This means the keyword "drake" will match Drake, DRAKE, and DrAke, and you cannot make any assumption on the case of the strings in the database. 
  The database can have strings in uppercase, lowercase or any mixed format.

--------------
Error checking 
--------------
  Every good programmer should do some basic error checking to make sure the data entered is correct. We cannot say how much error checking you should or should not do, or detail out all possible checkings. 
  However, we can say that we won't be trying to break down your system but your system also should not break down when the user makes a mistake.
  
*Groups of size 3 must counter SQL injection attacks and make the password non-visible at the time of typing.*
