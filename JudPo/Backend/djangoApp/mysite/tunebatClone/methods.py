import csv
import re
import numpy as np

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
        if ((song_dict.get(word)) == None):
            print("missing word:", word)
        else:
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
