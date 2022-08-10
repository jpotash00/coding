import csv
import re
import string
import numpy as np

import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

def dictCreator(data,song_dict): #added
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
    return song_dict #added
    
def highestRankID(value,song_dict,intArr): #added
    for word in value:
        x = list(song_dict.get(word))
        np.add.at(intArr,x,1)
    max_value = max(intArr)
    indexTupGreatest = np.where(intArr == max_value) #--> get just one most likely answer
    songIDIndexGreatest = int(indexTupGreatest[0]+1)
    #numStr = str(songIDIndexGreatest) - removed
    return str(songIDIndexGreatest) #added

def highestRankID1(value,song_dict,intArr):
    for word in value:
        # if ((song_dict.get(word)) == None):
        #     print("missing word:", word)
        # else:
            #///get me all the songs containing this word by artist 
        x = list(song_dict.get(word))
        np.add.at(intArr,x,1)
    max_value = max(intArr)
    indexTupGreatest = np.where(intArr == max_value) #--> get just one most likely answer
    ls = []
    if (len(indexTupGreatest[0]) > 1): #if ranks at multiple highest value then
        for i in range(len(indexTupGreatest[0])):
            ls.append(str(indexTupGreatest[0][i]+1))
        # indexTupGreatest = indexTupGreatest[0][:-1]
        # songIDIndexGreatest = int(indexTupGreatest[0]+1)  
    else:
        songIDIndexGreatest = int(indexTupGreatest[0]+1)
        ls.append(str(songIDIndexGreatest))
    return ls

def getSongIDList(songid,intArr,dict_organizer):
    # (songid = -1) - removed
    for rank in intArr:
        songid+=1
        if (rank > 0):
            dict_organizer[songid+1] = rank #add +1 because it's starts from 0 and our song_id's start from 1 so it will be dimensionally consistent
    return dict_organizer #added
    
def getHarmonicMatch(song_beat): #str, will use this for final query
    matching_camelots = [song_beat]
    number = int(song_beat[:-1])
    letter = song_beat[-1]
    cl = ['A','B']
    if letter == 'A':
        tmp_song_beat = str(number) + 'B'
    else:
        tmp_song_beat = str(number) + 'A'
    matching_camelots.append(tmp_song_beat)

    possible_cams = [number+i for i in [1,-1]]
    for num in possible_cams:
        if (num == 0):
            matching_camelots.append(str(12)+letter)
        if (num >=1 and num <=12):
            matching_camelots.append(str(num)+letter)
        elif (num > 12):
            matching_camelots.append(str(num % 12)+letter)
        # elif (num < 0):
        #     matching_camelots.append(str((abs(num))%12)+letter)
    if (cl[0] == letter): #A
        camlist = [matching_camelots[-2].replace(letter, cl[1]),matching_camelots[-1].replace(letter, cl[1])]
    else:
        camlist = [matching_camelots[-2].replace(letter, cl[0]),matching_camelots[-1].replace(letter, cl[0])]
    return matching_camelots + camlist

def spotifyToCamelot(key,mode,listMajor,listMinor, dict_key): #<int,int,dict,dict,dict>
    list = ['-Flat','-Sharp']
    dict_Cam = {}
    true_dict = {}
    dict_Cam[0] = listMinor
    dict_Cam[1] = listMajor
    dict_key.get(key)
    val = dict_Cam[mode][dict_key.get(key)] #--> '12A'
    letter = val[-1]

    for key,value in dict_Cam[mode].items():
        if (val == value): 
            k = key #--> 'C'
            break
    
    if (letter == 'B'):
        scale = 'Major'
        if 'b' in k: #--> add flat
            result = k[:-1] + list[0] + " " + scale
        elif '#' in k: #--> add sharp
            result = k[:-1] + list[1] + " " + scale 
        else:
            result = k + " " + scale 
    else: 
        scale = 'Minor'
        if 'b' in k: #--> add flat
            result = k[:-1] + list[0] + " " + scale
        elif '#' in k: #--> add sharp
            result = k[:-1] + list[1] + " " + scale 
        else:
            result = k + " " + scale 
    true_dict[val] = result #---> {'8B':'C Major'} for key = 0, mode = 1
    return true_dict

