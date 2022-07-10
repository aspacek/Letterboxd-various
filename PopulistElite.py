######################
## PopulistElite.py ##
######################

# sys module - reads in input values
#            - exits program on error
import sys

# requests module - reads in source code from a given url
import requests

# locale module - able to convert number string with commas to an integer
import locale

##
## Written by Alex Spacek
## September 2021
##

############################################################
# FINDSTRINGS
# Function that gives every location of substring in string.
# INPUTS:
#   substring = string (any)
#   string    = string (any)
##################################
def findstrings(substring,string):
	# Initialize flag to see if any substrings are found:
	lastfound = -1
	# While loop until no more substrings are found:
	while True:
		# Find next instance of substring in string, starting right after the location of the previous string:
		lastfound = string.find(substring,lastfound+1)
		# If no more substring are found, end the function:
		if lastfound == -1:  
			break
		# If a new substring is found, record its location:
		yield lastfound

####################################################################################
# GETSTRINGS
# Function that grabs all desired substrings that are surrounded by 2 given strings:
# INPUTS:
#   which      = string ('first', 'last', 'all')
#   prestring  = string (any)
#   poststring = string (any)
#   source     = string (the source from which to grab the desired strings)
# OUTPUTS:
#   strings = string or string array (whatever was wanted)
##################################################
def getstrings(which,prestring,poststring,source):
	# First find the start of the string:
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
		sys.exit('ERROR - in getstrings - Invalid input for "which"')
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

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def SortAndSyncList_Multi(ListToSort, *ListsToSync):
    y = sorted(zip(ListToSort, zip(*ListsToSync)))
    w = [n for n in zip(*y)]
    return list(w[0]), tuple(list(a) for a in zip(*w[1]))

###########################################
# FILMINFO
# Function to grab info about a given film.
# INPUTS:
#   verbose = integer (0 or 1)
#   film    = string (a valid Letterboxd film)
# OUTPUTS:
#   film_name      = string (the name of the film)
#   film_year      = integer (the year of the film)
#   film_directors = string array (list of all directors of the film)
#   film_actors    = string array (list of all actors in the film)
#   film_runtime   = integer (the runtime of the film in minutes)
#   film_avgrating = float (the average Letterboxd rating of the film)
#   film_views     = integer (the number of views the film has on Letterboxd)
###########################
def filminfo(verbose,film):
	# The base url of the film's page:
	url = 'https://letterboxd.com/film/'+film+'/'
	# Grab source code for the film's page:
	r = requests.get(url)
	source = r.text
	# Get the film title:
	film_name = getstrings('last','name: "','",',source)
	# Get the film year:
	film_year = int(getstrings('first','releaseYear: "','",',source))
	# Get the director(s):
	# Check on the number of directors:
	director_check = list(findstrings('<h3><span>Director</span></h3>',source))
	# If there are multiple directors or no directors:
	if director_check == []:
		nodirector_check = list(findstrings('<h3><span>Directors</span></h3>',source))
		if nodirector_check == []:
			film_directors = ['none']
		else:
			subtext = getstrings('first','<h3><span>Directors</span></h3>','</div>',source)
			film_directors = getstrings('all','class="text-slug">','</a>',subtext)
	# If there is one director:
	else:
		subtext = getstrings('first','<h3><span>Director</span></h3>','</div>',source)
		film_directors = getstrings('all','class="text-slug">','</a>',subtext)
	# Get the actors:
	# Check on the number of actors:
	actor_check = list(findstrings('class="text-slug tooltip">',source))
	# If there are multiple actors:
	if len(actor_check) > 1:
		film_actors = getstrings('all','class="text-slug tooltip">','</a>',source)
	# If there is one actor:
	elif len(actor_check) == 1:
		film_actors = [getstrings('first','class="text-slug tooltip">','</a>',source)]
	# If there are no actors:
	else:
		film_actors = ['none']
	# Get the runtime, if there is one:
