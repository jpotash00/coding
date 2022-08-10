import re
import string
from django.db import connection
from django.shortcuts import redirect, render
from django.http import HttpResponse
import numpy as np
from . spotifyCSV import *
from . methods import *
from . models import *

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

def landing(request):
    mycursor.execute("select concat(title,' ',artist) AS songID FROM songs")
    rez = mycursor.fetchall()
    pp = []
    
    for d in rez:
        pp.append(list(d)[0])
    searching = "getaway syn cole"
    w = SpotifytoDBtoCSV(searching)
    lip = songInDBAlready(pp,w)
    with open("spotifyAPIDump.csv",'r') as filer:
        if getLines(filer) == 0: #shouldn't have to worry about this
            print("empty file, song exists in Db")
        else:
            csv_data = csv.reader(open("spotifyAPIDump.csv")) #/Users/jonathanpotash/Desktop/github_code/coding/JudPo/Backend/djangoApp/mysite
            for row in csv_data:
                mycursor.execute("INSERT INTO song_copy(title, artist, genre, released_year, song_key, bpm, camelot, Instrumental_type) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)", row)   
    return render(request,'output1.html')
    # return render(request,'landing.html')

def initialSearch(request):
    if (request.method == 'POST'):
        value=request.POST['song']
        if("by" in value):
            value = string.capwords(value) #value = value.title()
            newStr = value.split(" ")
            newStr.remove("By")
            value = newStr
        else:
            value = string.capwords(value) #value = value.title()
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

        #**** dict_camMajor = {'C':'8B', 'Db':'3B', 'D':'10B', 'Eb':'5B', 'E':'12B', 'F':'7B', 'F#':'2B', 'G':'9B', 'Ab':'4B', 'A':'11B', 'Bb':'6B', 'B':'1B'}
        #**** dict_camMinor = {'C':'5A', 'Db':'12A', 'D':'7A', 'Eb':'2A', 'E':'9A', 'F':'4A', 'F#':'11A', 'G':'6A', 'Ab':'1A', 'A':'8A', 'Bb':'3A', 'B':'10A'}
        #**** dict_key = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
       
        #---->puts everything in dictionary of {word:song_id}
        sd = dictCreator(data, song_dict)
        #---->gets list of songID's most related to the output from html input
        strNum = highestRankID1(value,sd,intArr)
        # mycursor.execute("select song_id, title, artist, bpm, camelot from songs where song_id in %s", [strNum]) 
        mycursor.execute("select song_id, camelot from songs where song_id in %s", [strNum])
        res = mycursor.fetchall()
        # print(res[0][1])
        # for row in res:
        #     pass
    #--Not Needed Unless testing for HTML
        xyz = Songs.objects.raw("select * from songs where song_id in %s", [strNum]) 
        for choice in xyz: #---> print all songs in most desirable list purposes
            pass
    #-----
    #----> gets dict in order of all related songID's by {songid:rank}
        do = getSongIDList(-1,intArr,dict_organizer)
        sort_dict = sorted(do.items(),key=lambda x: x[1], reverse=True)
        newlist = [i[0] for i in sort_dict] #inserts all songIDs (currently in order by rank) into list
        for i in range(len(sort_dict)):
            # newlist.append(sort_dict[i][0])
            numStrID_key = str(newlist[i]) 
            numStrRank_Val = str(sort_dict[i][1])
            mycursor.execute("UPDATE songs SET ranked = %s where song_id = %s", [numStrRank_Val,numStrID_key]) #---> idea to create rank system and then delete it so I can get order by rank
        #not needed
        all_results = Songs.objects.raw("select song_id, title, artist, bpm, camelot, song_key from songs where ranked > 0 ORDER BY ranked DESC")
        for f in all_results: #--> in order to pass info to html, this is the result to choose songs
            pass
        #^^^^^^
        mycursor.execute("update songs set ranked = NULL where ranked > 0")
        #--> After choosing song it will get sent down here for final query
        match = getHarmonicMatch(res[0][1]) #-->currently choosing #1 (likliest search) song's in list's camelot 
        final_rez = Songs.objects.raw("select song_id, title from songs where camelot in %s ORDER BY camelot DESC, bpm DESC",[match]) #AND song_id != %s, ,res[0][0]
        for finale in final_rez:
            pass
    #--------- Pulling Info from API
    # spotCam = spotifyToCamelot(0,1,dict_camMajor,dict_camMinor, dict_key)
    # for k in spotCam:#--> only 1 value
    #     mycursor.execute("select title, camelot from songs where camelot = %s", [k])
    # x = mycursor.fetchall()
    # for r in x:
    #     print(r) 
    return render(request,'add.html', {"xyz": xyz}) #***

    # return render(request,'add.html', {"final_rez": final_rez}) #***

# def finalSearch(request):
#     pass

def categoryCreated(response):
    return render(response, 'add.html')