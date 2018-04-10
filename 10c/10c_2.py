import nltk
from nltk.corpus import PlaintextCorpusReader, stopwords
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
regex_tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
from collections import Counter

file = open("./aristotle_politics.txt")
text = file.read()
text = text.lower()
tokenized = regex_tokenizer.tokenize(text)


non_stop = []
for token in tokenized:
	if (token not in stop_words):
		non_stop.append(token)

for index, tokens in enumerate(non_stop):
	non_stop[index] = lmtzr.lemmatize(non_stop[index])

lemmas = Counter(non_stop).most_common(10)
print(lemmas)

