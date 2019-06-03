import json
import string
import time
import re
from urllib.request import urlopen
keywords = input("What key words would you like to search? \nSeparate words with a + (Ex: renaissance+women+art) :\n")
ignore = input("Would you like to ignore any specific words?\nSeparate words with a comma (Ex: fresco,michaelangelo,rafael) :\n")
saveFile = input("What do you want to name your data file?\n")

# index counts the last index recieved 
index = 0
# the base url
baseurl = 'https://www.googleapis.com/books/v1/volumes?maxResults=40&langRestrict=en&orderBy=relevance&projection=full&q='
# start index is added to deal with moving forward in the results
# this is your api key to id yourself to google - don't use mine please
apikey = '&key:AIzaSyAuXnVCa4WAxmHrm-vjU2oDvD8vONJsQyQ'
# query string
query = keywords
# we are going to count on a exception to determine when we are done
# reading the multiple results in the loop
finished = False
#words I don't care about
commonWords = ["i","first","new","examines","studies","womens","also","works","including","me","my","myself","we","our","us","ours","ourselves","you","you're","you've","you'll","you'd","your","yours","yourself","yourselves","he","him","his","himself","she","she's","her","hers","herself","it","it's","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","that'll","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","can","will","just","don","don't","should","should've","now","ain","aren","aren't","couldn","couldn't","didn","didn't","doesn","doesn't","hadn","hadn't","hasn","hasn't","haven","haven't","isn","isn't","ma","mightn","mightn't","mustn","mustn't","needn","needn't","shan","shan't","shouldn","shouldn't","wasn","wasn't","weren","weren't","won't","wouldn","wouldn't","one","two","third","way","book","well","many","provide","year"]
commonWords.extend((ignore))

# a little function to help us write data
def saveData(newFile, *params):
        file = open(newFile, "a")
        file.write('+'.join(params))
        file.write(' ')
        file.close()

while not finished:
    #keeps track of which book result we are looking at
    startIndex = '&startIndex=' + str(index + 1)
    url = baseurl + query + startIndex + apikey
    #opens the url we made
    response = urlopen(url)
    #reads what the data returned
    contents = response.read()
    #allows humans to read the the data returned
    text = contents.decode('utf8')
    #puts text data into a dictionary we can access
    data = json.loads(text)
    try:
        for book in data['items']:
            index += 1
            # basically, we print stuff to a file instead of just the screen
            # I am interested in records with descriptions only, so if there is not one, 
            # I except the error and move on
            if 'description' in book['volumeInfo']:
              #turn description into one big string, make all lowercase
                desc = str(book['volumeInfo']['description']).lower()
                #remove punctuation from description
                descNP = re.sub('['+string.punctuation+']', "", desc)
                #remove common words eg. "the", "and", "a"
                for line in descNP.split():
                  if line in commonWords:
                    line = line.replace(line, "")
                  saveData(saveFile, line)
                #print titles so we can see that the method is working
                print("result " + str(index), book['volumeInfo']['title'])

            else:
                continue
    except Exception as ex: # when google is out of results, for book it will fail...
        finished = True
        continue