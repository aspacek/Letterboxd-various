import sys
import requests
import random

def findstrings(substring,string):
	lastfound = -1
	while True:
		lastfound = string.find(substring,lastfound+1)
		if lastfound == -1:  
			break
		yield lastfound

def getstrings(which,prestring,poststring,source):
	# First find the start of the number of pages string:
	length = len(prestring)
	prevalue = list(findstrings(prestring,source))
	# If first instance wanted:
	if which == 'first':
		prevalue = [prevalue[0]+length]
	# If last instance wanted:
	elif which == 'last':
		prevalue = [prevalue[-1]+length]
	# If all instances wanted:
	elif which == 'all':
		prevalue = [item+length for item in prevalue]
	else:
		sys.exit('ERROR - in function "getstrings" - Invalid input for "which"')
	# Find the location of the end of string, and get the strings:
	strings = []
	for beginning in prevalue:
		end = source.find(poststring,beginning)
		value = source[beginning:end]
		strings = strings+[value]
	# If just one string desired, return a scalar, otherwise return the array:
	if which == 'first' or which == 'last':
		return strings[0]
	elif which == 'all':
		return strings

# Grabs values entered through execution
# i.e. >>python user_film_compare.py <year min> <year max> <rating min> <rating max> <unrated?> <genre>
inputs = sys.argv
minyear = int(inputs[1])
maxyear = int(inputs[2])
minrating = float(inputs[3])
maxrating = float(inputs[4])
dounrated = int(inputs[5])
genre = inputs[6]

# Acceptable genres are:
# 'action'
# 'adventure'
# 'animation'
# 'comedy'
# 'crime'
# 'documentary'
# 'drama'
# 'family'
# 'fantasy'
# 'history'
# 'horror'
# 'music'
# 'mystery'
# 'romance'
# 'romcom'
# 'science-fiction'
# 'thriller'
# 'tv-movie'
# 'war'
# 'western'

# Check inputs:
if dounrated == 1 and minrating != 0:
	sys.exit('ERROR - in function "MAIN" - Can\'t input min/max ratings if dounrated = 1')
elif dounrated == 1 and maxrating != 0:
	sys.exit('ERROR - in function "MAIN" - Can\'t input min/max ratings if dounrated = 1')

# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')

# The base url of our film collection:
url = 'https://letterboxd.com/moogic/list/moogics-dvd-collection/detail/'
# Grab source code for the first page:
r = requests.get(url)
source = r.text

# Find the number of pages
pages = int(getstrings('last','/moogic/list/moogics-dvd-collection/detail/page/','/">',source))

# Loop through all pages and grab all the film titles:
pageflag = 0
# Initialize results:
films = []
years = []
# Start on page 1, get the films and years:
films = films+getstrings('all','data-film-slug="/film/','/"',source)
years = years+getstrings('all','/films/year/','/">',source)
# Now loop through the rest of the pages:
if pageflag == 0:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films and years:
		films = films+getstrings('all','data-film-slug="/film/','/"',source)
		years = years+getstrings('all','/films/year/','/">',source)
# Make year values integers:
years = [int(item) for item in years]

# Make sure the lengths match:
if len(films) != len(years):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of ratings')

# Status update:
print('\nLimiting years, if requested.')

# Limit years:
cutfilms = []
cutyears = []
if minyear != 0 or maxyear != 0:
	if maxyear == 0:
		maxyear = 3000
	for i in range(len(films)):
		if years[i] >= minyear and years[i] <= maxyear:
			cutfilms = cutfilms+[films[i]]
			cutyears = cutyears+[years[i]]
else:
	cutfilms = [item for item in films]
	cutyears = [item for item in years]
if len(cutfilms) == 0:
	sys.exit('ERROR - in function "MAIN" - No films in the year range given')

# Status update:
print('\nGetting all of Alex\'s film ratings.')

# Grab all film ratings:
# The base url of the user's film ratings:
url2 = 'https://letterboxd.com/moogic/films/ratings/'
# Grab source code for first ratings page:
r2 = requests.get(url2)
source2 = r2.text
# Find the number of ratings pages:
pages2 = int(getstrings('last','/moogic/films/ratings/page/','/"',source2))
# Loop through all pages and grab all the film titles:
# Initialize results:
films2 = []
ratings2 = []
# Start on page 1, get the films:
films2 = films2+getstrings('all','data-film-slug="/film/','/"',source2)
# Do the same for ratings:
ratings2 = ratings2+getstrings('all','rating rated-','">',source2)
# Now loop through the rest of the pages:
for page in range(pages2-1):
	# Start on page 2:
	page = str(page + 2)
	# Grab source code of the page:
	r2 = requests.get(url2+'page/'+page+'/')
	source2 = r2.text
	# Get films:
	films2 = films2+getstrings('all','data-film-slug="/film/','/"',source2)
	# Get ratings:
	ratings2 = ratings2+getstrings('all','rating rated-','">',source2)
