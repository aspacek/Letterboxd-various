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
	# getratings
	if keyword[i] == 'getratings' and equals[i] == '=':
		getratings = int(parameter[i])
	# dotopyears
	if keyword[i] == 'dotopyears' and equals[i] == '=':
		dotopyears = int(parameter[i])
# Defaults, if parameters not found:
if 'getratings' not in locals():
	print('\ngetratings not found in input file; getratings = 1 by default.')
	getratings = 1
if 'dotopyears' not in locals():
	print('\ndotopyears not found in input file; dotopyears = 0 by default.')
	dotopyears = 0

# Grab all ratings, if needed:
if dotopyears == 1:
	# Read in previous ratings if wanted:
	if getratings == 0:
		films = []
		ratings = []
		with open('Data/moogic_ratings.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				films = films+[row[0]]
				ratings = ratings+[row[1]]
	# Otherwise, grab info from internet:
	else:
		# The base url of the user's film ratings:
		url = 'https://letterboxd.com/moogic/films/ratings/'
		# Grab source code for first ratings page:
		r = requests.get(url)
		source = r.text
		# Find the number of ratings pages:
		pages = int(getstrings('last','/moogic/films/ratings/page/','/"',source))
		# Loop through all pages and grab all the film titles:
		# Initialize results:
		films = []
		ratings = []
		# Start on page 1, get the films:
		films = films+getstrings('all','data-film-slug="/film/','/"',source)
		# Do the same for ratings:
		ratings = ratings+getstrings('all','rating rated-','">',source)
		# Now loop through the rest of the pages:
		for page in range(pages-1):
			# Start on page 2:
			page = str(page + 2)
			# Grab source code of the page:
			r = requests.get(url+'page/'+page+'/')
			source = r.text
			# Get films:
			films = films+getstrings('all','data-film-slug="/film/','/"',source)
			# Get ratings:
			ratings = ratings+getstrings('all','rating rated-','">',source)
	# Make sure the lengths match:
	if len(films) != len(ratings):
		sys.exit('ERROR - Number of films does not match number of ratings')
	# Write out ratings to file, if they're new:
	if getratings == 1:
		with open('Data/moogic_ratings.csv', mode='w') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in range(len(films)):
				csvwriter.writerow([films[i],ratings[i]])
	# Ratings should be integer type:
	ratings = [int(item) for item in ratings]

# Grab all years, if needed:
if dotopyears == 1:
	# Read in previous years if wanted:
	if getratings == 0:
		filmsX = []
		years = []
		with open('Data/moogic_years.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				filmsX = filmsX+[row[0]]
				years = years+[row[1]]
	# Otherwise, grab info from internet:
	else:
		# Initialize results:
		years = []
		# Loop through films:
		for i in range(len(films)):
			# The base url of our film collection:
			url = 'https://letterboxd.com/film/'+films[i]+'/'
			# Grab source code for the film page:
			r = requests.get(url)
			source = r.text
			# Get the years:
			years = years+[getstrings('first','releaseYear: "','",',source)]
	# Make sure the lengths match:
	if len(films) != len(years):
		sys.exit('ERROR - Number of films does not match number of years')
	# Write out years to file, if they're new:
	if getratings == 1:
		with open('Data/moogic_years.csv', mode='w') as outfile:
			csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in range(len(years)):
				csvwriter.writerow([films[i],years[i]])
	# Years should be integer type:
	years = [int(item) for item in years]

# Grab favorite films list, if necessary:
if dotopyears == 1:
	# The base url of our film collection:
	url = 'https://letterboxd.com/moogic/list/moogics-favorite-films-of-all-time-rated/'
	# Grab source code for the film page:
	r = requests.get(url)
	source = r.text
	# Get the films:
	topfilms = getstrings('all','data-film-slug="/film/','/"',source)

# Check top years, if wanted:
if dotopyears == 1:
	# Do decades first:
	decades = ['1990s','2000s','2010s','2020s']
	minyears = [1990,2000,2010,2020]
	maxyears = [1999,2009,2019,2020]
	# For each one, grab films and print out all remaining films with 5 stars:
	for i in range(len(decades)):
		# Grab list films:
		decade = decades[i]
		url = 'https://letterboxd.com/moogic/list/moogics-top-10-films-of-the-'+decade+'/'
		r = requests.get(url)
		source = r.text
		filmsX = getstrings('all','data-film-slug="/film/','/"',source)
		# Loop through all films:
		potentialfilms = []
		potentialyears = []
		potentialratings = []
		potentialinlist = []
		potentialrankings = []
		questionablefilms = []
		questionableyears = []
		questionableratings = []
		for j in range(len(films)):
			flag = 0
			# Check if a list film matches:
			for k in range(len(filmsX)):
				if films[j] == filmsX[k]:
					flag = 1
					# If it does match, check year and rating:
					if years[j] < minyears[i] or years[j] > maxyears[i] or ratings[j] != 10:
						questionablefilms = questionablefilms+[films[j]]
						questionableyears = questionableyears+[years[j]]
						questionableratings = questionableratings+[ratings[j]]
					# If all is good, note placement in top films list:
					else:
						potentialfilms = potentialfilms+[films[j]]
						potentialyears = potentialyears+[years[j]]
						potentialratings = potentialratings+[ratings[j]]
						potentialinlist = potentialinlist+['YES']
						listflag = 0
						for l in range(len(topfilms)):
							if films[j] == topfilms[l]:
								listflag = 1
								potentialrankings = potentialrankings+[l+1]
						if listflag == 0:
							sys.exit('ERROR - 5 star film not in top films list')
			if flag == 0:
				# If film isn't in list, note it if it's the right year and it's rated 5 stars:
				if years[j] >= minyears[i] and years[j] <= maxyears[i]:
					if ratings[j] == 10:
						potentialfilms = potentialfilms+[films[j]]
						potentialyears = potentialyears+[years[j]]
						potentialratings = potentialratings+[ratings[j]]
						potentialinlist = potentialinlist+['NO ']
						listflag = 0
						for l in range(len(topfilms)):
							if films[j] == topfilms[l]:
								listflag = 1
								potentialrankings = potentialrankings+[l+1]
						if listflag == 0:
							sys.exit('ERROR - 5 star film not in top films list')
		# Print out:
		print('\nDecade = '+decade)
		print('  Questionable films:')
		if len(questionablefilms) == 0:
			print('    None')
		else:
			for j in range(len(questionablefilms)):
				print('    '+questionablefilms[j]+' '+str(questionableyears[j])+' '+str(questionableratings[j]))
		print('  Potential films:')
		if len(potentialfilms) == 0:
			print('    None')
		else:
			# Sort films by top list ranking:
			# Sort all the users and interpretations by the scores:
			sortA = [name for number,name in sorted(zip(potentialrankings,potentialinlist))]
			sortB = [name for number,name in sorted(zip(potentialrankings,potentialfilms))]
			sortC = [name for number,name in sorted(zip(potentialrankings,potentialyears))]
			sortD = [name for number,name in sorted(zip(potentialrankings,potentialratings))]
			potentialrankings.sort()
			for j in range(len(potentialrankings)):
				print('    '+sortA[j]+' '+str(potentialrankings[j])+' '+sortB[j]+' '+str(sortC[j])+' '+str(sortD[j]))
	# Next do all years:
	topyears = [1990,1991,1992,1993,1994,1995,1996,1997,1998,1999]
	topyears = topyears+[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009]
	topyears = topyears+[2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
	topyears = topyears+[2020]
	# For each one, grab films and print out all remaining films with 5 stars:
	for i in range(len(topyears)):
		# Grab list films:
		topyear = topyears[i]
		url = 'https://letterboxd.com/moogic/list/moogics-top-10-films-of-'+str(topyear)+'/'
		r = requests.get(url)
		source = r.text
		filmsX = getstrings('all','data-film-slug="/film/','/"',source)
		# Loop through all films:
		potentialfilms = []
		potentialyears = []
		potentialratings = []
		potentialinlist = []
		potentialrankings = []
		questionablefilms = []
		questionableyears = []
		questionableratings = []
		for j in range(len(films)):
			flag = 0
			# Check if a list film matches:
			for k in range(len(filmsX)):
				if films[j] == filmsX[k]:
					flag = 1
					# If it does match, check year and rating:
					if years[j] != topyear or ratings[j] != 10:
						questionablefilms = questionablefilms+[films[j]]
						questionableyears = questionableyears+[years[j]]
						questionableratings = questionableratings+[ratings[j]]
					# If all is good, note placement in top films list:
					else:
						potentialfilms = potentialfilms+[films[j]]
						potentialyears = potentialyears+[years[j]]
						potentialratings = potentialratings+[ratings[j]]
						potentialinlist = potentialinlist+['YES']
						listflag = 0
						for l in range(len(topfilms)):
							if films[j] == topfilms[l]:
								listflag = 1
								potentialrankings = potentialrankings+[l+1]
						if listflag == 0:
							sys.exit('ERROR - 5 star film not in top films list')
			if flag == 0:
				# If film isn't in list, note it if it's the right year and it's rated 5 stars:
				if years[j] == topyear:
					if ratings[j] == 10:
						potentialfilms = potentialfilms+[films[j]]
						potentialyears = potentialyears+[years[j]]
						potentialratings = potentialratings+[ratings[j]]
						potentialinlist = potentialinlist+['NO ']
						listflag = 0
						for l in range(len(topfilms)):
							if films[j] == topfilms[l]:
								listflag = 1
								potentialrankings = potentialrankings+[l+1]
						if listflag == 0:
							sys.exit('ERROR - 5 star film not in top films list')
		# Print out:
		print('\nYear = '+str(topyear))
		print('  Questionable films:')
		if len(questionablefilms) == 0:
			print('    None')
		else:
			for j in range(len(questionablefilms)):
				print('    '+questionablefilms[j]+' '+str(questionableyears[j])+' '+str(questionableratings[j]))
		print('  Potential films:')
		if len(potentialfilms) == 0:
			print('    None')
		else:
			# Sort films by top list ranking:
			# Sort all the users and interpretations by the scores:
			sortA = [name for number,name in sorted(zip(potentialrankings,potentialinlist))]
			sortB = [name for number,name in sorted(zip(potentialrankings,potentialfilms))]
			sortC = [name for number,name in sorted(zip(potentialrankings,potentialyears))]
			sortD = [name for number,name in sorted(zip(potentialrankings,potentialratings))]
			potentialrankings.sort()
			for j in range(len(potentialrankings)):
				print('    '+sortA[j]+' '+str(potentialrankings[j])+' '+sortB[j]+' '+str(sortC[j])+' '+str(sortD[j]))