#	print(film)
	runtime_check = getstrings('first','<p class="text-link text-footer">\n\t\t\t\t','More details at',source)
	if runtime_check == '\n\t\t\t\t\n\t\t\t\t\t':
		film_runtime = -1
	else:
		string = getstrings('first','<p class="text-link text-footer">\n\t\t\t\t','&nbsp;min',source)
		if is_integer(string):
			film_runtime = int(getstrings('first','<p class="text-link text-footer">\n\t\t\t\t','&nbsp;min',source))
		else:
			newstring = ''
			for bit in string:
				if is_integer(bit):
					newstring = newstring+bit
			film_runtime = int(newstring)
	# Get the average rating, if there is one:
	avgrating_check = list(findstrings('name="twitter:data2" content="',source))
	if avgrating_check == []:
		film_avgrating = -1.0
	else:
		film_avgrating = float(getstrings('first','name="twitter:data2" content="',' out of 5"',source))
	# Get the watch count:
	url = 'https://letterboxd.com/film/'+film+'/members/'
	r = requests.get(url)
	source2 = r.text
	views_check = list(findstrings('class="tooltip" title="1&nbsp;person"> Watched',source2))
	if views_check == []:
		views = getstrings('first','class="tooltip" title="','&nbsp;people',source2)
	else:
		views = getstrings('first','class="tooltip" title="','&nbsp;person',source2)
	locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
	film_views = locale.atoi(views)
	# Get the genres:
	extra_genres = []
	film_genres = []
	# Check on the number of genres:
	genre_check = list(findstrings('/films/genre/',source))
	# Check on the number of "genre" labels to ignore:
	genre_ignore_check = list(findstrings('/films/genre/horror/by/rating/size/small',source))
	# Number of valid genres:
	genre_length = len(genre_check)-len(genre_ignore_check)
	# If there are multiple genres:
	if genre_length > 1:
		genres_temp = getstrings('all','/films/genre/','/"',source)
		for j in range(len(genres_temp)):
			if genres_temp[j] != 'horror/by/rating/size/small':
				if j == 0:
					film_genres = film_genres+[genres_temp[j]]
				else:
					extra_genres = extra_genres+[genres_temp[j]]
	# If there is one genre:
	elif genre_length == 1:
		flag = 0
		if len(genre_ignore_check) == 0:
			flag = 1
			film_genres = film_genres+[getstrings('first','/films/genre/','/"',source)]
		else:
			genres_temp = getstrings('all','/films/genre/','/"',source)
			for j in range(len(genres_temp)):
				if genres_temp[j] != 'horror/by/rating/size/small':
					flag = flag+1
					film_genres = film_genres+[genres_temp[j]]
		if flag != 1:
			sys.exit('ERROR - in filminfo - genre extraction (of one genre) encountered an error.')
	# If there are no genres:
	else:
		film_genres = film_genres+['none']
	film_genres = film_genres+extra_genres
	# Return the results:
	return film_name,film_year,film_directors,film_actors,film_runtime,film_avgrating,film_views,film_genres

##################
## MAIN PROGRAM ##
##################

# Min/max views
view_min = 200000
view_max = 1000000000
view_min2 = 1
view_max2 = 500

# Min/max runtimes
runtime_min = 60
runtime_max = 480
runtime_min2 = 60
runtime_max2 = 240

# Verbose?
verbose = 0

# Top 1000 films list
url = 'https://letterboxd.com/arhodes/list/top-1000-highest-rated-on-letterboxd/'

# Read in all films:
films = []
ratings = []
runtimes = []
views = []
films2 = []
ratings2 = []
runtimes2 = []
views2 = []
# Grab source code for the first page:
r = requests.get(url)
source = r.text
# Find the number of pages
pagecheck = list(findstrings('/page/',source))
if pagecheck == []:
	pages = 1
else:
	pages = int(getstrings('last','/page/','/">',source))
