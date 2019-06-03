from wordcloud import WordCloud
import matplotlib.pyplot as plt 
import sys
from PIL import Image
import numpy as np
from os import path

#initiate data structures
list1 = []
list2 = []
text = " "

#populate list 1 with words from file 1
try:
	l1 = input("What file would you like to read from? \n")
	with open(l1, 'r') as data:
		for line in data:
			for word in line.split():
				list1.append(word.upper())
except:
	print("Something went wrong. I can't find that file!")
	sys.exit()

#populate list 2 with words from file 2
try:
	l2 = input("What file would you like to compare it with? \n")
	with open(l2, 'r') as data:
		for line in data:
			for word in line.split():
				list2.append(word.lower())
except:
	print("Something went wrong. I can't find that file!")
	sys.exit()

def topNWords(wordlist):
	#frequency dictionary
	frqzTable = {}
	#count frequency of words in wordlist
	for word in wordlist:
		if word in frqzTable:
			frqzTable[word] += 1
		else:
			frqzTable[word] = 1
	#scale frequencies so that there is a more even representation of words from file 1 and file 2
	for word in frqzTable:
		frqzTable[word] = sqrt(frqzTable[word]/len(wordlist))
	return frqzTable

#method that maps words to colors and sets a default color
class Colorize(object):
	def __init__(self,colorMap,defaultColor):
		#map words to colors
		self.wordMap = {word:color
						 for (color, words) in colorMap.items()
						 for word in words}
		#set default color
		self.defaultColor = defaultColor

	def __call__(self,word,**kwargs):
		#return wordmap and deafault color
		return self.wordMap.get(word,self.defaultColor)

#text1 = ' '.join(list1)
#text2 = ' '.join(list2)
#text = text1 + ' ' + text2


#set up creation of word cloud

#choose mask image
mask = np.array(Image.open('cloudmask.png'))
#get path to where this file is stored if it exists
filepath = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#get font otf file
font = filepath + 'BowlbyOneSC-Regular.otf'
#background color
background = (35,13,13)
#topNWords
num = input("How many words would you like to look at? \n")
#find top N most frequent words of file 1
freq1 = topNWords(list1)
#find top N most frequent words of file 2
freq2 = topNWords(list2)
#make a dictionary of frequency
frqzTable = {**freq1, **freq2}
sortedWords = dict(sorted(frqzTable.items(), key=lambda x: x[1], reverse=True)[:int(num)])
#generate word cloud
cloud = WordCloud(collocations = False, width = 1500, height = 1300, background_color = background, mask = mask, min_font_size = 10, max_words = int(num), font_path = font).fit_words(sortedWords)

#set up for recolor of word cloud

#save desired colors
c1 = input("What two colors do you want to use? Press enter after typing each color. \n")
c2 = input("")
#map set 1 to specific color
colorMap = {c1:list1}
#set default color
defaultColor = c2
#save effects of our Colorize function into a variable
colorized = Colorize(colorMap,defaultColor)

#recolor our wordcloud with our color specifications
cloud.recolor(color_func=colorized)

#plot cloud with matplotlib
plt.imshow(cloud)
plt.show()