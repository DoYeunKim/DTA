from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

documents = ["We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light.",
	"Wise men talk because they have something to say; fools, because they have to say something.",
   	"Ignorance, the root and stem of every evil.",
	"Those who tell the stories rule society.",
   	"There are three classes of men; lovers of wisdom, lovers of honor, and lovers of gain.",
   	"Knowing yourself is the beginning of all wisdom",
   	"What is a friend? A single soul dwelling in two bodies",
   	"Happiness is the meaning and the purpose of life, the whole aim and end of human existence.",
	"Patience is bitter, but its fruit is sweet."]

titles = ["Plato-1", "Plato-2", "Plato-3", "Plato-4", "Plato-5", "Aristotle-6", "Aristotle-7", "Aristotle-8", "Aristotle-9"]

def get_top_terms_per_cluster(num_of_terms, num_of_k, model_param, vectorizer_param):
	print("Top terms per cluster: ")
	order_centroids = model_param.cluster_centers_.argsort()[:, ::-1]
	terms = vectorizer_param.get_feature_names()
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
model = KMeans().fit(vected)

num_k = 3

get_top_terms_per_cluster(10, num_k, model, vectorizer)
create_dendrogram(vected, titles)




