import re
from django.db import connection
from django.shortcuts import redirect, render
from django.http import HttpResponse
import numpy as np

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
    intArr = np.zeros(len(data)).astype('int')
    #---->puts everything in dictionary of {word:song_id}
    for songID in range(len(data)):
        for word in data[songID]:
            if ('<' in word or '>' in word):
                f = filter(str.isalpha, word)
                s = "".join(f)
                res_list = re.findall('[A-Z][^A-Z]*',s)
                data[songID] = res_list
            else:
                data[songID] = data[songID][0].split()
            for word in data[songID]:
                if (word in song_dict.keys()):
                    song_dict[word].add(songID)
                else:
                    song_dict[word] = set([songID])
    #---->gets the songID most related to the output from html request
    for word in value:
        print(word)
        x = list(song_dict.get(word))
        np.add.at(intArr,x,1)
    max_value = max(intArr)
    indexTupGreatest = np.where(intArr == max_value) #--> get just one most likely answer
    songIDIndexGreatest = int(indexTupGreatest[0]+1)
    strNum = str(songIDIndexGreatest)

     
    mycursor.execute("select song_id, title, artist, bpm, camelot from songs where song_id = %s", strNum) 
    res = mycursor.fetchall()
    for row in res:
        print(row)
    #---------
    # mycursor.execute("select * from songs where songs.title LIKE %s AND songs.artist LIKE %s", [("%" + t + "%"), ("%" + a + "%")])#works with remixes
    # result = mycursor.fetchall() #if more than 1 comes up than choose 1
    # if (len(result) == 0): #then make API call
    #     print("doesn't exist in database")
    # else:
    # #     print("before")
    #     mycursor.execute("select title, artist, bpm, camelot from songs where camelot = (select camelot from songs where title = %s) Order By (title = %s) DESC", [t,t]) #need to do a Join (set foreign key as instrumental key)
    # #     print(">>>>>>>after")
    #     res = mycursor.fetchall()
    #     for row in res:
    #         print(row)
 
    return render(request,'add.html')

def categoryCreated(response):
    return render(response, 'add.html')