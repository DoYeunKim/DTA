###################################################################################################################
# py script to use NYT Articles API to gather New York Times articles that fits the query
# 
# Created by Do Yeun Kim
#
# The first code to be ran, followed by fetchArticles.py
#

from urllib.request import urlopen
from nytimesarticle import articleAPI
import time
import pandas as pd

# API key for NYT API's
# 229edd80e1c84eb38a7ad4983b31e318
#api = articleAPI("229edd80e1c84eb38a7ad4983b31e318")
api = articleAPI("890989d50b494c01823421a8f0c28b42")

# These codes were used to determine API limits
#res = urlopen("https://api.nytimes.com/svc/books/v3/lists/overview.json?api-key=890989d50b494c01823421a8f0c28b42")
#print(res.info())
#res.close();

# Fetch the published date and url for articles
def runAPI():

	# Determine some variables
	byYear = getYearlyNumber();
	numYears = len(byYear.Year) - 1
	starYear = int(byYear.Year[0])
	endYear = int(byYear.Year[numYears])

	# Counting for adding to dataframe
	count = 0

	# Iterate through years
	for years in range(0,numYears + 1):

		# Get date
		date = byYear.Year[years]
		print(date)

		# Initialize pd
		this_year = pd.DataFrame(columns = ["Published Date", "URL"])
		csv_name = str(date) + ".csv"
		
		# Iterate through each year's worth of pages
		for i in range(0, byYear.Iterate[years]): 
			print(i)
			
			# API search
			# Defining begin_date and end_date
			# '0813' and '0812' from the first article on NYT on NYT AI Topics
			# which was published in 1984/08/13
			articles = api.search(q = '"artificial intelligence"',
						begin_date = int(str(date) + '0813'),
						end_date = int(str(date + 1) + '0812'),
						page = i)

			# For each article in page, grab pub_date and url
			# Then add these to dataframe
			for doc in range(0,10):
				pub_date = articles['response']['docs'][doc]['pub_date'][:10]
				url = articles['response']['docs'][doc]['web_url']
				this_year.loc[count] = [pub_date, url]
				count += 1
			
			# Wait some time to avoid exceeding API limits
			if i != byYear.Iterate[years]:
				wait()
		
		# Write each year's worth of data to a csv file
		print("Done with ", date)
		this_year.to_csv(csv_name, index = False)

	print("Done fetching articles")
	


# Wait for 6 seconds
# Currently the API rate limit is 5 seconds
def wait():
	start = time.time()
	time.clock()
	elapsed = 0;
	while elapsed < 6:
		elapsed = time.time() - start
		time.sleep(1)


# Read in nyt_ai.csv which includes the number of articles per year (yyyy/08/13 to yyyy/08/12)
def getYearlyNumber():
	df = pd.read_csv('./DTA_AI_csv/nyt_ai.csv', names=['Year','NumArticles','Iterate'])
	#print(df)
	return(df)

runAPI()
