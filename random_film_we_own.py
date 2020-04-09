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
newgenreflag = 0
if newgenres == 0:
	genrepath = Path('Data/Genres.csv')
	if genrepath.exists():
		newgenreflag = 1
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
	if newgenres == 0 and newgenreflag == 1:
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
if len(films) != len(films3):
	sys.exit('ERROR - in function "MAIN" - Number of films with genres does not match number of films')
# Write out the data:
if newgenreflag == 0:
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
print('\nGetting average Letterboxd ratings for all collection films.')

# If newratingsLetterboxd = 0, check for previous Letterboxd rating output:
newLratingflag = 0
if newratingsLetterboxd == 0:
	Lratingpath = Path('Data/RatingsLetterboxd.csv')
	if Lratingpath.exists():
		newLratingflag = 1
		# If there is previous output, read it in:
		films5 = []
		Lratings5 = []
		with open('Data/RatingsLetterboxd.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films5 = films5+[row[0]]
				Lratings5 = Lratings5+[row[1]]
# Go through all collection films, and either
# grab info from internet, or use previous info if available:
films6 = []
Lratings6 = []
for i in range(len(films3)):
	# Check if previous info available:
	Lratingflag = 0
	if newratingsLetterboxd == 0 and newLratingflag == 1:
		if films3[i] in films5:
			Lratingflag = 1
			films6 = films6+[films[i]]
			Lratings6 = Lratings6+[Lratings5[films5.index(films3[i])]]
	# If previous info not available, get it from the internet:
	if Lratingflag == 0:
		url = 'https://letterboxd.com/film/'+films3[i]+'/'
		# Grab source code for genre page:
		r = requests.get(url)
		source = r.text
		# Find the genres:
		print(films3[i])
		Lrating = getstrings('first','"ratingValue":',',"',source)
		if Lrating == '':
			Lrating = -1.0
		else:
			Lrating = float(Lrating)
		films6 = films6+[films3[i]]
		Lratings6 = Lratings6+[Lrating]
# Make Letterboxd ratings values floats:
Lratings6 = [float(item) for item in Lratings6]
# Make sure the lengths match:
if len(films6) != len(Lratings6):
	sys.exit('ERROR - in function "MAIN" - Number of films does not match number of Letterboxd ratings')
if len(films3) != len(films6):
	sys.exit('ERROR - in function "MAIN" - Number of films with Letterboxd ratings does not match number of films')
# Write out the data:
if newLratingflag == 0:
	with open('Data/RatingsLetterboxd.csv', mode='w') as outfile:
		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in range(len(films6)):
			csvwriter.writerow([films6[i],Lratings6[i]])

# Status update:
print('\nMatching film collection with ratings.')

# Match ratings if they exist, otherwise make them -1.0:
ratingscount = 0
newfilms = []
newyears = []
newgenres = []
newratings = []
newLratings = []
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
			newLratings = newLratings+[Lratings6[i]]
			del films4[j]
			del ratings4[j]
			ratingscount = ratingscount+1
		j = j+1
	if flag == 0:
		newfilms = newfilms+[films3[i]]
		newyears = newyears+[years3[i]]
		newgenres = newgenres+[genres3[i]]
		newratings = newratings+[-1.0]
		newLratings = newLratings+[Lratings6[i]]

# Status update:
print('\nNumber of collection that has been rated: '+str(ratingscount))
print('\nLimiting years, if requested.')

# Limit years:
ycutfilms = []
ycutyears = []
ycutgenres = []
ycutratings = []
ycutLratings = []
if minyear != 0 or maxyear != 0:
	if maxyear == 0:
		maxyear = 3000
	for i in range(len(newfilms)):
		if newyears[i] >= minyear and newyears[i] <= maxyear:
			ycutfilms = ycutfilms+[newfilms[i]]
			ycutyears = ycutyears+[newyears[i]]
			ycutgenres = ycutgenres+[newgenres[i]]
			ycutratings = ycutratings+[newratings[i]]
			ycutLratings = ycutLratings+[newLratings[i]]
else:
	ycutfilms = [item for item in newfilms]
	ycutyears = [item for item in newyears]
	ycutgenres = [item for item in newgenres]
	ycutratings = [item for item in newratings]
	ycutLratings = [item for item in newLratings]
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
rcutLratings = []
if minrating != 0 or maxrating != 0:
	if maxrating == 0:
		maxrating = 5
	for i in range(len(ycutfilms)):
		if ycutratings[i] >= minrating and ycutratings[i] <= maxrating:
			rcutfilms = rcutfilms+[ycutfilms[i]]
			rcutyears = rcutyears+[ycutyears[i]]
			rcutgenres = rcutgenres+[ycutgenres[i]]
			rcutratings = rcutratings+[ycutratings[i]]
			rcutLratings = rcutLratings+[ycutLratings[i]]
	if len(rcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the rating range given')
# Otherwise, just keep all of the films:
else:
	rcutfilms = [item for item in ycutfilms]
	rcutyears = [item for item in ycutyears]
	rcutgenres = [item for item in ycutgenres]
	rcutratings = [item for item in ycutratings]
	rcutLratings = [item for item in ycutLratings]

# Status update:
print('\nNumber fitting rating criterion: '+str(len(rcutfilms)))
print('\nLimiting Letterboxd ratings, if requested.')

# Limit Letterboxd ratings:
Lcutfilms = []
Lcutyears = []
Lcutgenres = []
Lcutratings = []
LcutLratings = []
if minratingLetterboxd != 0 or maxratingLetterboxd != 0:
	if maxratingLetterboxd == 0:
		maxratingLetterboxd = 5
	for i in range(len(rcutfilms)):
		if rcutLratings[i] >= minratingLetterboxd and rcutLratings[i] <= maxratingLetterboxd:
			Lcutfilms = Lcutfilms+[rcutfilms[i]]
			Lcutyears = Lcutyears+[rcutyears[i]]
			Lcutgenres = Lcutgenres+[rcutgenres[i]]
			Lcutratings = Lcutratings+[rcutratings[i]]
			LcutLratings = LcutLratings+[rcutLratings[i]]
	if len(Lcutfilms) == 0:
		sys.exit('ERROR - in function "MAIN" - No films in the Letterboxd rating range given')
# Otherwise, just keep all of the films:
else:
	Lcutfilms = [item for item in rcutfilms]
	Lcutyears = [item for item in rcutyears]
	Lcutgenres = [item for item in rcutgenres]
	Lcutratings = [item for item in rcutratings]
	LcutLratings = [item for item in rcutLratings]

# Status update:
print('\nNumber fitting Letterboxd rating criterion: '+str(len(Lcutfilms)))
print('\nLimiting genres, if requested.')

# Limit genres:
gcutfilms = []
gcutyears = []
gcutgenres = []
gcutratings = []
gcutLratings = []
if genre != 'any':
	for i in range(len(Lcutfilms)):
		genres = Lcutgenres[i].split(' ')
		flag1 = 0
		flag2 = 0
		for j in range(len(genres)):
			if genre == genres[j]:
				gcutfilms = gcutfilms+[Lcutfilms[i]]
				gcutyears = gcutyears+[Lcutyears[i]]
				gcutgenres = gcutgenres+[Lcutgenres[i]]
				gcutratings = gcutratings+[Lcutratings[i]]
				gcutLratings = gcutLratings+[LcutLratings[i]]
			elif genre == 'romcom':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'comedy':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
			elif genre == 'romdram':
				if genres[j] == 'romance':
					flag1 = 1
				elif genres[j] == 'drama':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
			elif genre == 'actadv':
				if genres[j] == 'action':
					flag1 = 1
				elif genres[j] == 'adventure':
					flag2 = 1
				if flag1 == 1 and flag2 == 1:
					gcutfilms = gcutfilms+[Lcutfilms[i]]
					gcutyears = gcutyears+[Lcutyears[i]]
					gcutgenres = gcutgenres+[Lcutgenres[i]]
					gcutratings = gcutratings+[Lcutratings[i]]
					gcutLratings = gcutLratings+[LcutLratings[i]]
# Otherwise, just keep all of the films:
else:
	gcutfilms = [item for item in Lcutfilms]
	gcutyears = [item for item in Lcutyears]
	gcutgenres = [item for item in Lcutgenres]
	gcutratings = [item for item in Lcutratings]
	gcutLratings = [item for item in LcutLratings]

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
			films5 = []
			directors5 = []
			actors5 = []
			with open('Data/Actors.csv') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				for row in csv_reader:
					films5 = films5+[row[0]]
					directors5 = directors5+[row[1]]
					actors5 = actors5+[row[2]]
	# Go through all collection films, and either
	# grab info from internet, or use previous info if available:
	films6 = []
	directors6 = []
	actors6 = []
	for i in range(len(gcutfilms)):
		# Check if previous info available:
		actorflag = 0
		if newactors == 0 and newactorflag == 1:
			if gcutfilms[i] in films5:
				actorflag = 1
				films6 = films6+[gcutfilms[i]]
				directors6 = directors6+[directors5[films5.index(gcutfilms[i])]]
				actors6 = actors6+[actors5[films5.index(gcutfilms[i])]]
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
			films6 = films6+[gcutfilms[i]]
			directors6 = directors6+[directorstring]
			actors6 = actors6+[actorstring]
	# Make sure the lengths match:
	if len(films6) != len(actors6):
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of actors')
	# Make sure films6 is identical to gcutfilms:
	if films6 != gcutfilms:
		sys.exit('ERROR - in function "MAIN" - Director/actor film array not the same as the previous film array')
	# Write out the data:
	if newactors == 1:
		with open('Data/Actors.csv', mode='w') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in range(len(films6)):
				csvwriter.writerow([films6[i],directors6[i],actors6[i]])
# Otherwise just make them empty arrays:
else:
	directors6 = []
	actors6 = []

# Status update:
print('\nLimiting directors, if requested.')

# Limit directors:
dcutfilms = []
dcutyears = []
dcutgenres = []
dcutratings = []
dcutLratings = []
dcutdirectors = []
dcutactors = []
if director != 'none':
	for i in range(len(gcutfilms)):
		directors = directors6[i].split(' ')
		for j in range(len(directors)):
			if director == directors[j]:
				dcutfilms = dcutfilms+[gcutfilms[i]]
				dcutyears = dcutyears+[gcutyears[i]]
				dcutgenres = dcutgenres+[gcutgenres[i]]
				dcutratings = dcutratings+[gcutratings[i]]
				dcutLratings = dcutLratings+[gcutLratings[i]]
				dcutdirectors = dcutdirectors+[directors6[i]]
				dcutactors = dcutactors+[actors6[i]]
# Otherwise, just keep all of the films:
else:
	dcutfilms = [item for item in gcutfilms]
	dcutyears = [item for item in gcutyears]
	dcutgenres = [item for item in gcutgenres]
	dcutratings = [item for item in gcutratings]
	dcutLratings = [item for item in gcutLratings]
	dcutdirectors = [item for item in directors6]
	dcutactors = [item for item in actors6]

# Status update:
print('\nNumber fitting director criterion: '+str(len(dcutfilms)))
print('\nLimiting actors, if requested.')

# Limit actors:
acutfilms = []
acutyears = []
acutgenres = []
acutratings = []
acutLratings = []
acutdirectors = []
acutactors = []
if actor != 'none':
	for i in range(len(dcutfilms)):
		actors = dcutactors[i].split(' ')
		for j in range(len(actors)):
			if actor == actors[j]:
				acutfilms = acutfilms+[dcutfilms[i]]
				acutyears = acutyears+[dcutyears[i]]
				acutgenres = acutgenres+[dcutgenres[i]]
				acutratings = acutratings+[dcutratings[i]]
				acutLratings = acutLratings+[dcutLratings[i]]
				acutdirectors = acutdirectors+[dcutdirectors[i]]
				acutactors = acutactors+[dcutactors[i]]
# Otherwise, just keep all of the films:
else:
	acutfilms = [item for item in dcutfilms]
	acutyears = [item for item in dcutyears]
	acutgenres = [item for item in dcutgenres]
	acutratings = [item for item in dcutratings]
	acutLratings = [item for item in dcutLratings]
	acutdirectors = [item for item in dcutdirectors]
	acutactors = [item for item in dcutactors]

# Denote the final result arrays:
finalfilms = [item for item in acutfilms]
finalyears = [item for item in acutyears]
finalgenres = [item for item in acutgenres]
finalratings = [item for item in acutratings]
finalLratings = [item for item in acutLratings]
finaldirectors = [item for item in acutdirectors]
finalactors = [item for item in acutactors]

# Status update:
print('\nNumber fitting actor criterion: '+str(len(acutfilms)))
print('\nRequested films obtained. Choosing one randomly.')

# Grab a random "number" of films:
random.seed()
if len(finalfilms) < number:
	number = len(finalfilms)
choice = []
year = []
genre = []
rating = []
Lrating = []
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
	genre = genre+[finalgenres[finalfilms.index(thischoice)]]
	rating = rating+[finalratings[finalfilms.index(thischoice)]]
	Lrating = Lrating+[finalLratings[finalfilms.index(thischoice)]]
	if dflag == 1:
		director = director+[finaldirectors[finalfilms.index(thischoice)]]
	if aflag == 1:
		actor = actor+[finalactors[finalfilms.index(thischoice)]]

# Print out the result:
print('\n********************')
if dflag == 0 and aflag == 0:
	for i in range(len(choice)):
		if rating[i] == -1.0:
			print('{} -- {:d} -- no rating -- {:.2f}/5.00 -- {}'.format(choice[i],year[i],Lrating[i],genre[i]))
		else:
			print('{} -- {:d} -- {:.1f}/5.0 -- {:.2f}/5.00 -- {}'.format(choice[i],year[i],rating[i],Lrating[i],genre[i]))
elif dflag == 1 and aflag == 0:
	for i in range(len(choice)):
		if rating[i] == -1.0:
			print('{} -- {:d} -- no rating -- {:.2f}/5.00 -- {} -- {}'.format(choice[i],year[i],Lrating[i],genre[i],director[i]))
		else:
			print('{} -- {:d} -- {:.1f}/5.0 -- {:.2f}/5.00 -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],genre[i],director[i]))
elif dflag == 0 and aflag == 1:
	for i in range(len(choice)):
		actors = actor[i].split(' ')
		if len(actors) < 5:
			n = len(actors)
		else:
			n = 5
		actor5 = ''
		for j in range(n):
			actor5 = actor5+actors[j]+' '
		if rating[i] == -1.0:
			print('{} -- {:d} -- no rating -- {:.2f}/5.00 -- {} -- {}'.format(choice[i],year[i],Lrating[i],genre[i],actor5))
		else:
			print('{} -- {:d} -- {:.1f}/5.0 -- {:.2f}/5.00 -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],genre[i],actor5))
elif dflag == 1 and aflag == 1:
	for i in range(len(choice)):
		actors = actor[i].split(' ')
		if len(actors) < 5:
			n = len(actors)
		else:
			n = 5
		actor5 = ''
		for j in range(n):
			actor5 = actor5+actors[j]+' '
		if rating[i] == -1.0:
			print('{} -- {:d} -- no rating -- {:.2f}/5.00 -- {} -- {} -- {}'.format(choice[i],year[i],Lrating[i],genre[i],director[i],actor5))
		else:
			print('{} -- {:d} -- {:.1f}/5.0 -- {:.2f}/5.00 -- {} -- {} -- {}'.format(choice[i],year[i],rating[i],Lrating[i],genre[i],director[i],actor5))
print('********************\n')
