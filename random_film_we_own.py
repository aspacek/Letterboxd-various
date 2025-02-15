import sys
import csv
import requests
from pathlib import Path
import random

##################################
def findstrings(substring,string):
	lastfound = -1
	while True:
		lastfound = string.find(substring,lastfound+1)
		if lastfound == -1:  
			break
		yield lastfound

##################################################
def getstrings(which,prestring,poststring,source):
	# First find the start of the number of pages string:
	length = len(prestring)
	prevalue = list(findstrings(prestring,source))
	if len(prevalue) > 0:
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
	else:
		return ''
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

############################################
############################################

########################
# Acceptable genres are:
# 'actadv'
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
# 'romdram'
# 'science-fiction'
# 'thriller'
# 'tv-movie'
# 'war'
# 'western'
###########

# Grabs values entered through execution
# i.e. >>python user_film_compare.py input.txt
inputs = sys.argv
input = inputs[1]

# Read in an input file:
with open(input) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=' ',skipinitialspace=True)
	keyword = []
	equals = []
	parameter = []
	for row in csv_reader:
		if len(row) == 3:
			keyword = keyword+[row[0]]
			equals = equals+[row[1]]
			parameter = parameter+[row[2]]
# Get parameters:
for i in range(len(keyword)):
	# minyear
	if keyword[i] == 'minyear' and equals[i] == '=':
		minyear = int(parameter[i])
	# maxyear
	elif keyword[i] == 'maxyear' and equals[i] == '=':
		maxyear = int(parameter[i])
	# minrating
	elif keyword[i] == 'minrating' and equals[i] == '=':
		minrating = float(parameter[i])
	# maxrating
	elif keyword[i] == 'maxrating' and equals[i] == '=':
		maxrating = float(parameter[i])
	# minratingLetterboxd
	elif keyword[i] == 'minratingLetterboxd' and equals[i] == '=':
		minratingLetterboxd = float(parameter[i])
	# maxratingLetterboxd
	elif keyword[i] == 'maxratingLetterboxd' and equals[i] == '=':
		maxratingLetterboxd = float(parameter[i])
	# minpopularity
	elif keyword[i] == 'minpopularity' and equals[i] == '=':
		minpopularity = float(parameter[i])
	# maxpopularity
	elif keyword[i] == 'maxpopularity' and equals[i] == '=':
		maxpopularity = float(parameter[i])
	# minwatches
	elif keyword[i] == 'minwatches' and equals[i] == '=':
		minwatches = int(parameter[i])
	# maxwatches
	elif keyword[i] == 'maxwatches' and equals[i] == '=':
		maxwatches = int(parameter[i])
	# genre
	elif keyword[i] == 'genre' and equals[i] == '=':
		genre = parameter[i]
	# number
	elif keyword[i] == 'number' and equals[i] == '=':
		number = int(parameter[i])
	# director
	elif keyword[i] == 'director' and equals[i] == '=':
		director = parameter[i]
	# actor
	elif keyword[i] == 'actor' and equals[i] == '=':
		actor = parameter[i]
	# liked
	elif keyword[i] == 'liked' and equals[i] == '=':
		liked = int(parameter[i])
	# allnew
	elif keyword[i] == 'allnew' and equals[i] == '=':
		allnew = int(parameter[i])
	# newgenres
	elif keyword[i] == 'newgenres' and equals[i] == '=':
		newgenres = int(parameter[i])
	# newratingsLetterboxd
	elif keyword[i] == 'newratingsLetterboxd' and equals[i] == '=':
		newratingsLetterboxd = int(parameter[i])
	# newactors
	elif keyword[i] == 'newactors' and equals[i] == '=':
		newactors = int(parameter[i])
# Defaults, if parameters not found:
if 'minyear' not in locals():
	print('\nminyear not found in input file; minyear = 0 by default.')
	minyear = 0
if 'maxyear' not in locals():
	print('\nmaxyear not found in input file; maxyear = 0 by default.')
	maxyear = 0
if 'minrating' not in locals():
	print('\nminrating not found in input file; minrating = 0 by default.')
	minrating = 0
if 'maxrating' not in locals():
	print('\nmaxrating not found in input file; maxrating = 0 by default.')
	maxrating = 0
if 'minratingLetterboxd' not in locals():
	print('\nminratingLetterboxd not found in input file; minratingLetterboxd = 0 by default.')
	minratingLetterboxd = 0
if 'maxratingLetterboxd' not in locals():
	print('\nmaxratingLetterboxd not found in input file; maxratingLetterboxd = 0 by default.')
	maxratingLetterboxd = 0
if 'minpopularity' not in locals():
	print('\nminpopularity not found in input file; minpopularity = 0 by default.')
	minpopularity = 0
if 'maxpopularity' not in locals():
	print('\nmaxpopularity not found in input file; maxpopularity = 0 by default.')
	maxpopularity = 0
if 'minwatches' not in locals():
	print('\nminwatches not found in input file; minwatches = 0 by default.')
	minwatches = 0
if 'maxwatches' not in locals():
	print('\nmaxwatches not found in input file; maxwatches = 0 by default.')
	maxwatches = 0
if 'genre' not in locals():
	print('\ngenre not found in input file; genre = any by default.')
	genre = 'any'
if 'number' not in locals():
	print('\nnumber not found in input file; number = 1 by default.')
	number = 1
if 'director' not in locals():
	print('\ndirector not found in input file; director = none by default.')
	director = 'none'
if 'actor' not in locals():
	print('\nactor not found in input file; actor = none by default.')
	actor = 'none'
if 'liked' not in locals():
	print('\nliked not found in input file; liked = 0 by default.')
	liked = 0
if 'allnew' not in locals():
	print('\nallnew not found in input file; allnew = 0 by default.')
	allnew = 0
