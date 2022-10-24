# This will be our source code
import sqlite3
import tkinter as tk
from tkinter import simpledialog

connection = None
cursor = None


def connect(path):
    '''
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    
    connection.executescript(''''''drop table if exists perform;
                        drop table if exists artists;
                        drop table if exists plinclude;
                        drop table if exists playlists;
                        drop table if exists listen;
                        drop table if exists sessions;
                        drop table if exists songs;
                        drop table if exists users;

                        create table users (
                        uid		char(4),
                        name		text,
                        pwd		text,
                        primary key (uid)
                        );
                        create table songs (
                        sid		int,
                        title		text,
                        duration	int,
                        primary key (sid)
                        );
                        create table sessions (
                        uid		char(4),
                        sno		int,
                        start 	date,
                        end 		date,
                        primary key (uid,sno),
                        foreign key (uid) references users
                            on delete cascade
                        );
                        create table listen (
                        uid		char(4),
                        sno		int,
                        sid		int,
                        cnt		real,
                        primary key (uid,sno,sid),
                        foreign key (uid,sno) references sessions,
                        foreign key (sid) references songs
                        );
                        create table playlists (
                        pid		int,
                        title		text,
                        uid		char(4),
                        primary key (pid),
                        foreign key (uid) references users
                        );
                        create table plinclude (
                        pid		int,
                        sid		int,
                        sorder	int,
                        primary key (pid,sid),
                        foreign key (pid) references playlists,
                        foreign key (sid) references songs
                        );
                        create table artists (
                        aid		char(4),
                        name		text,
                        nationality	text,
                        pwd		text,
                        primary key (aid)
                        );
                        create table perform (
                        aid		char(4),
                        sid		int,
                        primary key (aid,sid),
                        foreign key (aid) references artists,
                        foreign key (sid) references songs
                        );'''''')
    connection.commit()
    '''
    return

def main():
    path = "./project1.db"
    connect(path)
    ROOT = tk.Tk()

    ROOT.withdraw()

    user_type = simpledialog.askstring(title = "Song management", prompt = "Are you a user or an artist")
    print(user_type)
    
if __name__ == "__main__":
    main()