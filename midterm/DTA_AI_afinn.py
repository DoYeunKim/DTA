############################################################################################################
# py script to perform afinn sentiment analysis on the txt files procured so far
# 
# Created by Do Yeun Kim (04/07/2018)
#
# This script follows fetchArticles.py

import nltk
from nltk.corpus import stopwords, PlaintextCorpusReader
from nltk import ne_chunk, pos_tag, word_tokenize
from collections import Counter
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from afinn import Afinn
from statistics import mean
import pandas as pd
import codecs

afinn = Afinn()
regex_tokenizer = RegexpTokenizer(r'\w+')
posArticlesIndex = []
posArticlesYear = []
negArticlesIndex = []
negArticlesYear = []
stop_words = set(stopwords.words('english'))

# Fetch files and initialize the dataframe to store data
corpus_root = "./DTA_AI_data/"
my_corpus = PlaintextCorpusReader(corpus_root, '.*txt')
print(len(my_corpus.fileids()))
analyze = pd.DataFrame(columns = ['Title', 'avgVal', 'negMostVal', 'posMostVal'])
negSource = pd.DataFrame(columns = ['Year', 'Index'])
posSource = pd.DataFrame(columns = ['Year', 'Index'])

# Process utf files
# Reads in txt files from ./DTA_AI_data/
# Then sentence tokenize the texts, assess the valence of each sentence using afinn sentiment analyzer
# Then returns average valence, most negative valence, and most positive valence of each article as .csv
def sentAnalyze():
	
	# Iterate through all the txt files and perform sentiment analysis
	for index, article in enumerate(my_corpus.fileids()):
		# Open file, perform sentence tokenization, and initialize temporary array
		# Here, we use codecs with 'utf-8-sig' tag to consume BOM's that are getting in the way
		# of properly encoding the text file
		sfile = codecs.open(corpus_root + article, 'r', 'utf-8-sig')
		text = sfile.read()
		sentences = sent_tokenize(text)
		valence = []
		year = article.split('_')[0]

		# Iterate through each sentence and perform sentiment analysis, populating valence[]
		for num, sent in enumerate(sentences):
			vscore = afinn.score(sent)
			valence.append(vscore)

		# Extract overall valence, most negative valence, and most positive valence
		# Ignore files that don't have any content for the time being
		# Populate the dataframe
		if len(valence) > 0:
			average = mean(valence)
			minV = min(valence)
			maxV = max(valence)
			analyze.loc[index + 1] = [article, average, minV, maxV]

		# If the article has negative valence, then add it to negArticles for further processing
		if average < 0:
			negArticlesIndex.append(index)
			negArticlesYear.append(year)
		elif average > 0:
			posArticlesIndex.append(index)
			posArticlesYear.append(year)
		print("Done with " + article)
		sfile.close()

	analyze.to_csv("./DTA_AI_valence/valences.csv")

	# Output indices for overall negative and overall positive articles for further processing
	negSource['Index'] = negArticlesIndex
	negSource['Year'] = negArticlesYear
	negSource.to_csv("./DTA_AI_valence/negArticles.csv", index=False)

	posSource['Index'] = posArticlesIndex
	posSource['Year'] = posArticlesYear
	posSource.to_csv("./DTA_AI_valence/posArticles.csv", index=False)
	



def extractAdjectives():

	negSource = pd.read_csv('./DTA_AI_valence/negArticles.csv')
	NSLen = len(negSource.Index) - 1
	negSource["Tag"] = ['N'] * (NSLen + 1)
	posSource = pd.read_csv('./DTA_AI_valence/posArticles.csv')
	PSLen = len(posSource.Index) - 1
	posSource["Tag"] = ['P'] * (PSLen + 1)

	
	for i in range(0, NSLen + 1):
		index = negSource.Index[i]	
		afile = codecs.open(corpus_root + my_corpus.fileids()[index], 'r', 'utf-8-sig')
		text = afile.read()
		regexed = regex_tokenizer.tokenize(text)
		tagged = nltk.pos_tag(regexed)
		adjectives = ""	

		for tokens in tagged:
			if (tokens[0] not in stop_words):
				if tokens[1][:2] == 'NN':
					adjectives = adjectives + " " + tokens[0]	
		
		textIndex = "{0:0=4d}".format(i)		
		loc = './DTA_AI_voyant/neg_noun/' + textIndex + '.txt'
		with open(loc, 'wb') as out:
			out.write(adjectives.encode('utf-8'))

		afile.close()
	print("Done with negative articles")


	for j in range(0, PSLen + 1):
		index = posSource.Index[j]	
		afile = codecs.open(corpus_root + my_corpus.fileids()[index], 'r', 'utf-8-sig')
		text = afile.read()
		regexed = regex_tokenizer.tokenize(text)
		tagged = nltk.pos_tag(regexed)
		adjectives = ""	

		for tokens in tagged:
			if (tokens[0] not in stop_words):
				if tokens[1][:2] == 'NN':
					adjectives = adjectives + " " + tokens[0]	
		
		textIndex = "{0:0=4d}".format(j)		
		loc = './DTA_AI_voyant/pos_noun/' + textIndex + '.txt'
		with open(loc, 'wb') as out:
			out.write(adjectives.encode('utf-8'))

		afile.close()
	print("Done with positive articles")

def globalAdjectives():

	for index, article in enumerate(my_corpus.fileids()):
		gfile = codecs.open(corpus_root + article, 'r', 'utf-8-sig')
		text = gfile.read()
		
		regexed = regex_tokenizer.tokenize(text)
		tagged = nltk.pos_tag(regexed)
		adjectives = ""	

		for tokens in tagged:
			if (tokens[0] not in stop_words):
				if tokens[1]== 'NNP':
					adjectives = adjectives + " " + tokens[0]	
		
		textIndex = "{0:0=4d}".format(index)		
		loc = './DTA_AI_voyant/global_pnoun/' + textIndex + '.txt'
		with open(loc, 'wb') as out:
			out.write(adjectives.encode('utf-8'))

		gfile.close()
		print("Done with " + article)

#sentAnalyze()
extractAdjectives()
#globalAdjectives()
