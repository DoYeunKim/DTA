from nltk.corpus import PlaintextCorpusReader
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter
import requests
import nltk

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


#my_sent = "Hi I am in Boston, calling for you in Las Vegas"
#tokens = nltk.word_tokenize(my_sent)
#print(tokens)

#print(get_places(tokens))

def get_latlongbytype(place_param, type_param = "country"):
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

#latlong = get_latlongbytype('Brunswick ME', type_param="locality")
#print(latlong)

corpus_root="./"
txt = PlaintextCorpusReader(corpus_root, 'Jules_Verne_Around_The_World.txt')
#places = list(set(get_places(txt)))
#Above code does not allow for the txt object to be iterated.
#turns out that I need to use .words() function to allow this
#Here is the modified version:
places = list(set(get_places(txt.words(txt.fileids()))))
#print(places)

lat = []
long = []

for place in places:
	#print(place)
	listlong = get_latlongbytype(place, type_param="locality")
	if listlong == "":
		print("Not found")
	else:
		lat.append(listlong['lat'])
		long.append(listlong['lng'])

import gmplot
gmap = gmplot.GoogleMapPlotter.from_geocode("Sicily,Italy", zoom=2)
gmap.heatmap(lat, long, 20, 20)
gmap.draw("around_the_world.html")
