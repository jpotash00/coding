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
        dict_organizer = {}
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
        #---->gets the a singular songID most related to the output from html request
        for word in value:
            x = list(song_dict.get(word))
            np.add.at(intArr,x,1)
        max_value = max(intArr)
        indexTupGreatest = np.where(intArr == max_value) #--> get just one most likely answer
        songIDIndexGreatest = int(indexTupGreatest[0]+1)
        strNum = str(songIDIndexGreatest)
        mycursor.execute("select song_id, title, artist, bpm, camelot from songs where song_id = %s", [strNum]) 
        # res = mycursor.fetchall()
        #----> gets list in order of all related songID's
        songid = -1
        for rank in intArr:
            songid+=1
            if (rank > 0):
                dict_organizer[songid+1] = rank
        sort_dict = sorted(dict_organizer.items(),key=lambda x: x[1], reverse=True)
        newlist = []
        for i in range(len(sort_dict)):
            newlist.append(sort_dict[i][0])
            numStrKey = str(newlist[i])
            numStrVal = str(sort_dict[i][1])
            mycursor.execute("UPDATE song_copy SET ranked = %s where song_id = %s", [numStrVal,numStrKey]) #---> idea to create rank system and then delete it so I can get order by rank
        mycursor.execute("select song_id, title, artist, bpm, camelot from song_copy where ranked > 0 ORDER BY ranked DESC LIMIT 10") #(1,2,12,23,37,125) - for happy now by kygo
        # songChoices = mycursor.fetchall()
        # for row in songChoices:
        #     print(row)
        mycursor.execute("update song_copy set ranked = NULL where ranked > 0")
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