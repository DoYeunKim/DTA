from nltk.corpus import PlaintextCorpusReader
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter
import requests
import nltk

# Look for places in the given article
def get_places(words_param):
	chunked = ne_chunk(pos_tag(words_param))
	prev = None
	continuous_chunk = []
	current_chunk = []
	for i in chunked:
		if type(i) == Tree:
			if (i.label() == "GPE"): #filter places
				current_chunk.append(" ".join([token for token, pos in i.leaves()]))
	return current_chunk

# Search for the lattitude and the longitude of the places found
def get_latlongbytype(place_param, type_param = "city"):
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + place_param)
	resp_json_payload = response.json()
	try:
		types = (resp_json_payload['results'][0]['address_components'][0]['types'])
		if any(type_param in s for s in types):
			latlong = resp_json_payload['results'][0]['geometry']['location']
		else:
			latlong = ""
	except:
		latlong = ""
	return latlong

# Read in the articles that are stored as .txt files
corpus_root="./2ndAssign"
txt = PlaintextCorpusReader(corpus_root, '.*txt')
print(txt.fileids())
places = [] 

# Iterate through the articles and append the list of places in the given article to 
# the composite list (places)
for article in txt.fileids():
	content = txt.words(article)
	places.extend(list(set(get_places(content))))

lat = []
long = []

# Look for lattitude and longitude of the locations in places
for place in places:
	print(place)
	listlong = get_latlongbytype(place, type_param="locality")
	if listlong == "":
		pass
		# print("Not found")
	else:
		lat.append(listlong['lat'])
		long.append(listlong['lng'])
		print(listlong)

# Plot the lats and longs
import gmplot
gmap = gmplot.GoogleMapPlotter.from_geocode("Kansas, USA", zoom=2)
gmap.heatmap(lat, long, 20, 20)
gmap.draw("./2ndAssign/school_shooting.html")
