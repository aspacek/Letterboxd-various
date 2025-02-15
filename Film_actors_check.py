##########################
## Film_actors_check.py ##
##########################

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
## Copied from Actors_league.py
## September 2024
##

############################################################################
############################################################################

film1 = 'atonement'
film2 = 'pride-prejudice'

film1 = input('\nEnter Letterboxd film 1: ')
film2 = input('\nEnter Letterboxd film 2: ')
print('')

films = [film1,film2]
ratings = [0,0]

films,ratings,actors = getfilminfo(films,ratings,['actors'])

alreadydone = []
for i in range(len(actors)):
	for j in range(len(actors)):
		if i != j:
			if actors[i] == actors[j]:
				flag = 0
				for k in range(len(alreadydone)):
					if i == alreadydone[k]:
						flag = 1
				if flag == 0:
					print(actors[i])
					alreadydone = alreadydone+[j]
print('')