#---------------SpotifySearchMethods--------------------#
# credentials = json.load(open('static/authorization.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)

sp = spotipy.Spotify()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTracks(searchquery):
    getTrack = sp.search(q=searchquery,market=['US','FR','GB','CH','KR','DE'])
    tracks = {}
    IDlist = []
    arter = []
    trackIDlist = {}
    rez = getTrack['tracks']['items']
    for i in range(len(rez)):
        album_type = rez[i]['album']['album_type']
        trackName = rez[i]['name']
        trackID = rez[i]['id']
        try:
            tttt = rez[i]['artists'][1]['name']
        except:
            ttt = ""
        if (album_type != 'compilation'): #test if album != 'compilation'
            if('Acoustic' not in trackName):
                regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                if(regex.search(trackName) == None):
                    resid = [ele for ele in ['Remix','Mix','Edit'] if(ele not in trackName)]
                    if ('-' in trackName and len(resid) == 3):
                        x = trackName.split('-')
                        trackName = x[0].rstrip()
                    if(trackName not in tracks.values()):
                        tracks[trackID] = trackName #title
                        IDlist.append(trackID)
                        arter.append(rez[i]['artists'][0]['name'])
                        arty = arter[-1]
                        trackIDlist[i] = {trackID:trackName}
                    elif(trackID not in tracks.keys() and trackName in tracks.values() and arty not in arter): #need to account for artist instead of trackID
                        IDlist.append(trackID)
                        arter.append(rez[i]['artists'][0]['name'])
                        trackIDlist[i] = {trackID:trackName}
                elif('(with %s)' in trackName, [tttt]):
                    trackName = re.sub("[\(\[].*?[\)\]]", "", trackName)
                    if ('-' in trackName):
                        x = trackName.split('-')
                        trackName = x[0].rstrip() + ' -' + x[1]
                    else:
                        trackName = trackName.rstrip()
                    resid = [ele for ele in ['Remix','Mix','Edit'] if(ele not in trackName)]
                    if (' - ' in trackName and 'Live' in trackName and len(resid) == 3): #and (ele for ele: #and ele for ele in ['Remix','Mix','Edit'] if(ele not in trackName)): #all the small things
                        x = trackName.split(' - ')
                        trackName = x[0].rstrip()
                    else:
                        trackName += ' Remix'
                    if(trackName not in tracks.values()):
                        tracks[trackID] = trackName #title
                        IDlist.append(trackID)
                        trackIDlist[i] = {trackID:trackName}
    return trackIDlist

def getArtists(searchquery):
    count = -1
    artists = []
    listArtists = {}
    getArtist = sp.search(q=searchquery,market=['US','FR','GB','CH','KR','DE'])
    getID = getTracks(searchquery)
    rez = getArtist['tracks']['items']
    for i in range(len(rez)):
        namer = ""
        if (i in getID.keys()):
            count+=1
            artists.append(rez[i]['artists'])
            namer = artists[count][0]['name']
            listArtists[i] = namer 
    return listArtists

def getGenreSpot(dict): #get artists and track first
    dictGenre = {}
    for k,v in dict.items():
        searchquery = v.split('&')[0].rstrip()
        getArtist = sp.search(q=searchquery,type='artist',market=['US','FR','GB','CH','KR','DE'])
        genre = getArtist['artists']['items'][0]['genres'][0]
        if (genre == 'complextro'):
            dictGenre[k] = 'Electro House'
        elif (genre == 'edm'):
            dictGenre[k] = 'EDM'
        else:
            dictGenre[k] = genre.title()
    return dictGenre
   
def getReleasedYear(searchquery): #gets list of release_years for each song
    getRelease = sp.search(q=searchquery,market=['US','FR','GB','CH','KR','DE'])
    releaseYear = {}
    getID = getTracks(searchquery)
    rez = getRelease['tracks']['items'] #dict of dicts -> artist
    for i in range(len(rez)):
        if (i in getID.keys()):
            releaseYear[i]= (int(rez[i]['album']['release_date'][:4])) #release date
    return releaseYear

