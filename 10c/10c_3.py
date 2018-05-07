from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import PlaintextCorpusReader

corpus_root = "./platos_dialogues/"
my_corpus = PlaintextCorpusReader(corpus_root, '.*txt')
documents = []
titles = []

for text in my_corpus.fileids():
	with open(corpus_root + text, 'rb') as f:
		documents.append(f.read())
	titles.append(text[:-4])

print(titles)

def get_top_terms_per_cluster(num_of_terms, num_of_k, model_param, vectorizer_param):
	print("Top terms per cluster: ")
	order_centroids = model_param.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer_param.get_feature_names()
	print(len(terms))
	for i in range(num_of_k):
		print("Cluster %d: " % i)
		for ind in order_centroids[i, :num_of_terms]:
			print(" %s" % terms[ind])


def create_dendrogram(tfidf_model_param, titles_param):
    from sklearn.metrics.pairwise import cosine_similarity
    from scipy.cluster.hierarchy import ward, dendrogram
    import matplotlib
    matplotlib.use('Agg')
	import matplotlib.pyplot as plt

    dist = 1 - cosine_similarity(tfidf_model_param)
    linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances
    fig, ax = plt.subplots(figsize=(10, 15)) # set size
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles_param)
    plt.tick_params(
        axis = "x",
        which = "both",
        bottom = "off",
        top = "off",
        labelbottom = "off")
    plt.tight_layout()
    plt.savefig("dendrogram.png", dpi = 200)

vectorizer = TfidfVectorizer(stop_words='english')
vected = vectorizer.fit_transform(documents)
num_k = 9 
model = KMeans(n_clusters = num_k, init = 'k-means++', max_iter = 100, n_init = 1).fit(vected)

num_terms = 10


get_top_terms_per_cluster(num_terms, num_k, model, vectorizer)
create_dendrogram(vected, titles)
