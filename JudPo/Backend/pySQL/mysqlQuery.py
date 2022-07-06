from xml.dom.pulldom import DOMEventStream
from mysqlCredentials import *

#--main
name = input("Enter song_title or artist: ")
mycursor.execute("select * from songs where title = %s", [name])
findTitle = mycursor.fetchall()
if (len(findTitle) == 0):
    mycursor.execute("select * from songs where artist = %s", [name])
    findArtist = mycursor.fetchall()
    if (len(findArtist) == 0):
        print("Song Doesn't Exist in Database")
    else:
        mycursor.execute("select title, artist, bpm, camelot from songs where artist = %s", [name])
        result = mycursor.fetchall()
        for row in result:
            print(row)
else:
    mycursor.execute("select title, artist, bpm, camelot from songs where title LIKE %s", [("%" + name + "%")])#works with remixes
    result = mycursor.fetchall()
    for row in result:
        print(row)

    

#---extra

name = input("Enter song_title or artist: ")
mycursor.execute("Select title, artist from songs where (title = %s OR artist = %s)", [name,name])

val = mycursor.fetchone()
if (val == None):
    raise Exception(name + " is not a valid song_title or artist")
else:
    pass
#col_idx = x.index(x)
#print(col_idx)
