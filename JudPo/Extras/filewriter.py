from filereaderTXT import returnList  
import csv
def txtToCSV():  #for use with csvList without '\n'
    with open('song.csv', 'w') as file:
        counts = 0
        for line in returnList():
            if (counts % 4 != 0) and counts != 0:
                file.write(',')
            elif (counts % 4 == 0) and counts > 0:
                file.write('\n')
            file.write(line)
            counts+=1

def printerCSV(): 
    #counter = 0     
    with open('song.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #counter+=1
            print(row)
    #print(counter)
    
#---------------    
            
def txtToCSV2(): #for use with csvList with '\n'
    counter = 0
    with open('songs.csv', 'w') as file:
        for line in copy:
            if (line == '\n'):
                counter+=1
                file.write('\n')      
            elif copy[counter+1] == '\n':
                file.write(line)
                counter+=1
            else:
                counter+=1
                file.write(line)
                file.write(',')

#-----------  
def toCSV():
    header = ['title','artist','genre','released_year','song_key','camelot','bpm']
    with open('mainsong.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(header)
        writer.writerows(copy)
        #for song_data in copy:
            #song_data_string = ",".join(song_data) --not needed
            #writer.writerow(song_data)
        
#---------Main
copy = returnList();
toCSV()


            