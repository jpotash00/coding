import re
from django.db import connection
from django.shortcuts import redirect, render
from django.http import HttpResponse
import numpy as np
from . methods import *

mycursor = connection.cursor()
# def tester(request):
#     return HttpResponse("Hello, Django!")
#def songs(response):
#     return HttpResponse("<h1>Good song choice!</h1>")
# def home(request):
#     if (request.method == 'POST'):
#         value=request.POST['song']
#         print(value)
#         print("....... it works")
#     mycursor.execute("select * from songs where title LIKE %s", [("%" + value + "%")])#works with remixes
#     result = mycursor.fetchall()
#     if (len(result) == 0): #then make API call
#         pass
#     else:
#         mycursor.execute("select title, artist, bpm, camelot from songs where camelot = (select camelot from songs where title = %s) ORDER BY BPM DESC", value) #need to do a Join (set foreign key as instrumental key)
#         result = mycursor.fetchall()
#         for row in result:
#             print(row)
 
#     return render(request,'add.html')

def home(request):
    return render(request, 'home.html')

def categorySearch(request):
    if (request.method == 'POST'):
        value=request.POST['song']
        if("by" in value):
            value = value.title()
            newStr = value.split(" ")
            newStr.remove("By")
            value = newStr
        else:
            value = value.title()
            newstr = value.split()
            value = newstr
    #---->Initial database search to get a list of all the titles and artist as one string
        mycursor.execute("select concat(title,' ',artist) AS songID FROM songs")
        rez = mycursor.fetchall()
        data = list(rez)
        #---->Initialized empty Data Structures
        song_dict = {}
        dict_organizer = {}
        intArr = np.zeros(len(data)).astype('int')
        dict_camMajor = {'C':'8B', 'Db':'3B', 'D':'10B', 'Eb':'5B', 'E':'12B', 'F':'7B', 'F#':'2B', 'G':'9B', 'Ab':'4B', 'A':'11B', 'Bb':'6B', 'B':'1B'}
        dict_camMinor = {'C':'5A', 'Db':'12A', 'D':'7A', 'Eb':'2A', 'E':'9A', 'F':'4A', 'F#':'11A', 'G':'6A', 'Ab':'1A', 'A':'8A', 'Bb':'3A', 'B':'10A'}
        dict_key = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
        #---->puts everything in dictionary of {word:song_id}
        sd = dictCreator(data, song_dict)
        #---->gets the singular songID most related to the output from html request
        strNum = highestRankID(value,sd,intArr)
        mycursor.execute("select song_id, title, artist, bpm, camelot from songs where song_id = %s", [strNum]) 
        # res = mycursor.fetchall()
        # for row in res:
        #     print(row)
        #----> gets list in order of all related songID's
        do = getSongIDList(-1,intArr,dict_organizer)
        sort_dict = sorted(do.items(),key=lambda x: x[1], reverse=True)
        newlist = [i[0] for i in sort_dict] 
        for i in range(len(sort_dict)):
            newlist.append(sort_dict[i][0])
            numStrKey = str(newlist[i])
            numStrVal = str(sort_dict[i][1])
            mycursor.execute("UPDATE song_copy SET ranked = %s where song_id = %s", [numStrVal,numStrKey]) #---> idea to create rank system and then delete it so I can get order by rank
        mycursor.execute("select song_id, title, artist, bpm, camelot from song_copy where ranked > 0 ORDER BY ranked DESC LIMIT 10") #(1,2,12,23,37,125) - for happy now by kygo
        # songChoices = mycursor.fetchall() #--> send this info to frontend so that I can choose which song I want to obtain a single base song
        # for row in songChoices:
        #     print(row)
        mycursor.execute("update song_copy set ranked = NULL where ranked > 0")
    #--------- Pulling Info from API
    spotCam = spotifyToCamelot(0,1,dict_camMajor,dict_camMinor, dict_key)
    for k in spotCam:#--> only 1 value
        mycursor.execute("select title, camelot from songs where camelot = %s", [k])
    # x = mycursor.fetchall()
    # for r in x:
    #     print(r)
    # mycursor.execute("select * from songs where songs.title LIKE %s AND songs.artist LIKE %s", [("%" + t + "%"), ("%" + a + "%")])#works with remixes
    
    return render(request,'add.html')

def categoryCreated(response):
    return render(response, 'add.html')