print('')
print('# Pages = '+str(pages))
# Loop through all pages and grab all the film titles:
films_temp = []
# Start on page 1, get the films:
text_blocks = getstrings('all','data-film-slug="/film','data-menu',source)
for i in range(len(text_blocks)):
	correct_film_check = list(findstrings('data-linked="linked"',text_blocks[i]))
	if correct_film_check != []:
		films_temp = films_temp+[getstrings('first','/','/"',text_blocks[i])]
# Now loop through the rest of the pages:
if pages > 1:
	for page in range(pages-1):
		# Start on page 2:
		page = str(page + 2)
		print('')
		print('Starting page '+page)
		# Grab source code of the page:
		r = requests.get(url+'page/'+page+'/')
		source = r.text
		# Get films:
		text_blocks = getstrings('all','data-film-slug="/film','data-menu',source)
		for i in range(len(text_blocks)):
			correct_film_check = list(findstrings('data-linked="linked"',text_blocks[i]))
			if correct_film_check != []:
				films_temp = films_temp+[getstrings('first','/','/"',text_blocks[i])]
# Grab film info:
print('')
for i in range(len(films_temp)):
	if i % 50 == 0:
		print('Film # '+str(i+1)+' / '+str(len(films_temp)))
	fname,fyear,fdirectors,factors,fruntime,favgrating,fviews,fgenres = filminfo(verbose,films_temp[i])
	viewflag = 0
	if fviews >= view_min and fviews <= view_max:
		viewflag = 1
	runtimeflag = 0
	if fruntime >= runtime_min and fruntime <= runtime_max:
		runtimeflag = 1
	if viewflag == 1 and runtimeflag == 1:
		films = films+[films_temp[i]]
		ratings = ratings+[favgrating]
		runtimes = runtimes+[fruntime]
		views = views+[fviews]
	viewflag2 = 0
	if fviews >= view_min2 and fviews <= view_max2:
		viewflag2 = 1
	runtimeflag2 = 0
	if fruntime >= runtime_min2 and fruntime <= runtime_max2:
		runtimeflag2 = 1
	if viewflag2 == 1 and runtimeflag2 == 1:
		films2 = films2+[films_temp[i]]
		ratings2 = ratings2+[favgrating]
		runtimes2 = runtimes2+[fruntime]
		views2 = views2+[fviews]

# Sort results by rating:
xfilms = [val for val in films]
xruntimes = [val for val in runtimes]
xratings = [val for val in ratings]
xviews = [val for val in views]
ratings_sorted,combined_sorted = SortAndSyncList_Multi(xratings,xfilms,xruntimes,xviews)
films_sorted = combined_sorted[0]
runtimes_sorted = combined_sorted[1]
views_sorted = combined_sorted[2]
ratings_sorted.reverse()
films_sorted.reverse()
runtimes_sorted.reverse()
views_sorted.reverse()
xfilms2 = [val for val in films2]
xruntimes2 = [val for val in runtimes2]
xratings2 = [val for val in ratings2]
xviews2 = [val for val in views2]
ratings_sorted2,combined_sorted2 = SortAndSyncList_Multi(xratings2,xfilms2,xruntimes2,xviews2)
films_sorted2 = combined_sorted2[0]
runtimes_sorted2 = combined_sorted2[1]
views_sorted2 = combined_sorted2[2]
ratings_sorted2.reverse()
films_sorted2.reverse()
runtimes_sorted2.reverse()
views_sorted2.reverse()

# Print results:
print('')
for i in range(len(films_sorted)):
	print('{:3d} - {:80s} - {:4.2f} - {:6d} - {:7d}'.format(i+1,films_sorted[i],ratings_sorted[i],runtimes_sorted[i],views_sorted[i]))
print('')
for i in range(len(films_sorted2)):
	print('{:3d} - {:80s} - {:4.2f} - {:6d} - {:7d}'.format(i+1,films_sorted2[i],ratings_sorted2[i],runtimes_sorted2[i],views_sorted2[i]))
print('')
