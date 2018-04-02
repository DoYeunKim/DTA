import pandas as pd
from nltk.corpus import PlaintextCorpusReader
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter

corpus_root = "./SH"
my_corpus = PlaintextCorpusReader(corpus_root, '[^__].*txt')

from nltk.text import Text
#print(my_corpus.fileids())

def rangedf():
	df = pd.DataFrame(columns=['Book', 'tokens', 'types'])

	for index in range (1,len(my_corpus.fileids())+1):
		book_name = my_corpus.fileids()[index - 1]
		book_content = my_corpus.words(book_name)
	
		file_name = book_name 
		book_tokens = len(book_content)
		book_types =  len(set(book_content))

		df.loc[index] = [file_name, book_tokens, book_types]

	print(df)

df1 = pd.DataFrame(columns=['Book', 'tokens', 'types'])
def indexdf(df1):

	for index, book in enumerate(my_corpus.fileids()):
		content = my_corpus.words(book)
		file_name = book
		book_tokens = len(content)
		book_types = len(set(content))
	
		df1.loc[index + 1] = [file_name, book_tokens, book_types]
	print("\nFull files: \n", df1)

#rangedf()
indexdf(df1)

#df.apply(lambda <thing being added>: <value>, <dimension>
#use this command to add "TTR" to dataframe
#df1['TTR'] = df1.apply(lambda row: 100 * row.types / row.tokens, axis=1)


df2 = pd.DataFrame(columns=['Book', 'tokens', 'types', 'TTR'])
def normaldf(df2):

	for index, book in enumerate(my_corpus.fileids()):
		content=my_corpus.words(book)[:50000]
		file_name = book
		book_tokens = len(content)
		book_types = len(set(content))
		TTR = (book_types/book_tokens) * 100

		df2.loc[index + 1] = [file_name, book_tokens, book_types, TTR]
	print("\nThe first 50K words: \n", df2)


normaldf(df2)

import matplotlib as plt

df2.plot(x="Book", y="TTR")	
