import nltk
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tokenize import WordPunctTokenizer, sent_tokenize
from nltk.tree import Tree
from collections import Counter
sentence = "We're going to the national championship game! #GoUBears"

#this uses Treebank World Tokenizer, the default tokenizer
tokens = nltk.word_tokenize(sentence)
print(tokens)

wp_tokenizer = WordPunctTokenizer()
wp_tokens = wp_tokenizer.tokenize(sentence)
print(wp_tokens)


text = "I hate newspapermen. They come into camp and pick up their camp rumors and print them as facts. I regard them as spies, which, in truth, they are. If I had my choice I would kill every reporter in the world, but I am sure we would be getting reports from hell before breakfast."

#This uses Punkt Sentence Tokenizer, the default tokenizerI hate newspapermen.

sent_token_list = sent_tokenize(text)
print(sent_token_list)

#removing stop words
stop_words = set(stopwords.words('english'))
my_sentence = "Music is a moral law. It gives soul to the universe, wings to the mind, flight to the imagination, and charm and gaiety to life and to everything."
my_sentence = my_sentence.lower()

tokens = nltk.word_tokenize(my_sentence)
for token in tokens:
	if (token not in stop_words):
		print(token)
	
