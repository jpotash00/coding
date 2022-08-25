import re
import string
from urllib import response
from django.db import connection
from django.db.models import Case, When
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np
from . spotifyCSV import *
from . methods import *
from . models import *

mycursor = connection.cursor()

def landing(request):
    return render(request,'landing.html')

def initialSearch(request):
    if (request.method == 'POST'):
        value=request.POST['song']
        if("by" in value):
            value = value.casefold()
            newStr = value.split(" ")
            newStr.remove("by")
            value = newStr #--> for initial dict
            newStr = ",".join(newStr)
            searching = newStr #--->  for spotifyToCSV
        else:
            value = value.casefold()
            newstr = value.split() #--> for inital dict
            searching = value #---> for spotifyToCSV
            value = newstr

        mycursor.execute("select concat(title,' ',artist) AS songID FROM songs")  #---->Initial database search to get a list of all the titles and artist as one string
        rez = mycursor.fetchall()
        data = list(rez)

        pp = [] #---> for spotify
        for d in rez:
            pp.append(list(d)[0])

        song_dict = {}
        dict_organizer = {}
        intArr = np.zeros(len(data)).astype('int') #initializing numpy array full of 0's of len data
       
        sd = dictCreator(data, song_dict)  #puts everything in dictionary of {word:song_id}
        strNum = highestRankID1(value,sd,intArr) #  #---->gets list of songID's most related to the output from server-side form input not in order (unnecessart)
        if (len(strNum) == 0): #---> empty
            return render(request, 'error.html')
        # mycursor.execute("select song_id, camelot from songs where song_id in %s", [strNum])
        # res = mycursor.fetchall()
        do = getSongIDList(-1,intArr,dict_organizer)
        sort_dict = sorted(do.items(),key=lambda x: x[1], reverse=True)
        newlist = [str(i[0]) for i in sort_dict] #inserts all songIDs (currently in order by rank) into list for ORM DB Search
        # print(newlist)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(newlist)])
        xyz = Songs.objects.filter(pk__in=newlist).values().order_by(preserved) #select * from songs where song_id in list(strNum)
        # print(xyz)
        deta = {0:xyz} #---> original data from DJANGO DB ORM info
        htmlDict = CombineSearch(deta) #--> list of dicts that gets passed to html on render
        # for i in range(len(sort_dict)):
        #     numStrID_key = str(newlist[i]) 
        #     numStrRank_Val = str(sort_dict[i][1])
        #     mycursor.execute("UPDATE songs SET ranked = %s where song_id = %s", [numStrRank_Val,numStrID_key]) #---> idea to create rank system and then delete it so I can get order by rank
        
        #not needed
        # all_results = Songs.objects.raw("select song_id, title, artist, bpm, camelot, song_key from songs where ranked > 0 ORDER BY ranked DESC")
        # for f in all_results: #--> in order to pass info to html, this is the result to choose songs 
        # mycursor.execute("update songs set ranked = NULL where ranked > 0")

    #--------- Pulling Info from API

    # spotCam = spotifyToCamelot(0,1,dict_camMajor,dict_camMinor, dict_key)
    # for k in spotCam:#--> only 1 value
    #     mycursor.execute("select title, camelot from songs where camelot = %s", [k])
    # x = mycursor.fetchall()
    # for r in x:
    return render(request,'add.html', {"htmlDict":htmlDict})

def songSpotify(response):
    mycursor.execute("select concat(title,' ',artist) AS songID FROM songs")  #---->Initial database search to get a list of all the titles and artist as one string
    rez = mycursor.fetchall()
    pp = [] #---> for spotify
    for d in rez:
        pp.append(list(d)[0])
    w = SpotifytoDBtoCSV(searching) #---> need to send search from form here somehow???
    songInDBAlready(pp,w)
    with open("spotifyAPIDump.csv",'r') as filer:
        if getLines(filer) == 0: #shouldn't have to worry about this
            print("empty file, song exists in Db")
        else:
            csv_data = csv.reader(open("spotifyAPIDump.csv"))
            for row in csv_data:
                mycursor.execute("INSERT INTO song_copy(title, artist, genre, released_year, song_key, bpm, camelot, Instrumental_type) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)", row)   
    return render(response,'spotifySearch.html')


def finalSearch(response):   #--> After choosing song it will get sent down here for final query
    match = getHarmonicMatch('11B')#(element from choosen list)
    final_rez = Songs.objects.filter(camelot__in = match).values().order_by('camelot') #DESC, bpm DESC",[match]) #AND song_id != %s, ,res[0][0] ---> put song used as number 1 in table or remove
    de = {0:final_rez} #---> original data from DJANGO DB ORM info
    hD = CombineSearch(de)
    return render(response,'finalSearch.html', {"hD":hD})

def error(request):
    return render(request, 'error.html')