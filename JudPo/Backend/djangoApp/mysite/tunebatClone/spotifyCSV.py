import re
import pandas as p
import csv
from . methods import *

def getLines():
    lineNum = 0
    for lines in file1:
        lineNum+=1
    return lineNum 

def bool_validLine(vLine):
    try:
        bool = vLine[0][0].isdigit()
        if (bool == False):
            return False
        else:
            return True
    except:
        return False
def int_validLine(vLine): #finds number of spaces to skip before valuable info on valid lines 
    if bool_validLine(vLine) == False:
        return 0
    else: 
        return 1
def getTrack_id(id):#-->string
    return id
def getTitle(title):#-->string
    try:
        return title.title()
    except:
        listIssues.add(count)
def getArtist(artist):#-->string
    try:
        return artist.title()
    except:
        listIssues.add(count)
def getGenre(genre): #-->string
    try:
        return genre.title()
    except:
        listIssues.add(count)
def getRelease_Year(year): #--->int
    try:
       return int(year[:4])
    except:
        listIssues.add(count)
def getSong_Key_BPM_Camelot(fileKey, fileMode):#-->string (key, mode)
    try:
        x = int(fileKey)
        y = int(fileMode)
        z = spotifyToCamelot(x,y,dict_camMajor,dict_camMinor, dict_key)
        for mo,ke in z.items():
            tmp_list.append(ke)
            tmp_list.append(getBPM(line[7])) 
            tmp_list.append(mo)
    except:
        listIssues.add(count)
def getBPM(bpm): #-->int
    try:
        return int(round(float(bpm),0))
    except:
        listIssues.add(count)
def Instrumental():
    return "No"
def returnList():
    return csv_list
def returnListIssues():
    return listIssues

def getIndividualSongs(title,artist):
    x = title + "," + artist
    return x

def toCSV():
    header = ['title','artist','genre','released_year','song_key','bpm','camelot','Instrumental_type','ranked']
    with open('spotifyMassDump.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(header)
        writer.writerows(copy)
 #----MAIN 
dict_camMajor = {'C':'8B', 'Db':'3B', 'D':'10B', 'Eb':'5B', 'E':'12B', 'F':'7B', 'F#':'2B', 'G':'9B', 'Ab':'4B', 'A':'11B', 'Bb':'6B', 'B':'1B'}
dict_camMinor = {'C':'5A', 'Db':'12A', 'D':'7A', 'Eb':'2A', 'E':'9A', 'F':'4A', 'F#':'11A', 'G':'6A', 'Ab':'1A', 'A':'8A', 'Bb':'3A', 'B':'10A'}
dict_key = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}
          
with open("/Users/jonathanpotash/Desktop/github_code/coding/JudPo/Backend/pySQL/spotifySongList.csv", 'r') as file1:
    count = 0
    lineCount = getLines()
    if lineCount == 0:
        print("Error: empty file")
        file1.close()
    
with open("/Users/jonathanpotash/Desktop/github_code/coding/JudPo/Backend/pySQL/spotifySongList.csv", 'r') as file2:
    listIssues = set() #set of lines where there was an issue
    duplicatID = {} #contains duplicate spotifyTrackID's for removal
    duplicatSongs = {} #dict of {line where error occurred: completeSongsArtist}
    completeIDs = [] #contains completeList of spotifyTrackID's in csvFile
    completeSongsArtist = [] #contains duplicate string of "song,artist" for removal
    csv_list = [] 
    while(count < lineCount):
        tmp_list = []
        newline = file2.readline()
        line = newline.strip().split(',')
        count+=1
        if (count > 1):
            if (bool_validLine(line) == True):
                if (getIndividualSongs(line[1],line[2]) in completeSongsArtist):
                    duplicatSongs[count] = getIndividualSongs(line[1],line[2])
                if (getTrack_id(line[0]) in completeIDs):
                    duplicatID[count] = line[0]
                if (len(line) < 8):
                    listIssues.add(count)
                else:
                    completeIDs.append(getTrack_id(line[0]))
                    tmp_list.append(getTitle(line[1]))
                    completeSongsArtist.append(getIndividualSongs(line[1],line[2]))
                    tmp_list.append(getArtist(line[2]))
                    tmp_list.append(getGenre(line[3]))
                    tmp_list.append(getRelease_Year(line[4]))
                    getSong_Key_BPM_Camelot(line[5],line[6]) #5 = key, #6 = mode
                    tmp_list.append(Instrumental())
                    csv_list.append(tmp_list) #for writerrow
copy = returnList()
toCSV()