if 'newgenres' not in locals():
	print('\nnewgenres not found in input file; newgenres = 0 by default.')
	newgenres = 0
if 'newratingsLetterboxd' not in locals():
	print('\nnewratingsLetterboxd not found in input file; newratingsLetterboxd = 0 by default.')
	newgenres = 0
if 'newactors' not in locals():
	print('\nnewactors not found in input file; newactors = 0 by default.')
	newactors = 0

# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')

# If allnew = 0, check for previous film collection output:
collectionflag = 0
if allnew == 0:
	collectionpath = Path('Data/Collection.csv')
	print(collectionpath)
	print(collectionpath.exists())
	if collectionpath.exists():
		# If there is previous output, read it in:
		collectionflag = 1
		films = []
		years = []
		with open('Data/Collection.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films = films+[row[0]]
				years = years+[row[1]]
	# Make year values integers:
	years = [int(item) for item in years]
# Otherwise, grab info from internet:
if collectionflag == 0:
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
	films = films+getstrings('all','data-film-slug="','"',source)
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
			films = films+getstrings('all','data-film-slug="','"',source)
			years = years+getstrings('all','/films/year/','/">',source)
	# Make year values integers:
	years = [int(item) for item in years]
	# Make sure the lengths match:
	if len(films) != len(years):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of ratings')
	# Write out the data:
	with open('Data/Collection.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films)):
			csvwriter.writerow([films[i],years[i]])

# Status update:
print('\nNumber of films in collection: '+str(len(films)))
print('\nReading in Amanda\'s and Alex\'s film collection by popularity.')

# If allnew = 0, check for previous film collection popularity output:
popularityflag = 0
if allnew == 0:
	popularitypath = Path('Data/Popularity.csv')
	if popularitypath.exists():
		# If there is previous output, read it in:
		popularityflag = 1
		films3 = []
		popularity3 = []
		with open('Data/Popularity.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films3 = films3+[row[0]]
				popularity3 = popularity3+[row[1]]
	# Make popularity values floats:
	popularity3 = [float(item) for item in popularity3]
# Otherwise, grab info from internet:
if popularityflag == 0:
	# The base url of our film collection:
	url = 'https://letterboxd.com/moogic/list/moogics-dvd-collection/detail/by/popular/'
	# Grab source code for the first page:
	r = requests.get(url)
	source = r.text
	# Find the number of pages
	pages = int(getstrings('last','/moogic/list/moogics-dvd-collection/detail/by/popular/page/','/">',source))
	# Loop through all pages and grab all the film titles:
	pageflag = 0
	# Initialize results:
	films2 = []
	# Start on page 1, get the films:
	films2 = films2+getstrings('all','data-film-slug="','"',source)
	# Now loop through the rest of the pages:
	if pageflag == 0:
		for page in range(pages-1):
			# Start on page 2:
			page = str(page + 2)
			# Grab source code of the page:
			r = requests.get(url+'page/'+page+'/')
			source = r.text
			# Get films and years:
			films2 = films2+getstrings('all','data-film-slug="','"',source)
	# Compute the popularity percentiles:
	popularity2 = []
	for i in range(len(films2)):
		popularity2 = popularity2+[(len(films2)-i)/float(len(films2))*100]
	# Match original films with popularity values
	films3 = []
	popularity3 = []
	for i in range(len(films2)):
		flag = 0
		j = 0
		while flag == 0 and j < len(films2):
			if films[i] == films2[j]:
				flag = 1
				films3 = films3+[films[i]]
				popularity3 = popularity3+[popularity2[j]]
				del films2[j]
				del popularity2[j]
			j = j+1
		if flag == 0:
			sys.exit('ERROR - in function "MAIN" - There is a popularity value for an invalid film')
	# Make popularity values floats:
	popularity3 = [float(item) for item in popularity3]
	# Make sure the lengths match:
	if len(films) != len(popularity3):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of popularity values')
	if films != films3:
		sys.exit('ERROR - in function "MAIN" - Number of popularity films does not match number of films')
	# Write out the data:
	with open('Data/Popularity.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films3)):
			csvwriter.writerow([films3[i],popularity3[i]])

# Status update:
print('\nGetting genres for all collection films.')

# If newgenres = 0, check for previous film genre output:
newgenreflag = 0
if newgenres == 0:
	genrepath = Path('Data/Genres.csv')
	if genrepath.exists():
		newgenreflag = 1
		# If there is previous output, read it in:
		films4 = []
		years4 = []
		genres4 = []
		with open('Data/Genres.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films4 = films4+[row[0]]
				years4 = years4+[row[1]]
				genres4 = genres4+[row[2]]
# Go through all collection films, and either
# grab info from internet, or use previous info if available:
films5 = []
years5 = []
genres5 = []
for i in range(len(films)):
	# Check if previous info available:
	genreflag = 0
	if newgenres == 0 and newgenreflag == 1:
		if films[i] in films4:
			genreflag = 1
			films5 = films5+[films[i]]
			years5 = years5+[years[i]]
			genres5 = genres5+[genres4[films4.index(films[i])]]
	# If previous info not available, get it from the internet:
	if genreflag == 0:
		url = 'https://letterboxd.com/film/'+films[i]+'/genres/'
		# Grab source code for genre page:
		r = requests.get(url)
		source = r.text
		# Find the genres:
		genres = getstrings('all','"/films/genre/','/"',source)
		flag = 0
		genrestring = ''
		for j in range(len(genres)):
			genrestring = genrestring+genres[j]
			if j < len(genres)-1:
				genrestring = genrestring+' '
		films5 = films5+[films[i]]
		years5 = years5+[years[i]]
		genres5 = genres5+[genrestring]
# Make sure the lengths match:
if len(films5) != len(genres5):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of genres')
if len(films) != len(films5):
	sys.exit('ERROR - in function "MAIN" - Number of films with genres does not match number of films')
# Write out the data:
if newgenreflag == 0:
	with open('Data/Genres.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films5)):
			csvwriter.writerow([films5[i],years5[i],genres5[i]])

# Status update:
print('\nGetting all of Alex\'s film ratings.')

# If allnew = 0, check for previous film ratings output:
ratingsflag = 0
if allnew == 0:
	ratingspath = Path('Data/Ratings.csv')
	if ratingspath.exists():
		# If there is previous output, read it in:
		ratingsflag = 1
		films6 = []
		ratings6 = []
		with open('Data/Ratings.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films6 = films6+[row[0]]
				ratings6 = ratings6+[row[1]]
	# Make ratings values integers:
	ratings6 = [int(item) for item in ratings6]
# Otherwise, grab info from internet:
if ratingsflag == 0:
	# Grab all film ratings:
	# The base url of the user's film ratings:
	url = 'https://letterboxd.com/moogic/films/ratings/'
	# Grab source code for first ratings page:
	r = requests.get(url)
	source = r.text
	# Find the number of ratings pages:
	pages = int(getstrings('last','/moogic/films/ratings/page/','/"',source))
	# Loop through all pages and grab all the film titles:
	# Initialize results:
	films6 = []
	ratings6 = []
	# Start on page 1, get the films:
	films6 = films6+getstrings('all','data-film-slug="/film/','/"',source)
	# Do the same for ratings:
	ratings6 = ratings6+getstrings('all','rating rated-','">',source)
	# Now loop through the rest of the pages:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films:
		films6 = films6+getstrings('all','data-film-slug="/film/','/"',source)
		# Get ratings:
		ratings6 = ratings6+getstrings('all','rating rated-','">',source)
	# Make ratings values integers:
	ratings6 = [int(item) for item in ratings6]
	# Make sure the lengths match:
	if len(films6) != len(ratings6):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of ratings')
	# Write out the data:
	with open('Data/Ratings.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films6)):
			csvwriter.writerow([films6[i],ratings6[i]])

# Status update:
print('\nNumber of total ratings: '+str(len(films6)))
print('\nGetting the number of times films have been watched.')

# If allnew = 0, check for previous film watches output:
watchesflag = 0
if allnew == 0:
	watchespath = Path('Data/Watches.csv')
	if watchespath.exists():
		# If there is previous output, read it in:
		watchesflag = 1
		films7 = []
		watches7 = []
		with open('Data/Watches.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films7 = films7+[row[0]]
				watches7 = watches7+[row[1]]
	# Make watches values integers:
	watches7 = [int(item) for item in watches7]
# Otherwise, grab info from internet:
if watchesflag == 0:
	# Grab all film ratings:
	# The base url of the user's film ratings:
	url = 'https://letterboxd.com/moogic/list/moogics-most-watched-films/detail/'
	# Grab source code for first ratings page:
	r = requests.get(url)
	source = r.text
	# Find the number of ratings pages:
	pages = int(getstrings('last','/moogic/list/moogics-most-watched-films/detail/page/','/">',source))
	# Loop through all pages and grab all the film titles:
	# Initialize results:
	films7 = []
	watches7 = []
	# Start on page 1, get the films:
	films7 = films7+getstrings('all','data-film-slug="/film/','/"',source)
	# Do the same for watches:
	watches7 = watches7+getstrings('all','/"> <p>','</p>',source)
	# Now loop through the rest of the pages:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films:
		films7 = films7+getstrings('all','data-film-slug="/film/','/"',source)
		# Get watches:
		watches7 = watches7+getstrings('all','/"> <p>','</p>',source)
	# Make watches values integers:
	watches7 = [int(item) for item in watches7]
	# Make sure the lengths match:
	if len(films7) != len(watches7):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of films with multiple watches')
	# Write out the data:
	with open('Data/Watches.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films7)):
			csvwriter.writerow([films7[i],watches7[i]])

# Status update:
print('\nNumber of films watched more than once: '+str(len(films7)))
print('\nGetting average Letterboxd ratings for all collection films.')

# If newratingsLetterboxd = 0, check for previous Letterboxd rating output:
newLratingflag = 0
if newratingsLetterboxd == 0:
	Lratingpath = Path('Data/RatingsLetterboxd.csv')
	if Lratingpath.exists():
		newLratingflag = 1
		# If there is previous output, read it in:
		films8 = []
		Lratings8 = []
		with open('Data/RatingsLetterboxd.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films8 = films8+[row[0]]
				Lratings8 = Lratings8+[row[1]]
# Go through all collection films, and either
# grab info from internet, or use previous info if available:
films9 = []
Lratings9 = []
for i in range(len(films)):
	# Check if previous info available:
	Lratingflag = 0
	if newratingsLetterboxd == 0 and newLratingflag == 1:
		if films[i] in films8:
			Lratingflag = 1
			films9 = films9+[films[i]]
			Lratings9 = Lratings9+[Lratings8[films8.index(films[i])]]
	# If previous info not available, get it from the internet:
	if Lratingflag == 0:
		url = 'https://letterboxd.com/film/'+films[i]+'/'
		# Grab source code for genre page:
		r = requests.get(url)
		source = r.text
		# Find the Letterboxd ratings:
		Lrating = getstrings('first','"ratingValue":',',"',source)
		if Lrating == '':
			Lrating = -1.0
		else:
			Lrating = float(Lrating)
		films9 = films9+[films[i]]
		Lratings9 = Lratings9+[Lrating]
# Make Letterboxd ratings values floats:
Lratings9 = [float(item) for item in Lratings9]
# Make sure the lengths match:
if len(films9) != len(Lratings9):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of Letterboxd ratings')
if len(films) != len(films9):
	sys.exit('ERROR - in function "MAIN" - Number of films with Letterboxd ratings does not match number of films')
# Write out the data:
if newLratingflag == 0:
	with open('Data/RatingsLetterboxd.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films9)):
			csvwriter.writerow([films9[i],Lratings9[i]])

# Status update:
print('\nMatching film collection with ratings.')

# Match ratings if they exist, otherwise make them -1.0:
ratingscount = 0
newfilms = []
newyears = []
newpopularity = []
newgenres = []
newratings = []
newLratings = []
for i in range(len(films)):
	flag = 0
	j = 0
	while flag == 0 and j < len(films6):
		if films[i] == films6[j]:
			flag = 1
			newfilms = newfilms+[films[i]]
			newyears = newyears+[years[i]]
			newpopularity = newpopularity+[popularity3[i]]
			newgenres = newgenres+[genres5[i]]
			newratings = newratings+[ratings6[j]/2.0]
			newLratings = newLratings+[Lratings9[i]]
			del films6[j]
			del ratings6[j]
			ratingscount = ratingscount+1
		j = j+1
	if flag == 0:
		newfilms = newfilms+[films[i]]
		newyears = newyears+[years[i]]
		newpopularity = newpopularity+[popularity3[i]]
		newgenres = newgenres+[genres5[i]]
		newratings = newratings+[-1.0]
		newLratings = newLratings+[Lratings9[i]]
# Make sure the films match:
if films != newfilms:
	sys.exit('ERROR - in function "MAIN" - Collection films don\'t match after ratings matching')

# Status update:
print('\nNumber of collection that has been rated: '+str(ratingscount))
print('\nMatching collection with films watched multiple times.')

# Match watches if they exist,
# otherwise make them 1 if a rating exists,
# otherwise make them 0:
watchescount = 0
newerfilms = []
neweryears = []
newerpopularity = []
newergenres = []
newerratings = []
newerLratings = []
newerwatches = []
for i in range(len(newfilms)):
	flag = 0
	j = 0
	while flag == 0 and j < len(films7):
		if newfilms[i] == films7[j]:
			flag = 1
			newerfilms = newerfilms+[newfilms[i]]
			neweryears = neweryears+[newyears[i]]
			newerpopularity = newerpopularity+[newpopularity[i]]
			newergenres = newergenres+[newgenres[i]]
			newerratings = newerratings+[newratings[i]]
			newerLratings = newerLratings+[newLratings[i]]
			newerwatches = newerwatches+[watches7[j]]
			del films7[j]
			del watches7[j]
			watchescount = watchescount+1
		j = j+1
	if flag == 0:
		newerfilms = newerfilms+[newfilms[i]]
		neweryears = neweryears+[newyears[i]]
		newerpopularity = newerpopularity+[newpopularity[i]]
		newergenres = newergenres+[newgenres[i]]
		newerratings = newerratings+[newratings[i]]
		newerLratings = newerLratings+[newLratings[i]]
		if newratings[i] != -1:
			newerwatches = newerwatches+[1]
		else:
			newerwatches = newerwatches+[0]
# Make sure the films match:
if newfilms != newerfilms:
	sys.exit('ERROR - in function "MAIN" - Collection films don\'t match after watches matching')

# Status update:
print('\nNumber of collection that has been watched multiple times: '+str(watchescount))
print('\nLimiting years, if requested.')

# Limit years:
ycutfilms = []
ycutyears = []
ycutpopularity = []
ycutgenres = []
ycutratings = []
ycutLratings = []
ycutwatches = []
if minyear != 0 or maxyear != 0:
	if maxyear == 0:
		maxyear = 3000
	for i in range(len(newerfilms)):
		if neweryears[i] >= minyear and neweryears[i] <= maxyear:
			ycutfilms = ycutfilms+[newerfilms[i]]
			ycutyears = ycutyears+[neweryears[i]]
			ycutpopularity = ycutpopularity+[newerpopularity[i]]
			ycutgenres = ycutgenres+[newergenres[i]]
			ycutratings = ycutratings+[newerratings[i]]
			ycutLratings = ycutLratings+[newerLratings[i]]
			ycutwatches = ycutwatches+[newerwatches[i]]
else:
	ycutfilms = [item for item in newerfilms]
	ycutyears = [item for item in neweryears]
	ycutpopularity = [item for item in newerpopularity]
	ycutgenres = [item for item in newergenres]
	ycutratings = [item for item in newerratings]
	ycutLratings = [item for item in newerLratings]
	ycutwatches = [item for item in newerwatches]
if len(ycutfilms) == 0:
	sys.exit('ERROR - in function "MAIN" - No films in the year range given')

# Status update:
print('\nNumber fitting year criterion: '+str(len(ycutfilms)))
print('\nLimiting ratings, if requested.')

# Limit ratings:
rcutfilms = []
rcutyears = []
rcutpopularity = []
rcutgenres = []
rcutratings = []
rcutLratings = []
rcutwatches = []
if minrating != 0 or maxrating != 0:
	if maxrating == 0:
		maxrating = 5
	for i in range(len(ycutfilms)):
		if ycutratings[i] >= minrating and ycutratings[i] <= maxrating:
			rcutfilms = rcutfilms+[ycutfilms[i]]
			rcutyears = rcutyears+[ycutyears[i]]
			rcutpopularity = rcutpopularity+[ycutpopularity[i]]
			rcutgenres = rcutgenres+[ycutgenres[i]]
			rcutratings = rcutratings+[ycutratings[i]]
			rcutLratings = rcutLratings+[ycutLratings[i]]
			rcutwatches = rcutwatches+[ycutwatches[i]]
	if len(rcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the rating range given')
# Otherwise, just keep all of the films:
else:
	rcutfilms = [item for item in ycutfilms]
	rcutyears = [item for item in ycutyears]
	rcutpopularity = [item for item in ycutpopularity]
	rcutgenres = [item for item in ycutgenres]
	rcutratings = [item for item in ycutratings]
	rcutLratings = [item for item in ycutLratings]
	rcutwatches = [item for item in ycutwatches]

# Status update:
print('\nNumber fitting rating criterion: '+str(len(rcutfilms)))
print('\nLimiting Letterboxd ratings, if requested.')

# Limit Letterboxd ratings:
Lcutfilms = []
Lcutyears = []
Lcutpopularity = []
Lcutgenres = []
Lcutratings = []
LcutLratings = []
Lcutwatches = []
if minratingLetterboxd != 0 or maxratingLetterboxd != 0:
	if maxratingLetterboxd == 0:
		maxratingLetterboxd = 5
	for i in range(len(rcutfilms)):
		if rcutLratings[i] >= minratingLetterboxd and rcutLratings[i] <= maxratingLetterboxd:
			Lcutfilms = Lcutfilms+[rcutfilms[i]]
			Lcutyears = Lcutyears+[rcutyears[i]]
			Lcutpopularity = Lcutpopularity+[rcutpopularity[i]]
			Lcutgenres = Lcutgenres+[rcutgenres[i]]
			Lcutratings = Lcutratings+[rcutratings[i]]
			LcutLratings = LcutLratings+[rcutLratings[i]]
			Lcutwatches = Lcutwatches+[rcutwatches[i]]
	if len(Lcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the Letterboxd rating range given')
# Otherwise, just keep all of the films:
else:
	Lcutfilms = [item for item in rcutfilms]
	Lcutyears = [item for item in rcutyears]
	Lcutpopularity = [item for item in rcutpopularity]
	Lcutgenres = [item for item in rcutgenres]
	Lcutratings = [item for item in rcutratings]
	LcutLratings = [item for item in rcutLratings]
	Lcutwatches = [item for item in rcutwatches]

# Status update:
print('\nNumber fitting Letterboxd rating criterion: '+str(len(Lcutfilms)))
print('\nLimiting genres, if requested.')

# Limit genres:
gcutfilms = []
gcutyears = []
gcutpopularity = []
gcutgenres = []
gcutratings = []
gcutLratings = []
gcutwatches = []
if genre != 'any':
	for i in range(len(Lcutfilms)):
		genres = Lcutgenres[i].split(' ')
		flag1 = 0
		flag2 = 0
		for j in range(len(genres)):
			if genre == genres[j]:
				gcutfilms = gcutfilms+[Lcutfilms[i]]
				gcutyears = gcutyears+[Lcutyears[i]]
				gcutpopularity = gcutpopularity+[Lcutpopularity[i]]
				gcutgenres = gcutgenres+[Lcutgenres[i]]
				gcutratings = gcutratings+[Lcutratings[i]]
				gcutLratings = gcutLratings+[LcutLratings[i]]
				gcutwatches = gcutwatches+[Lcutwatches[i]]
			elif genre == 'romcom':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'comedy':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutpopularity = gcutpopularity+[Lcutpopularity[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
					gcutwatches = gcutwatches+[Lcutwatches[i]]
			elif genre == 'romdram':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'drama':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutpopularity = gcutpopularity+[Lcutpopularity[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
					gcutwatches = gcutwatches+[Lcutwatches[i]]
			elif genre == 'actadv':
				if genres[j] == 'action':
					flag1 = 1
				elif genres[j] == 'adventure':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutpopularity = gcutpopularity+[Lcutpopularity[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
					gcutwatches = gcutwatches+[Lcutwatches[i]]
# Otherwise, just keep all of the films:
else:
	gcutfilms = [item for item in Lcutfilms]
	gcutyears = [item for item in Lcutyears]
	gcutpopularity = [item for item in Lcutpopularity]
	gcutgenres = [item for item in Lcutgenres]
	gcutratings = [item for item in Lcutratings]
	gcutLratings = [item for item in LcutLratings]
	gcutwatches = [item for item in Lcutwatches]

# Status update:
print('\nNumber fitting genre criterion: '+str(len(gcutfilms)))
print('\nGetting directors and actors for all remaining films, if requested.')

# Deal with directors or actors, if requested:
if director != 'none' or actor != 'none' or newactors == 1:
	newactorflag = 0
	# If newactors = 0, check for previous film actor output:
	if newactors == 0:
		actorpath = Path('Data/Actors.csv')
		if actorpath.exists():
			newactorflag = 1
			# If there is previous output, read it in:
			films10 = []
			directors10 = []
			actors10 = []
			with open('Data/Actors.csv') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for row in csv_reader:
					films10 = films10+[row[0]]
					directors10 = directors10+[row[1]]
					actors10 = actors10+[row[2]]
	# Go through all collection films, and either
	# grab info from internet, or use previous info if available:
	films11 = []
	directors11 = []
	actors11 = []
	for i in range(len(gcutfilms)):
		# Check if previous info available:
		actorflag = 0
		if newactors == 0 and newactorflag == 1:
			if gcutfilms[i] in films10:
				actorflag = 1
				films11 = films11+[gcutfilms[i]]
				directors11 = directors11+[directors10[films10.index(gcutfilms[i])]]
				actors11 = actors11+[actors10[films10.index(gcutfilms[i])]]
		# If previous info not available, get it from the internet:
		if actorflag == 0:
			url = 'https://letterboxd.com/film/'+gcutfilms[i]+'/'
			# Grab source code for genre page:
			r = requests.get(url)
			source = r.text
			# Find the directors:
			directors1 = getstrings('all','Directed by <a href="/director/','/">',source)
			directors2 = getstrings('all',', <a href="/director/','/">',source)
			directors = directors1+directors2
			flag = 0
			directorstring = ''
			for j in range(len(directors)):
				directorstring = directorstring+directors[j]
				if j < len(directors)-1:
					directorstring = directorstring+' '
			# Find the actors:
			actors = getstrings('all','href="/actor/','/" class',source)
			flag = 0
			actorstring = ''
			for j in range(len(actors)):
				actorstring = actorstring+actors[j]
				if j < len(actors)-1:
					actorstring = actorstring+' '
			films11 = films11+[gcutfilms[i]]
			directors11 = directors11+[directorstring]
			actors11 = actors11+[actorstring]
	# Make sure the lengths match:
	if len(films11) != len(actors11):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of actors')
	# Make sure films6 is identical to gcutfilms:
	if films11 != gcutfilms:
		sys.exit('ERROR - in function "MAIN" - Director/actor film array not the same as the previous film array')
	# Write out the data:
	if newactors == 1:
		with open('Data/Actors.csv', mode='w') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in range(len(films11)):
				csvwriter.writerow([films11[i],directors11[i],actors11[i]])
# Otherwise just make them empty arrays:
else:
	directors11 = []
	actors11 = []

# Status update:
print('\nLimiting directors, if requested.')

# Limit directors:
dcutfilms = []
dcutyears = []
dcutpopularity = []
dcutgenres = []
dcutratings = []
dcutLratings = []
dcutwatches = []
dcutdirectors = []
dcutactors = []
if director != 'none':
	for i in range(len(gcutfilms)):
		directors = directors11[i].split(' ')
		for j in range(len(directors)):
			if director == directors[j]:
				dcutfilms = dcutfilms+[gcutfilms[i]]
				dcutyears = dcutyears+[gcutyears[i]]
				dcutpopularity = dcutpopularity+[gcutpopularity[i]]
				dcutgenres = dcutgenres+[gcutgenres[i]]
				dcutratings = dcutratings+[gcutratings[i]]
				dcutLratings = dcutLratings+[gcutLratings[i]]
				dcutwatches = dcutwatches+[gcutwatches[i]]
				dcutdirectors = dcutdirectors+[directors11[i]]
				dcutactors = dcutactors+[actors11[i]]
# Otherwise, just keep all of the films:
else:
	dcutfilms = [item for item in gcutfilms]
	dcutyears = [item for item in gcutyears]
	dcutpopularity = [item for item in gcutpopularity]
	dcutgenres = [item for item in gcutgenres]
	dcutratings = [item for item in gcutratings]
	dcutLratings = [item for item in gcutLratings]
	dcutwatches = [item for item in gcutwatches]
	dcutdirectors = [item for item in directors11]
	dcutactors = [item for item in actors11]

# Status update:
print('\nNumber fitting director criterion: '+str(len(dcutfilms)))
print('\nLimiting actors, if requested.')

# Limit actors:
acutfilms = []
acutyears = []
acutpopularity = []
acutgenres = []
acutratings = []
acutLratings = []
acutwatches = []
acutdirectors = []
acutactors = []
if actor != 'none':
	for i in range(len(dcutfilms)):
		actors = dcutactors[i].split(' ')
		for j in range(len(actors)):
			if actor == actors[j]:
				acutfilms = acutfilms+[dcutfilms[i]]
				acutyears = acutyears+[dcutyears[i]]
				acutpopularity = acutpopularity+[dcutpopularity[i]]
				acutgenres = acutgenres+[dcutgenres[i]]
				acutratings = acutratings+[dcutratings[i]]
				acutLratings = acutLratings+[dcutLratings[i]]
				acutwatches = acutwatches+[dcutwatches[i]]
				acutdirectors = acutdirectors+[dcutdirectors[i]]
				acutactors = acutactors+[dcutactors[i]]
# Otherwise, just keep all of the films:
else:
	acutfilms = [item for item in dcutfilms]
	acutyears = [item for item in dcutyears]
	acutpopularity = [item for item in dcutpopularity]
	acutgenres = [item for item in dcutgenres]
	acutratings = [item for item in dcutratings]
	acutLratings = [item for item in dcutLratings]
	acutwatches = [item for item in dcutwatches]
	acutdirectors = [item for item in dcutdirectors]
	acutactors = [item for item in dcutactors]

# Status update:
print('\nNumber fitting actor criterion: '+str(len(acutfilms)))
print('\nLimiting popularity, if requested.')

# Limit popularity:
pcutfilms = []
pcutyears = []
pcutpopularity = []
pcutgenres = []
pcutratings = []
pcutLratings = []
pcutwatches = []
pcutdirectors = []
pcutactors = []
if minpopularity != 0 or maxpopularity != 0:
	if maxpopularity == 0:
		maxpopularity = 100
	for i in range(len(acutfilms)):
		if acutpopularity[i] >= minpopularity and acutpopularity[i] <= maxpopularity:
			pcutfilms = pcutfilms+[acutfilms[i]]
			pcutyears = pcutyears+[acutyears[i]]
			pcutpopularity = pcutpopularity+[acutpopularity[i]]
			pcutgenres = pcutgenres+[acutgenres[i]]
			pcutratings = pcutratings+[acutratings[i]]
			pcutLratings = pcutLratings+[acutLratings[i]]
			pcutwatches = pcutwatches+[acutwatches[i]]
			if director != 'none':
				pcutdirectors = pcutdirectors+[acutdirectors[i]]
			if actor != 'none':
				pcutactors = pcutactors+[acutactors[i]]
	if len(pcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the popularity range given')
# Otherwise, just keep all of the films:
else:
	pcutfilms = [item for item in acutfilms]
	pcutyears = [item for item in acutyears]
	pcutpopularity = [item for item in acutpopularity]
	pcutgenres = [item for item in acutgenres]
	pcutratings = [item for item in acutratings]
	pcutLratings = [item for item in acutLratings]
	pcutwatches = [item for item in acutwatches]
	pcutdirectors = [item for item in acutdirectors]
	pcutactors = [item for item in acutactors]

# Status update:
print('\nNumber fitting popularity criterion: '+str(len(pcutfilms)))
print('\nLimiting by film watches, if requested.')

# Limit by watches:
wcutfilms = []
wcutyears = []
wcutpopularity = []
wcutgenres = []
wcutratings = []
wcutLratings = []
wcutwatches = []
wcutdirectors = []
wcutactors = []
if minwatches != 0 or maxwatches != 0:
	if maxwatches == 0:
		maxwatches = 1000
	for i in range(len(pcutfilms)):
		if pcutwatches[i] >= minwatches and pcutwatches[i] <= maxwatches:
			wcutfilms = wcutfilms+[pcutfilms[i]]
			wcutyears = wcutyears+[pcutyears[i]]
			wcutpopularity = wcutpopularity+[pcutpopularity[i]]
			wcutgenres = wcutgenres+[pcutgenres[i]]
			wcutratings = wcutratings+[pcutratings[i]]
			wcutLratings = wcutLratings+[pcutLratings[i]]
			wcutwatches = wcutwatches+[pcutwatches[i]]
			if director != 'none':
				wcutdirectors = wcutdirectors+[pcutdirectors[i]]
			if actor != 'none':
				wcutactors = wcutactors+[pcutactors[i]]
	if len(wcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the watches range given')
# Otherwise, just keep all of the films:
else:
	wcutfilms = [item for item in pcutfilms]
	wcutyears = [item for item in pcutyears]
	wcutpopularity = [item for item in pcutpopularity]
	wcutgenres = [item for item in pcutgenres]
	wcutratings = [item for item in pcutratings]
	wcutLratings = [item for item in pcutLratings]
	wcutwatches = [item for item in pcutwatches]
	wcutdirectors = [item for item in pcutdirectors]
	wcutactors = [item for item in pcutactors]

# Status update:
print('\nNumber fitting watches criterion: '+str(len(wcutfilms)))
print('\nGetting all of Alex\'s liked films.')

# If allnew = 0, check for previous liked films output:
likesflag = 0
if allnew == 0:
	likespath = Path('Data/Likes.csv')
	if likespath.exists():
		# If there is previous output, read it in:
		likesflag = 1
		films12 = []
		with open('Data/Likes.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films12 = films12+[row[0]]
# Otherwise, grab info from internet:
if likesflag == 0:
	# Grab all film ratings:
	# The base url of the user's film ratings:
	url = 'https://letterboxd.com/moogic/list/films-i-especially-like/detail/'
	# Grab source code for first ratings page:
	r = requests.get(url)
	source = r.text
	# Find the number of ratings pages:
	pages = int(getstrings('last','/moogic/list/films-i-especially-like/detail/page/','/"',source))
	# Loop through all pages and grab all the film titles:
	# Initialize results:
	films12 = []
	# Start on page 1, get the films:
	films12 = films12+getstrings('all','data-film-slug="/film/','/"',source)
	# Now loop through the rest of the pages:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films:
		films12 = films12+getstrings('all','data-film-slug="/film/','/"',source)
	# Write out the data:
	with open('Data/Likes.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films12)):
			csvwriter.writerow([films12[i]])

# Status update:
print('\nNumber of total liked films: '+str(len(films12)))
print('\nMatching films with likes.')

# Match liked films if they exist
likescount = 0
newestfilms = []
newestyears = []
newestpopularity = []
newestgenres = []
newestratings = []
newestLratings = []
newestwatches = []
newestdirectors = []
newestactors = []
newestlikes = []
for i in range(len(wcutfilms)):
	flag = 0
	j = 0
	while flag == 0 and j < len(films12):
		if wcutfilms[i] == films12[j]:
			flag = 1
			newestfilms = newestfilms+[wcutfilms[i]]
			newestyears = newestyears+[wcutyears[i]]
			newestpopularity = newestpopularity+[wcutpopularity[i]]
			newestgenres = newestgenres+[wcutgenres[i]]
			newestratings = newestratings+[wcutratings[i]]
			newestLratings = newestLratings+[wcutLratings[i]]
			newestwatches = newestwatches+[wcutwatches[i]]
			if director != 'none':
				newestdirectors = newestdirectors+[wcutdirectors[i]]
			if actor != 'none':
				newestactors = newestactors+[wcutactors[i]]
			del films12[j]
			newestlikes = newestlikes+[1]
			likescount = likescount+1
		j = j+1
	if flag == 0:
		newestfilms = newestfilms+[wcutfilms[i]]
		newestyears = newestyears+[wcutyears[i]]
		newestpopularity = newestpopularity+[wcutpopularity[i]]
		newestgenres = newestgenres+[wcutgenres[i]]
		newestratings = newestratings+[wcutratings[i]]
		newestLratings = newestLratings+[wcutLratings[i]]
		newestwatches = newestwatches+[wcutwatches[i]]
		if director != 'none':
			newestdirectors = newestdirectors+[wcutdirectors[i]]
		if actor != 'none':
			newestactors = newestactors+[wcutactors[i]]
		newestlikes = newestlikes+[0]
# Make sure the films match:
if wcutfilms != newestfilms:
	sys.exit('ERROR - in function "MAIN" - Collection films don\'t match after likes matching')

# Status update:
print('\nNumber of collection films with likes: '+str(likescount))
print('\nLimiting by film likes, if requested.')

# Limit by likes:
likecutfilms = []
likecutyears = []
likecutpopularity = []
likecutgenres = []
likecutratings = []
likecutLratings = []
likecutwatches = []
likecutdirectors = []
likecutactors = []
likecutlikes = []
if liked == 1:
	for i in range(len(newestfilms)):
		if newestlikes[i] == 1:
			likecutfilms = likecutfilms+[newestfilms[i]]
			likecutyears = likecutyears+[newestyears[i]]
			likecutpopularity = likecutpopularity+[newestpopularity[i]]
			likecutgenres = likecutgenres+[newestgenres[i]]
			likecutratings = likecutratings+[newestratings[i]]
			likecutLratings = likecutLratings+[newestLratings[i]]
			likecutwatches = likecutwatches+[newestwatches[i]]
			if director != 'none':
				likecutdirectors = likecutdirectors+[newestdirectors[i]]
			if actor != 'none':
				likecutactors = likecutactors+[newestactors[i]]
			likecutlikes = likecutlikes+[newestlikes[i]]
	if len(likecutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No remaining films with likes')
# Otherwise, just keep all of the films:
else:
	likecutfilms = [item for item in newestfilms]
	likecutyears = [item for item in newestyears]
	likecutpopularity = [item for item in newestpopularity]
	likecutgenres = [item for item in newestgenres]
	likecutratings = [item for item in newestratings]
	likecutLratings = [item for item in newestLratings]
	likecutwatches = [item for item in newestwatches]
	likecutdirectors = [item for item in newestdirectors]
	likecutactors = [item for item in newestactors]
	likecutlikes = [item for item in newestlikes]

# Status update:
print('\nNumber fitting likes criterion: '+str(len(likecutfilms)))
print('\nRequested films obtained. Choosing one randomly.')

# Denote the final result arrays:
finalfilms = [item for item in likecutfilms]
finalyears = [item for item in likecutyears]
finalpopularity = [item for item in likecutpopularity]
finalgenres = [item for item in likecutgenres]
finalratings = [item for item in likecutratings]
finalLratings = [item for item in likecutLratings]
finalwatches = [item for item in likecutwatches]
finaldirectors = [item for item in likecutdirectors]
finalactors = [item for item in likecutactors]
finallikes = [item for item in likecutlikes]

# Grab a random "number" of films:
random.seed()
if len(finalfilms) < number:
	number = len(finalfilms)
choice = []
year = []
popularity = []
genre = []
rating = []
Lrating = []
watches = []
likes = []
aflag = 0
dflag = 0
if director != 'none':
	dflag = 1
	director = []
if actor != 'none':
	aflag = 1
	actor = []
for i in range(number):
	flag = 0
	while flag == 0:
		thischoice = random.choice(finalfilms)
		if thischoice not in choice:
			flag = 1
	choice = choice+[thischoice]
	# Get the year, genre, rating, directors, actors:
	year = year+[finalyears[finalfilms.index(thischoice)]]
	popularity = popularity+[finalpopularity[finalfilms.index(thischoice)]]
	genre = genre+[finalgenres[finalfilms.index(thischoice)]]
	rating = rating+[finalratings[finalfilms.index(thischoice)]]
	Lrating = Lrating+[finalLratings[finalfilms.index(thischoice)]]
	watches = watches+[finalwatches[finalfilms.index(thischoice)]]
	likes = likes+[finallikes[finalfilms.index(thischoice)]]
	if dflag == 1:
		director = director+[finaldirectors[finalfilms.index(thischoice)]]
	if aflag == 1:
		actor = actor+[finalactors[finalfilms.index(thischoice)]]

# Print out the result:
print('\n********************')
if dflag == 0 and aflag == 0:
	for i in range(len(choice)):
		if likes[i] == 1:
			like = 'liked'
		else:
			like = 'no like'
		if rating[i] == -1.0:
			print('{} -- y:{:d} -- r:no rating -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {}'.format(choice[i],year[i],Lrating[i],popularity[i],watches[i],genre[i]))
		else:
			print('{} -- y:{:d} -- r:{:.1f}/5.0 -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],popularity[i],watches[i],like,genre[i]))
elif dflag == 1 and aflag == 0:
	for i in range(len(choice)):
		if likes[i] == 1:
			like = 'liked'
		else:
			like = 'no like'
		if rating[i] == -1.0:
			print('{} -- y:{:d} -- r:no rating -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {}'.format(choice[i],year[i],Lrating[i],popularity[i],watches[i],genre[i],director[i]))
		else:
			print('{} -- y:{:d} -- r:{:.1f}/5.0 -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],popularity[i],watches[i],like,genre[i],director[i]))
elif dflag == 0 and aflag == 1:
	for i in range(len(choice)):
		if likes[i] == 1:
			like = 'liked'
		else:
			like = 'no like'
		actors = actor[i].split(' ')
		if len(actors) < 5:
			n = len(actors)
		else:
			n = 5
		actor5 = ''
		for j in range(n):
			actor5 = actor5+actors[j]+' '
		if rating[i] == -1.0:
			print('{} -- y:{:d} -- r:no rating -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {}'.format(choice[i],year[i],Lrating[i],popularity[i],watches[i],genre[i],actor5))
		else:
			print('{} -- y:{:d} -- r:{:.1f}/5.0 -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],popularity[i],watches[i],like,genre[i],actor5))
elif dflag == 1 and aflag == 1:
	for i in range(len(choice)):
		if likes[i] == 1:
			like = 'liked'
		else:
			like = 'no like'
		actors = actor[i].split(' ')
		if len(actors) < 5:
			n = len(actors)
		else:
			n = 5
		actor5 = ''
		for j in range(n):
			actor5 = actor5+actors[j]+' '
		if rating[i] == -1.0:
			print('{} -- y:{:d} -- r:no rating -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {} -- {}'.format(choice[i],year[i],Lrating[i],popularity[i],watches[i],genre[i],director[i],actor5))
		else:
			print('{} -- y:{:d} -- r:{:.1f}/5.0 -- Lr:{:.2f}/5.00 -- p:{:.1f} -- w:{:d} -- {} -- {} -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],popularity[i],watches[i],like,genre[i],director[i],actor5))
print('********************\n')
