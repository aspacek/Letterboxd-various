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

outputfile = open('C_a_c_Output_'+film1+'.txt','w')

# Compare with every film in our collection
# Status update:
print('\nReading in Amanda\'s and Alex\'s film collection.')
outputfile.write('\nReading in Amanda\'s and Alex\'s film collection.')

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
outputfile.write('\nNumber of films in collection: '+str(len(films)))

# Read in actors and films to ignore
ignorefilms = []
ignoreactors = []
with open('C_a_c_films_to_ignore.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\n')
	for row in csv_reader:
		ignorefilms = ignorefilms+[row[0]]
with open('C_a_c_actors_to_ignore.txt') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\n')
	for row in csv_reader:
		ignoreactors = ignoreactors+[row[0]]

print('\nChecking all owned films that share at least one actor with '+film1)
outputfile.write('\n\nChecking all owned films that share at least one actor with '+film1)

allfilms = []
allactors = []
n = 0

for eachfilm in films:
	n = n+1
	print('\n'+str(n)+' / '+str(len(films))+' Checking '+eachfilm)
	outputfile.write('\n\n'+str(n)+' / '+str(len(films))+' Checking '+eachfilm)
	skipflag1 = 0
	for skipfilm in ignorefilms:
		if eachfilm == skipfilm:
			skipflag1 = 1
			print('Skipping '+eachfilm+' due to film Sheet match')
			outputfile.write('\nSkipping '+eachfilm+' due to film Sheet match')
	if film1 != eachfilm and skipflag1 == 0:
		filmcomparison = [film1,eachfilm]
		ratings = [0,0]
		filmcomparison,ratings,actors = getfilminfo(filmcomparison,ratings,['actors'])
		actors1 = []
		actors2 = []
		for i in range(len(filmcomparison)):
			if filmcomparison[i] == film1:
				actors1 = actors1+[actors[i]]
			else:
				actors2 = actors2+[actors[i]]
		matchflag = 0
		for i in range(len(actors2)):
			skipflag2 = 0
			for skipactor in ignoreactors:
				if actors2[i] == skipactor:
					skipflag2 = 1
					print('Skipping '+actors2[i]+' due to actor Sheet match')
					outputfile.write('\nSkipping '+actors2[i]+' due to actor Sheet match')
			if skipflag2 == 0:
				for j in range(len(actors1)):
					if actors2[i] == actors1[j]:
						skipflag3 = 0
						for k in range(len(actors2)):
							for skipactor in ignoreactors:
								if actors2[k] == skipactor:
									for l in range(len(actors1)):
										if l != j and actors2[k] == actors1[l]:
											skipflag3 = 1
											skippedactor = actors2[k]
						if skipflag3 == 0:
							allfilms = allfilms+[eachfilm]
							allactors = allactors+[actors2[i]]
						else:
							print(actors2[i]+' is in '+eachfilm+' but skipping due to '+skippedactor+' being in it')
							outputfile.write('\n'+actors2[i]+' is in '+eachfilm+' but skipping due to '+skippedactor+' being in it')

print('\n**************************************************')
outputfile.write('\n\n**************************************************')

sortedactors,sortedfilms = numsort(allactors,allfilms,1,0)

for i in range(len(sortedactors)):
	print('')
	print(sortedactors[i]+' - '+sortedfilms[i])
	outputfile.write('\n\n'+sortedactors[i]+' - '+sortedfilms[i])
print('')
outputfile.write('\n')

outputfile.close()
