#Importing necessary libraries

import requests
from collections import Counter
import pandas as pd
import json


"""-----------------.Top Ten Most Appearing Characters.--------------"""


url = 'https://swapi.dev/api/films' #URL for getting all the films details

films = requests.get(url).json() #Requesting the URL and converting the response into JSON type.

allCharacters = [] #List for containing Names and Heights of all the characters.

for i in range(len(films['results'])): #Looping through the entire Films Results.
    for j in films['results'][i]['characters']: #Looping through each and every characters using index location.
        allCharacters.append([requests.get(j).json()['name'],requests.get(j).json()['height']]) #Appending the names and heights of those characters by requesting their particular URL.

topTen = Counter([i[0] for i in allCharacters]) #Counter Function to get the count of all the names.
topNames = [] #Empty list to be used for sorting the characters
print('Top Ten Most Appearing Characters :')
for names in topTen.most_common(10): #Getting the Top 10 most appearing characters.
    print(names[0]) #Printing each Character onto next line
    topNames.append(names[0]) #Appending Most Common characters.

print()
print()
print()
"""------------------Sorting the Characters based on their Height--------------------"""

byheights = {} #Empty Dictionary

for name in topNames: #Looping through each names in most common names
   for value in allCharacters: #Looping through Character's Characteristics
       if name==value[0]: #Checking if name is in allCharacters
            byheights.update({name:int(value[1])}) #Updating the dictionary with characters name and height.
print('Top Ten Most Appearing Characters According to their Height :')
print("\n".join([j[0] for j in sorted(byheights.items(), key=lambda x:x[1],reverse=True)])) #Sorting the dictionary wrt its values in Descending order and printing the names out of it.




"""--------------------CSV------------------------"""


url = r'https://swapi.dev/api/people/' #URL for getting People details in StarWars

response = requests.get(url).json() #Response variable and converting it to JSON type.

columns = ['name', 'species', 'height', 'Appearences'] #Columns name

peopleInfo = {} #Empty dictionary to create DataFrame from.

for col in columns: #Looping through each column name
    if col != 'Appearences' and col != 'species': #Condition to update dict for only Name and Height column.
        peopleInfo.update({col:[response['results'][i][col] for i in range(len(response['results']))]})
    elif col != 'Appearences' and col == 'species':  #Condition to update dict for only species column.
        peopleInfo.update({col: [requests.get(" ".join(response['results'][i][col])).json()['name'] if response['results'][i][col] !=[] else 'Human' for i in range(len(response['results']))]})
    else:  #Condition to update dict for Appearences  column.
        peopleInfo.update({col:[len(response['results'][i]['films']) for i in range(len(response['results']))]})

finalCSV = pd.DataFrame(peopleInfo) #Converting the dictionary into a Pandas DataFrame
finalCSV.columns = finalCSV.columns.str.capitalize() #Capitializing the columns name
finalCSV.to_csv('Characters Detail',index=False) #Creating a CSV

"""------------------Sending the CSV File------------------"""

with open('Characters Detail', 'rb') as f: #Opening the file in Read-Binary Format
    r = requests.post('http://httpbin.org/post', files={'Character Detail.csv': f}) #Sending the file using POST method

#Checking if the connection was successful
if r.status_code == 200:
    print('CSV File Uploaded Successfully')
    print(r.text)
else:
    print('Error Sending the file.')












