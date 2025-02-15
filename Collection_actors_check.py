################################
## Collection_actors_check.py ##
################################

# sys module - reads in input values
#            - exits program on error
import sys

# csv module - read and write csv files
import csv

import requests

import time

import locale

from pathlib import Path

from shutil import copyfile

import os

sys.path.insert(0, "../Letterboxd/General-league-routines")
from Findstrings import findstrings
from Getstrings import getstrings
from Numsort import numsort
from Getuserfilms import getuserfilms
from Getfilminfo import getfilminfo

##
## Written by Alex Spacek
## Copied from Film_actors_check.py
## February 2025
##

############################################################################
############################################################################

# Enter a film name as it appears in the Letterboxd URL
# For example, https://letterboxd.com/film/atonement/
#film1 = 'atonement'

film1 = input('\nEnter Letterboxd film 1: ')

# Compare with every film in our collection
# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')

allnew = 1
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
		sys.exit('ERROR - in function "MAIN" - Number of films does not match number of years')
#	# Write out the data:
#	with open('Data/Collection.csv', mode='w') as outfile:
#		csvwriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#		for i in range(len(films)):
#			csvwriter.writerow([films[i],years[i]])

# Status update:
print('\nNumber of films in collection: '+str(len(films)))
print('\nChecking all owned films that share at least one actor with '+film1)

allfilms = []
allactors = []
numactors = []

for eachfilm in films:
	if film1 != eachfilm:
		filmcomparison = [film1,eachfilm]
		ratings = [0,0]
		filmcomparison,ratings,actors = getfilminfo(filmcomparison,ratings,['actors'])
		
		alreadydone = []
		matchflag = 0
		for i in range(len(actors)):
			for j in range(len(actors)):
				if i != j:
					if actors[i] == actors[j]:
						flag = 0
						for k in range(len(alreadydone)):
							if i == alreadydone[k]:
								flag = 1
						if flag == 0:
							allactors = allactors+[actors[i]]
							if matchflag == 0:
								numactors = numactors+[1]
							else:
								numactors[-1] = numactors[-1]+1
							alreadydone = alreadydone+[j]
							matchflag = 1
		if matchflag == 1:
			allfilms = allfilms+[eachfilm]

actorcount = 0
for i in range(len(allfilms)):
	print('')
	print(allfilms[i])
	for j in range(numactors[i]):
		print('\t'+allactors[actorcount])
		actorcount = actorcount+1
print('')
