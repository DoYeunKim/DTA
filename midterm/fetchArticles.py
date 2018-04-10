###################################################################################################################
# py script that fetches the content of the articles given url's
#
# Created by Do Yeun Kim (04/06/2018)
#
# This script follows nytScrapper.py, and is followed by DTA_AI_afinn.py

import requests
from lxml import html
import pandas as pd
import codecs
import math

# Fetch the content of each article 
def fetchText():
	# Read in a csv file as dataframe
	utfFilter = pd.read_csv('./DTA_AI_utfFilter.csv', names=['Year', 'Index'])

	for dates in range(0, len(utfFilter.Year) - 1):
		date = int(utfFilter.Year[dates])
		csvFile = './DTA_AI_csv/' + str(date) + '.csv'
		articles = pd.read_csv(csvFile, names=['Year', 'URL'])
		articlesRange = len(articles.Year)

		if (math.isnan(utfFilter.Index[dates])):
			index= articlesRange
		else:
			index = int(utfFilter.Index[dates])	
		print(index)
		if index < 1:
			utfFilter.loc[dates] = [date, articlesRange]

		# Iterate through the csv, extract year and url
		# Then submit HTML request to get the articles
		for i in range(1,articlesRange):
			url = articles.URL[i]
			year = articles.Year[i]

			# Fetch the articles from "story-body-text story-content" paragraphs 
			# (standard for article body) from NYT
			# "css-1p5hko7 emamhsk2" is a different class of paragraphs
			try:
				page = requests.get(url)
				tree = html.fromstring(page.text)

				content = []
				content = content + tree.xpath('//p[@class="story-body-text story-content"]/text()')
				content = content + tree.xpath('//p[@class="css-1o5hko7 emamhsk2"]/text()')

			except:
				content = " "
	
			content = str(content)	
	

			# There is a bunch of articles in ASCII and the rest in utf-8
			# To make it easier to process them for text analysis, we are going to store them separately
			print(utfFilter.Index[dates])
			path = "./DTA_AI_data/"
			fileName = year + "_rel_" + str(i) + ".txt"
			loc = path + fileName

			if i >= index:
				print(loc)	
				with open (loc, 'wb') as out:
					out.write(content.encode('utf-8'))
			else:	
				loc = path + fileName
				print(loc)
				with open (loc, 'w') as out:
					out.write(content)	
						

fetchText()
