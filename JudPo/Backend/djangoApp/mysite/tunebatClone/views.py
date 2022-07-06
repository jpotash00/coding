from django.shortcuts import render
from django.http import HttpResponse
from pySQL.mysqlCredentials import *
def tester(request):
    return HttpResponse("Hello, Django!")

def songs(response):
    return HttpResponse("<h1>Good song choice!</h1>")

def home(request):
    return render(request, 'index.html')

def categoryListing(request):
    mycursor.execute("SELECT * FROM songs")
    data = mycursor.fetchall()
    print(list(data))
    return render(request, 'view.html', {'songs': data})