# from django.conf import settings
from django.db import connection


mycursor = connection.cursor()
song = 'Happy Now'
mycursor.execute("select title, artist, bpm, camelot from songs where camelot = (select camelot from songs where title = %s)", song)
result = mycursor.fetchall()
for row in result:
    print(row)