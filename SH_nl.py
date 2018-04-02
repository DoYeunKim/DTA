from nltk.corpus import PlaintextCorpusReader
corpus_root = "./SH"
my_corpus = PlaintextCorpusReader(corpus_root, '[^__].*txt')
print(my_corpus.fileids())
#my_corpus.words('hound_of_baskerville.txt')[10:20]
#sentOut = my_corpus.sents('hound_of_baskerville.txt')[10]
#print(sentOut)
from nltk.text import Text
hound=Text(my_corpus.words('hound_of_baskerville.txt'))
#hound.concordance("Watson")
#hound.similar("hound")
#hound.collocations()
#from nltk.probability import FreqDist
#my_fdist = FreqDist(hound)
#top_100 = my_fdist.most_common(100) 
#print(top_100[50:99])
#my_fdist.hapaxes()
#hound.dispersion_plot(["Holmes","Watson"])
#hound.dispersion_plot(["Stapleton", "Henry", "Barrymore"])

#ne_chunk: name chunk ; pos_tag: part of speech ; word_tokenize: chunking
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter

def get_characters(words_param):
    chunked = ne_chunk(pos_tag(words_param))
    prev = None
    continuous_chunk = []
    current_chunk = []
    #print(chunked)

    for i in chunked:
        if type(i) == Tree:
            if (i.label() == "PERSON"):
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))


    #print(current_chunk)
    return current_chunk


top10 = Counter(get_characters(hound)).most_common(10)
#print(top10)

names = []
for person in top10:
	full_title = person[0]
	words_of_names = full_title.split()
	last_name = words_of_names[-1]
	names.append(last_name)

print(names)	

unique_names = list(set(names))
print(unique_names)

hound.dispersion_plot(unique_names)
