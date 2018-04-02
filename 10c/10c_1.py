import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tokenize import sent_tokenize

file = open("./plato_apology.txt")
text = file.read()

sentences = sent_tokenize(text)
numSentence = len(sentences)
print(numSentence)

numTokens = len(nltk.word_tokenize(text))
print(numTokens)

avgTokensPerSent = numTokens/numSentence
print(avgTokensPerSent)

length = -1
for sentence in sentences:
	sentLen = len(nltk.word_tokenize(sentence))
	if (sentLen > length):
		length = sentLen
print(length)
	
