from django.db import connection
from django.shortcuts import redirect, render
from django.http import HttpResponse
mycursor = connection.cursor()
# def tester(request):
#     return HttpResponse("Hello, Django!")

#def songs(response):
#     return HttpResponse("<h1>Good song choice!</h1>")

def home(request):
    mycursor.execute("select * from songs where title LIKE %s", [("%" + 'happy now' + "%")])#works with remixes
    result = mycursor.fetchall()
    if (len(result) == 0): #then make API call
            pass
    else:
        mycursor.execute("select title, artist, bpm, camelot from songs where camelot = (select camelot from songs where title LIKE %s) ORDER BY BPM DESC", [("%" + 'happy now' + "%")]) #need to do a Join (set foreign key as instrumental key)
        result = mycursor.fetchall()
        for row in result:
            print(row)

    return render(request, 'home.html')

def categorySearch(response):
    if (response.method == 'POST'):
        song = response.POST
        print(song)
        mycursor.execute("select * from songs where title LIKE %s", [("%" + song + "%")])#works with remixes
        result = mycursor.fetchall()
        if (len(result) == 0): #then make API call
            pass
        else:
            mycursor.execute("select title, artist, bpm, camelot from songs where camelot = (select camelot from songs where title = %s", song) #need to do a Join (set foreign key as instrumental key)
            result = mycursor.fetchall()
            for row in result:
                print(row)
 
    return render(response,"<h1>%s</h1>",result)

def categoryCreated(response):
    return render(response, 'add.html')