# Make ratings values integers:
ratings2 = [int(item) for item in ratings2]

# Make sure the lengths match:
if len(films2) != len(ratings2):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of ratings')

# Status update:
print('\nMatching film collection with ratings.')

# Match ratings if they exist, otherwise make them -1.0:
newfilms = []
newyears = []
newratings = []
for i in range(len(cutfilms)):
	flag = 0
	j = 0
	while flag == 0 and j < len(films2):
		if cutfilms[i] == films2[j]:
			flag = 1
			newfilms = newfilms+[cutfilms[i]]
			newyears = newyears+[cutyears[i]]
			newratings = newratings+[ratings2[j]/2.0]
			del films2[j]
			del ratings2[j]
		j = j+1
	if flag == 0:
		newfilms = newfilms+[cutfilms[i]]
		newyears = newyears+[cutyears[i]]
		newratings = newratings+[-1.0]

# Status update:
print('\nLimiting ratings, if requested.')

# Limit ratings?
finalfilms = []
finalyears = []
finalratings = []
if minrating != 0 or maxrating != 0:
	for i in range(len(newfilms)):
		if newratings[i] >= minrating and newratings[i] <= maxrating:
			finalfilms = finalfilms+[newfilms[i]]
			finalyears = finalyears+[newyears[i]]
			finalratings = finalratings+[newratings[i]]
	if len(finalfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the rating range given')
# Otherwise, unrated films only?:
elif dounrated == 1:
	for i in range(len(newfilms)):
		if newratings[i] == -1:
			finalfilms = finalfilms+[newfilms[i]]
			finalyears = finalyears+[newyears[i]]
			finalratings = finalratings+[newratings[i]]
# Otherwise, just keep all of the films:
else:
	finalfilms = [item for item in newfilms]
	finalyears = [item for item in newyears]
	finalratings = [item for item in newratings]

# Status update:
print('\nGetting genres for all remaining films.')

# Grab genres for every remaining film and check them:
finalfilms2 = []
finalyears2 = []
finalratings2 = []
finalgenres2 = []
for i in range(len(finalfilms)):
	url3 = 'https://letterboxd.com/film/'+finalfilms[i]+'/genres/'
	# Grab source code for genre page:
	r3 = requests.get(url3)
	source3 = r3.text
	# Find the genres:
	genres3 = getstrings('all','"/films/genre/','/"',source3)
	# If genre requested:
	if genre != 'any':
		if genre == 'romcom':
			romflag = 0
			comflag = 0
			genrestring = ''
			for j in range(len(genres3)):
				genrestring = genrestring+genres3[j]
				if j < len(genres3)-1:
					genrestring = genrestring+', '
				if genres3[j] == 'romance':
					romflag = 1
				elif genres3[j] == 'comedy':
					comflag = 1
				if romflag == 1 and comflag == 1 and j == len(genres3)-1:
					finalfilms2 = finalfilms2+[finalfilms[i]]
					finalyears2 = finalyears2+[finalyears[i]]
					finalratings2 = finalratings2+[finalratings[i]]
					finalgenres2 = finalgenres2+[genrestring]
		else:
			flag = 0
			genrestring = ''
			for j in range(len(genres3)):
				genrestring = genrestring+genres3[j]
				if j < len(genres3)-1:
					genrestring = genrestring+', '
				if genres3[j] == genre:
					flag = 1
				if flag == 1 and j == len(genres3)-1:
					finalfilms2 = finalfilms2+[finalfilms[i]]
					finalyears2 = finalyears2+[finalyears[i]]
					finalratings2 = finalratings2+[finalratings[i]]
					finalgenres2 = finalgenres2+[genrestring]
		if len(finalfilms2) == 0:
			sys.exit('ERROR - in function "MAIN" - No films match the genre given')
	# Otherwise just record them all together (if there's more than one):
	else:
		genrestring = ''
		for j in range(len(genres3)):
			genrestring = genrestring+genres3[j]
			if j < len(genres3)-1:
				genrestring = genrestring+', '
		finalfilms2 = finalfilms2+[finalfilms[i]]
		finalyears2 = finalyears2+[finalyears[i]]
		finalratings2 = finalratings2+[finalratings[i]]
		finalgenres2 = finalgenres2+[genrestring]

# Status update:
print('\nRequested films obtained. Choosing one randomly.')

# Grab a random film:
random.seed()
choice = random.choice(finalfilms2)
# Get the year and rating:
year = finalyears2[finalfilms2.index(choice)]
rating = finalratings2[finalfilms2.index(choice)]
xgenre = finalgenres2[finalfilms2.index(choice)]

# Print out the result:
if rating == -1.0:
	print('\n{} -- {:d} -- no rating -- {}\n'.format(choice,year,xgenre))
else:
	print('\n{} -- {:d} -- {:.1f}/5 -- {}\n'.format(choice,year,rating,xgenre))
