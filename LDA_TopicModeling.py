from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.tokenize import RegexpTokenizer
import glob, os

## Helper function to print the words of each topic
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx))
        print (" ".join([feature_names[i]+ ' ' + str(round(topic[i], 2))
              +' \n ' for i in topic.argsort()[:-no_top_words - 1:-1]]))


## Helper Function to break a string into chunks        
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# Change current folder to the location where your files are stored\n",
os.chdir('./works_by_aristotle')
documents = []
    
# Lets create documents with 1000 words
chunk_size = 1000
    
for filename in glob.glob("*.txt"):
	## Open and read the file
	file = open(filename, "r")
	text = file.read()

	#Use tokenizer to split the file text into words
	regex_tokenizer = RegexpTokenizer(r'\w+')
	file_words = regex_tokenizer.tokenize(text)
    
	# Now we will partion the file into documents of the size size (chunk_size)
	words_chunks = list(chunks(file_words,chunk_size))  
	for i in range(len(words_chunks)):
		documents.append(' '.join(words_chunks[i]))
    
#Define the maximum number of features to be considered
no_features = 1000
    
# Create the Vector Space with CountVectorizers
tf_vectorizer= CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

no_topics = 40
# Run LDA
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=50).fit(tf)

no_top_words = 10
display_topics(lda, tf_feature_names, no_top_words)

lda.perplexity(tf)

