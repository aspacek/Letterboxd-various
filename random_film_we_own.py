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
	# genre
	elif keyword[i] == 'genre' and equals[i] == '=':
		genre = parameter[i]
	# allnew
	elif keyword[i] == 'allnew' and equals[i] == '=':
		allnew = int(parameter[i])
	# newgenres
	elif keyword[i] == 'newgenres' and equals[i] == '=':
		newgenres = int(parameter[i])
	elif keyword[i] == 'number' and equals[i] == '=':
		number = int(parameter[i])
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
if 'genre' not in locals():
	print('\ngenre not found in input file; genre = any by default.')
	genre = 'any'
if 'allnew' not in locals():
	print('\nallnew not found in input file; allnew = 0 by default.')
	allnew = 0
if 'newgenres' not in locals():
	print('\nnewgenres not found in input file; newgenres = 0 by default.')
	newgenres = 0
if 'number' not in locals():
	print('\nnumber not found in input file; number = 1 by default.')
	number = 1

# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')

# If allnew = 0, check for previous film collection output:
collectionflag = 0
if allnew == 0:
	collectionpath = Path('Data/Collection.csv')
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
	# Write out the data:
	with open('Data/Collection.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films)):
			csvwriter.writerow([films[i],years[i]])

# Status update:
print('\nNumber of films in collection: '+str(len(films)))
print('\nGetting genres for all collection films.')

# If newgenres = 0, check for previous film genre output:
if newgenres == 0:
	genrepath = Path('Data/Genres.csv')
	if genrepath.exists():
		# If there is previous output, read it in:
		films2 = []
		years2 = []
		genres2 = []
		with open('Data/Genres.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films2 = films2+[row[0]]
				years2 = years2+[row[1]]
				genres2 = genres2+[row[2]]
# Go through all collection films, and either
# grab info from internet, or use previous info if available:
films3 = []
years3 = []
genres3 = []
for i in range(len(films)):
	# Check if previous info available:
	genreflag = 0
	if newgenres == 0:
		if films[i] in films2:
			genreflag = 1
			films3 = films3+[films[i]]
			years3 = years3+[years[i]]
			genres3 = genres3+[genres2[films2.index(films[i])]]
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
		films3 = films3+[films[i]]
		years3 = years3+[years[i]]
		genres3 = genres3+[genrestring]
# Make sure the lengths match:
if len(films3) != len(genres3):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of genres')
# Write out the data:
if newgenres == 1:
	with open('Data/Genres.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films3)):
			csvwriter.writerow([films3[i],years3[i],genres3[i]])

# Status update:
print('\nGetting all of Alex\'s film ratings.')

# If allnew = 0, check for previous film ratings output:
ratingsflag = 0
if allnew == 0:
	ratingspath = Path('Data/Ratings.csv')
	if ratingspath.exists():
		# If there is previous output, read it in:
		ratingsflag = 1
		films4 = []
		ratings4 = []
		with open('Data/Ratings.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films4 = films4+[row[0]]
				ratings4 = ratings4+[row[1]]
	# Make ratings values integers:
	ratings4 = [int(item) for item in ratings4]
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
	films4 = []
	ratings4 = []
	# Start on page 1, get the films:
	films4 = films4+getstrings('all','data-film-slug="/film/','/"',source)
	# Do the same for ratings:
	ratings4 = ratings4+getstrings('all','rating rated-','">',source)
	# Now loop through the rest of the pages:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films:
		films4 = films4+getstrings('all','data-film-slug="/film/','/"',source)
		# Get ratings:
		ratings4 = ratings4+getstrings('all','rating rated-','">',source)
	# Make ratings values integers:
	ratings4 = [int(item) for item in ratings4]
	# Make sure the lengths match:
	if len(films4) != len(ratings4):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of ratings')
	# Write out the data:
	with open('Data/Ratings.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films4)):
			csvwriter.writerow([films4[i],ratings4[i]])

# Status update:
print('\nNumber of total ratings: '+str(len(films4)))
print('\nMatching film collection with ratings.')

# Match ratings if they exist, otherwise make them -1.0:
ratingscount = 0
newfilms = []
newyears = []
newgenres = []
newratings = []
for i in range(len(films3)):
	flag = 0
	j = 0
	while flag == 0 and j < len(films4):
		if films3[i] == films4[j]:
			flag = 1
			newfilms = newfilms+[films3[i]]
			newyears = newyears+[years3[i]]
			newgenres = newgenres+[genres3[i]]
			newratings = newratings+[ratings4[j]/2.0]
			del films4[j]
			del ratings4[j]
			ratingscount = ratingscount+1
		j = j+1
	if flag == 0:
		newfilms = newfilms+[films3[i]]
		newyears = newyears+[years3[i]]
		newgenres = newgenres+[genres3[i]]
		newratings = newratings+[-1.0]

# Status update:
print('\nNumber of collection that has been rated: '+str(ratingscount))
print('\nLimiting years, if requested.')

# Limit years:
ycutfilms = []
ycutyears = []
ycutgenres = []
ycutratings = []
if minyear != 0 or maxyear != 0:
	if maxyear == 0:
		maxyear = 3000
	for i in range(len(newfilms)):
		if newyears[i] >= minyear and newyears[i] <= maxyear:
			ycutfilms = ycutfilms+[newfilms[i]]
			ycutyears = ycutyears+[newyears[i]]
			ycutgenres = ycutgenres+[newgenres[i]]
			ycutratings = ycutratings+[newratings[i]]
else:
	ycutfilms = [item for item in newfilms]
	ycutyears = [item for item in newyears]
	ycutgenres = [item for item in newgenres]
	ycutratings = [item for item in newratings]
if len(ycutfilms) == 0:
	sys.exit('ERROR - in function "MAIN" - No films in the year range given')

# Status update:
print('\nNumber fitting year criterion: '+str(len(ycutfilms)))
print('\nLimiting ratings, if requested.')

# Limit ratings:
rcutfilms = []
rcutyears = []
rcutgenres = []
rcutratings = []
if minrating != 0 or maxrating != 0:
	if maxrating == 0:
		maxrating = 5
	for i in range(len(ycutfilms)):
		if ycutratings[i] >= minrating and ycutratings[i] <= maxrating:
			rcutfilms = rcutfilms+[ycutfilms[i]]
			rcutyears = rcutyears+[ycutyears[i]]
			rcutgenres = rcutgenres+[ycutgenres[i]]
			rcutratings = rcutratings+[ycutratings[i]]
	if len(rcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the rating range given')
# Otherwise, just keep all of the films:
else:
	rcutfilms = [item for item in ycutfilms]
	rcutyears = [item for item in ycutyears]
	rcutgenres = [item for item in ycutgenres]
	rcutratings = [item for item in ycutratings]

# Status update:
print('\nNumber fitting rating criterion: '+str(len(rcutfilms)))
print('\nLimiting genres, if requested.')

# Limit genres:
gcutfilms = []
gcutyears = []
gcutgenres = []
gcutratings = []
if genre != 'any':
	for i in range(len(rcutfilms)):
		genres = rcutgenres[i].split(' ')
		flag1 = 0
		flag2 = 0
		for j in range(len(genres)):
			if genre == genres[j]:
				gcutfilms = gcutfilms+[rcutfilms[i]]
				gcutyears = gcutyears+[rcutyears[i]]
				gcutgenres = gcutgenres+[rcutgenres[i]]
				gcutratings = gcutratings+[rcutratings[i]]
			elif genre == 'romcom':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'comedy':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[rcutfilms[i]]
					gcutyears = gcutyears+[rcutyears[i]]
					gcutgenres = gcutgenres+[rcutgenres[i]]
					gcutratings = gcutratings+[rcutratings[i]]
			elif genre == 'romdram':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'drama':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[rcutfilms[i]]
					gcutyears = gcutyears+[rcutyears[i]]
					gcutgenres = gcutgenres+[rcutgenres[i]]
					gcutratings = gcutratings+[rcutratings[i]]
			elif genre == 'actadv':
				if genres[j] == 'action':
					flag1 = 1
				elif genres[j] == 'adventure':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[rcutfilms[i]]
					gcutyears = gcutyears+[rcutyears[i]]
					gcutgenres = gcutgenres+[rcutgenres[i]]
					gcutratings = gcutratings+[rcutratings[i]]
# Otherwise, just keep all of the films:
else:
	gcutfilms = [item for item in rcutfilms]
	gcutyears = [item for item in rcutyears]
	gcutgenres = [item for item in rcutgenres]
	gcutratings = [item for item in rcutratings]

# Denote the final result arrays:
finalfilms = [item for item in gcutfilms]
finalyears = [item for item in gcutyears]
finalgenres = [item for item in gcutgenres]
finalratings = [item for item in gcutratings]

# Status update:
print('\nNumber fitting genre criterion: '+str(len(gcutfilms)))
print('\nRequested films obtained. Choosing one randomly.')

# Grab a random "number" of films:
random.seed()
if len(finalfilms) < number:
	number = len(finalfilms)
choice = []
year = []
genre = []
rating = []
for i in range(number):
	choice = choice+[random.choice(finalfilms)]
	# Get the year and rating:
	year = year+[finalyears[finalfilms.index(choice[i])]]
	genre = genre+[finalgenres[finalfilms.index(choice[i])]]
	rating = rating+[finalratings[finalfilms.index(choice[i])]]

# Print out the result:
print('\n********************')
for i in range(len(choice)):
	if rating[i] == -1.0:
		print('{} -- {:d} -- no rating -- {}'.format(choice[i],year[i],genre[i]))
	else:
		print('{} -- {:d} -- {:.1f}/5 -- {}'.format(choice[i],year[i],rating[i],genre[i]))
print('********************\n')