def getSong_Key(dict):
    dict_camMajor = {'C':'8B', 'Db':'3B', 'D':'10B', 'Eb':'5B', 'E':'12B', 'F':'7B', 'F#':'2B', 'G':'9B', 'Ab':'4B', 'A':'11B', 'Bb':'6B', 'B':'1B'}
    dict_camMinor = {'C':'5A', 'Db':'12A', 'D':'7A', 'Eb':'2A', 'E':'9A', 'F':'4A', 'F#':'11A', 'G':'6A', 'Ab':'1A', 'A':'8A', 'Bb':'3A', 'B':'10A'}
    dict_key = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}

    Idl = []
    keyDict = {}
    getID = list(dict.keys())
    for num in getID:
        y = list(dict[num].keys())[0]
        Idl.append(y)
    zz = sp.audio_features(Idl)
    for i in range(len(zz)):
        fKey = int(zz[i]['key'])
        fMode = int(zz[i]['mode'])
        z = spotifyToCamelot(fKey,fMode,dict_camMajor,dict_camMinor,dict_key)
        for val in z.values():
            keyDict[getID[i]] = val
    return keyDict

def getBPM(dict):
    bpmDict = {}
    Idl = []
    getID = list(dict.keys())
    for num in getID:
        y = list(dict[num].keys())[0]
        Idl.append(y)
    zz = sp.audio_features(Idl)
    for i in range(len(zz)):
        bpmDict[getID[i]] = int(round(float(zz[i]['tempo']),0))
    return bpmDict

def getCamelot(dict):
    dict_camMajor = {'C':'8B', 'Db':'3B', 'D':'10B', 'Eb':'5B', 'E':'12B', 'F':'7B', 'F#':'2B', 'G':'9B', 'Ab':'4B', 'A':'11B', 'Bb':'6B', 'B':'1B'}
    dict_camMinor = {'C':'5A', 'Db':'12A', 'D':'7A', 'Eb':'2A', 'E':'9A', 'F':'4A', 'F#':'11A', 'G':'6A', 'Ab':'1A', 'A':'8A', 'Bb':'3A', 'B':'10A'}
    dict_key = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'F#', 7:'G', 8:'Ab', 9:'A', 10:'Bb', 11:'B'}

    Idl = []
    camDict = {}
    getID = list(dict.keys())
    for num in getID:
        y = list(dict[num].keys())[0]
        Idl.append(y)
    zz = sp.audio_features(Idl)
    for i in range(len(zz)):
        fKey = int(zz[i]['key'])
        fMode = int(zz[i]['mode'])
        z = spotifyToCamelot(fKey,fMode,dict_camMajor,dict_camMinor,dict_key)
        for kay in z.keys():
            camDict[getID[i]] = kay
    return camDict

def SpotifytoDBtoCSV(searchquery):
    fullList = []
    t = getTracks(searchquery)
    a = getArtists(searchquery)
    g = getGenreSpot(a)
    r = getReleasedYear(searchquery)
    sk = getSong_Key(t)
    bp = getBPM(t)
    cm = getCamelot(t)
    for i in t.keys():
        tmp_list = []
        ti = ((list(t[i].values()))[0])
        if ('-' in ti):
            ti = ti.replace('- ','<') + '>'
        tmp_list.append(ti)
        tmp_list.append(a[i])
        tmp_list.append(g[i])
        tmp_list.append(r[i])
        tmp_list.append(sk[i])
        tmp_list.append(bp[i])
        tmp_list.append(cm[i])
        tmp_list.append("No")
        fullList.append(tmp_list)
    return fullList

def songInDBAlready(DBDatalist,SpotListSearch):
    with open('spotifyAPIDump.csv', 'w', newline = '') as csvfile:
        for i in range(len(SpotListSearch)):
            x = (SpotListSearch[i][0] + " " + SpotListSearch[i][1])
            z = string.capwords(x)
            if ('’' in z):
                word = ""
                for le in z:
                    if (le == '’'):
                        word += "'"
                    else:
                        word += le
            z = word
            if (z in DBDatalist): #not working
                SpotListSearch.remove(SpotListSearch[i])
                return songInDBAlready(DBDatalist,SpotListSearch)
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerows(SpotListSearch)
    #------ 
def getDBdataList(plist):
    lll = []
    for d in plist:
        lll.append(string.capwords(d))
    return lll