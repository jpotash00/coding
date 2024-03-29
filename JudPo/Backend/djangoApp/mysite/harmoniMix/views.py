import re
import string
from typing import final
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
    #----for initial post value
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
            return error(request)
        do = getSongIDList(-1,intArr,dict_organizer)
        sort_dict = sorted(do.items(),key=lambda x: x[1], reverse=True)
        newlist = [str(i[0]) for i in sort_dict] #inserts all songIDs (currently in order by rank) into list for ORM DB Search  
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(newlist)])
        xyz = Songs.objects.filter(pk__in=newlist).values().order_by(preserved)
        deta = {0:xyz} #---> original data from DJANGO DB ORM info
        htmlDict = CombineSearch(deta,searching) #--> list of dicts that gets passed to html on render
    #----> when we get from spotChecker
    elif (request.method == 'GET'):
        try:
            value = request.GET.get('search')
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
                return error(request)
            do = getSongIDList(-1,intArr,dict_organizer)
            sort_dict = sorted(do.items(),key=lambda x: x[1], reverse=True)
            newlist = [str(i[0]) for i in sort_dict] #inserts all songIDs (currently in order by rank) into list for ORM DB Search  
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(newlist)])
            xyz = Songs.objects.filter(pk__in=newlist).values().order_by(preserved)
            deta = {0:xyz} #---> original data from DJANGO DB ORM info
            htmlDict = CombineSearch(deta,searching) 
            return render(request,'add.html', {"htmlDict":htmlDict})
        except: #when we get to finalSong
            val = request.GET.get('camelot')
            print(val)
            return finalSearch(request, val)
    return render(request,'add.html', {"htmlDict":htmlDict})


def songSpotify(request):
    value = request.GET.get('search')  #get data from original post??
    if("by" in value):
        value = value.casefold()
        newStr = value.split(" ")
        newStr.remove("by")
        # value = newStr #--> for initial dict
        newStr = ",".join(newStr)
        searching = newStr #--->  for spotifyToCSV
    else:
        value = value.casefold()
        # newstr = value.split() #--> for inital dict
        searching = value #---> for spotifyToCSV
        # value = newstr
    mycursor.execute("select concat(title,' ',artist) AS songID FROM songs")  #---->Initial database search to get a list of all the titles and artist as one string
    rez = mycursor.fetchall()
    pp = [] #---> for spotify
    for d in rez:
        pp.append(list(d)[0])
    w = SpotifytoDBtoCSV(searching)
    songInDBAlready(pp,w)
    with open("spotifyAPIDump.csv",'r') as filer:
        if getLines(filer) == 0: #shouldn't have to worry about this
            print("empty file, song exists in Db")
        else:
            csv_data = csv.reader(open("spotifyAPIDump.csv"))
            for row in csv_data:
                mycursor.execute("INSERT INTO songs(title, artist, genre, released_year, song_key, bpm, camelot,Instrumental_type) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)", row)  
    dict = {"s": searching} 
    return render(request,'spotifySearch.html', {"dict": dict})

def finalSearch(request, song_cam):   #--> After choosing song it will get sent down here for final query
    match = getHarmonicMatch(song_cam)#(element from choosen list - 11B temporary)
    final_rez = Songs.objects.filter(camelot__in = match).values().order_by('camelot') #DESC, bpm DESC",[match]) #AND song_id != %s, ,res[0][0] ---> put song used as number 1 in table or remove
    de = {0:final_rez} #---> original data from DJANGO DB ORM info
    hD = CombineSearch1(de)
    return render(request,'finalSearch.html', {"hD":hD})

def error(request):
    val = request.POST.get('song')
    dict = {"v": val}
    return render(request, 'error.html', {"dict":dict})