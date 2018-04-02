from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet  import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from nltk.stem.porter import *
pa = PorterStemmer()

#
regex_tokenizer = RegexpTokenizer(r'\w+')
regex_tokenizer.tokenize("We're going to the national championship game! #GoUBears")

print("Shows -> " + pa.stem('shows'))
print("Leaves -> " + pa.stem('leaves'))

print("Shows -> " + lmtzr.lemmatize('shows'))
print("Leaves -> " + lmtzr.lemmatize('leaves'))
print("was -> " + lmtzr.lemmatize('was', 'v'))
print("men -> " + lmtzr.lemmatize("men", "n"))
