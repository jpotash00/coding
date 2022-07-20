from mysqlCredentials import *
import csv
import sys

# def databaseCheck():
#   mycursor.execute("CREATE DATABASE IF NOT EXISTS songMixing")
#   mycursor.execute("USE songMixing")
#   tableImport()
# def tableImport():
#   mycursor.execute("CREATE TABLE IF NOT EXISTS songs (song_id INT NOT NULL AUTO_INCREMENT, title varchar(50), artist varchar(50), genre varchar(25), released_year INT, song_key varchar(25), bpm INT, camelot varchar(3), Instrumental_type varchar(4), ranked INT, PRIMARY KEY (song_id))")

def dataImport():
  csv_data = csv.reader(open("/Users/jonathanpotash/Desktop/Project/JudPo/Backend/pySQL/SongList - mainsong.csv"))
  header = next(csv_data) #skip header
  print('Importing the CSV Files')
  for row in csv_data:
      mycursor.execute("INSERT INTO song_copy(title, artist, genre, released_year, song_key, bpm, camelot, Instrumental_type) VALUES (%s ,%s, %s, %s, %s, %s, %s, %s)", row)   
  mydb.commit()
  mycursor.close()

#main
dataImport()
  

