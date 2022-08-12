import re
import csv

def getLines():
    lineNum = 0
    for lines in file1:
        lineNum+=1
    return lineNum 

def bool_validLine(vLine):
    if vLine == '':
        return False
    for word in vLine:
        if (c > 3):
            return True
        if word[:1].isdigit():
            c+=1
            continue
        if word[:1].isalpha():
            return False 
        if (word[:1] == '.') and c >= 1:
            return True
        else:
            return False

def int_validLine(vLine): #finds number of spaces to skip before valuable info on valid lines 
    c = 0
    if vLine == '':
        return False
    for word in vLine:
        if (c > 3):
            return c
        if word[:1].isdigit():
            c+=1
            continue
        if word[:1].isalpha():
            break 
        if (word[:1] == '.') and c >= 1:
            c+=1
            return c
        else:
            break

def lineCleaner(fileLine): #strips line and removes all spaces between words but leaves special characters
    q = ''
    internalCount = 0
    z = int_validLine(fileLine)
    for ch in fileLine:
        if internalCount < z:
            internalCount+=1
            continue
        if ch == ' ':
            continue 
        else:
            q+= ch
    return q

def getTitle(fileLine):
    x = ''
    for words in fileLine:
        if (words == '('):
            return x
        else:
            #------
            if (x.isalpha() and words.isdigit()):
                x += ' '
                x += words
                continue
            #-----
            if words == '<':
                x += ' '
            if (len(x)> 3):
                if (x[-1] == 'U' and words == 'S'):
                    x += words
                    continue
                if (x[-1] == 'S' and words == 'A'):
                    x += words
                    continue
            #------
            if (x == 'I' and words.isupper()):
                x += ' '
                x += words
                continue
            #------
            if (x.isupper() and words.isupper()):
                x += words
                continue
            if (words.isalpha() and words.isupper() and x != ''):
                if (x[-1] == '<'):
                    x+= words
                    continue
                x += ' '
                x += words
            #---------
            else:
                x += words

def getArtist(fileLine):
    a = fileLine
    st = 'Mc'
    st1 = 'D'
    art = re.search('\((.*?)\)', a).group(1)
    x = ''

    for word in art:
        if (len(x) > 0):
            if(x[-1].isalpha()) and (word.isdigit()):
                x += ' '
        if (word == '&'):
            x += ' '
        if (x == 'D' and word == 'J'):
            x+= word
            continue
        if (len(x) > 0):
            if(x[-1] == '\'' and word.isupper()):
                x += word
                continue
        if (st in x and word == 'C'):
            x += word
            continue
        if (word.isalpha() and word.isupper() and x != ''):
            x += ' '
            x += word
        else:
            x += word
    return x
def getCamelot(fileLine):
    c = fileLine
    cl = re.search('\[(.*?)\/', c).group(1)
    return cl
def getBPM(fileLine):
    b = fileLine
    bp = re.search('\/(.*?)\]', b).group(1)
    return bp
def returnList():
    return csv_list

 #----MAIN           
with open('song.txt', 'r') as file1:
    count = 0
    lineCount = getLines()
    if lineCount == 0:
        print("Error: empty file")
        file1.close()
with open('song.txt', 'r') as file2:
    csv_list = []
    while(count < lineCount):
        newline = file2.readline()
        line = newline.strip()
        count+=1
        if (bool_validLine(line) == True):
            tmp_list = []
            fLine = lineCleaner(line)
            tmp_list.append(getTitle(fLine))
            tmp_list.append(getArtist(fLine))
            tmp_list.append(getCamelot(fLine))
            tmp_list.append(getBPM(fLine))
            csv_list.append(tmp_list) #for writerrow
    #print(csvList)
    #print(len(csvList))
    
    
    #------
    #if (bool_validLine(line) == True):
        #fLine = lineCleaner(line)
        #csvList.append(getTitle(fLine)); 
        #csvList.append(getArtist(fLine));
        #csvList.append(getCamelot(fLine));
        #csvList.append(getBPM(fLine));
    
    #-------
    #if (bool_validLine(line) == True):
        #if (count != lineCount): #///
        #    fLine = lineCleaner(line)
        #    csvList.append(getTitle(fLine)); 
        #    csvList.append(getArtist(fLine));
        #    csvList.append(getCamelot(fLine));
        #    csvList.append(getBPM(fLine));
        #    csvList.append('\n') #//
       # else:#///
         #   fLine = lineCleaner(line)
         #   csvList.append(getTitle(fLine)); 
         #   csvList.append(getArtist(fLine));
         #   csvList.append(getCamelot(fLine));
         #   csvList.append(getBPM(fLine));