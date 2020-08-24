##############################
## LetterboxdCompareList.py ##
##############################

##########
## IMPORTS
##########

# requests module - reads in source code from a given url
import requests

# random module - for getting random numbers
import random

##############
## SUBROUTINES
##############

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

###############
## MAIN PROGRAM
###############

# Get list:
listurl = input('\nEnter Letterboxd list url: ')
print('')

# Read in all films:
# (1) Grab source code for the list page:
r = requests.get(listurl)
source = r.text
# (2) Initialize results:
films = []
# (3) Get the films:
# (3a) Details: get all strings from the source code between the strings
#      'data-film-slug="/film/' and '/"', which are the film names
films = films+getstrings('all','data-film-slug="/film/','/"',source)
# (4) Get number of films:
num = len(films)

# Ranking:
# (1) PRELIMINARY STEPS
# Ranking array:
ranks = [0 for i in range(num)]
# How many films to skip in the ranking process:
jumpnum = 5
# Start with a random film ranked #1:
choice = random.randrange(0,num)
ranks[choice] = 1
# Loop until everything is ranked:
alldone = 0
# (2) RANKING LOOP
while alldone == 0:
#	# TEMPORARY
	# Print out each iteration of the ranking:
	print('')
	for i in range(num):
		print(str(ranks[i])+' '+films[i])
	print('')
#	# TEMPORARY
	# Reset checking array each loop:
	checked = [0 for i in range(num)]
	# Pick a random unranked film:
	flag = 0
	while flag == 0:
		choice = random.randrange(0,num)
		if ranks[choice] == 0:
			flag = 1
	# Highest will always start at 1
	highest = 1
	# Find lowest:
	lowest = 1
	for i in range(num):
		if ranks[i] > lowest:
			lowest = ranks[i]
	# Check how many jumps of jumpnum there are:
	count = 0
	for i in range(num):
		if ranks[i] != 0:
			count = count+1
	# 'count-1' to account for first ranked, and int will always round down.
	jumps = int((count-1)/jumpnum)
	# Keep track of when jumping should be stopped:
	stopjumps = 0
	# No jumps if not enough films are ranked yet:
	if jumps == 0:
		stopjumps = 1
	# Keep checking until film is ranked:
	currentdone = 0
	# (3) CHECKING LOOP
	while currentdone == 0:
		# Find 'highest' film: 
		for i in range(num):
			if ranks[i] == highest:
				choice2 = i
		checked[choice2] = 1
		# Compare:
		higher = input('(1) '+films[choice]+'\n(2) '+films[choice2]+'\nWhich one do you rank higher? ')
		print('')
		# Two cases:
		#   A - New, unranked film is higher
		#   B - Already ranked film is higher
		# (A) NEW FILM IS HIGHER
		if higher == '1':
			# Two cases:
			#   i   - New film is done being ranked:
			#         - It was ranked higher than highest film
			#         - It was already compared with the next highest
			#   ii  - Jumping phase is ended, still more films to compare:
			#         - Go to highest ranked film not yet compared
			#         - Proceed stepwise down from now on
			# (i) FILM IS DONE BEING RANKED
			# If film is highest rated:
			if highest == 1:
				currentdone = 1
				finalplace = highest
			# If film directly above in rank was already compared:
			else:
				for i in range(num):
					if ranks[i] == highest-1 and checked[i] == 1:
						currentdone = 1
						finalplace = highest
			# (ii) JUMPING PHASE OVER
			if currentdone == 0:
				stopjumps = 1
				# Next film to check is just below the highest already checked:
				newhighest = highest
				foundnext = 0
				while foundnext == 0:
					for i in range(num):
						if ranks[i] == newhighest-1:
							if checked[i] == 1:
								foundnext = 1
							else:
								newhighest = newhighest-1
				highest = newhighest
		# (B) ALREADY RANKED FILM IS HIGHER
		else:
			# Two cases:
			#   i  - Still jumping, make next jump
			#   ii - Not jumping, go to next lowest
			#        - If none lower, stop ranking
			#        - If next lowest already checked, stop ranking
			#        - Otherwise, check with next lowest
			# (i) STILL JUMPING
			if stopjumps == 0:
				# Perform jump:
				highest = highest+jumpnum
				# Decrease jumps:
				jumps = jumps-1
				# If no more jumps left, stop jumping:
				if jumps == 0:
					stopjumps = 1
			# (ii) JUMPING HAS STOPPED
			else:
				# If already at lowest, insert new film just below:
				if highest == lowest:
					currentdone = 1
					finalplace = highest+1
				# If next lowest already checked, ranking done:
				else:
					for i in range(num):
						if ranks[i] == highest+1 and checked[i] == 1:
							currentdone = 1
							finalplace = highest+1
					# Otherwise, check next lowest next:
					if currentdone == 0:
						highest = highest+1
		# If done, put film in its place and shift all others down as necessary:
		if currentdone == 1:
			for i in range(num):
				if ranks[i] >= finalplace:
					ranks[i] = ranks[i]+1
			ranks[choice] = finalplace
	# Check if ranking is done:
	alldone = 1
	for i in range(num):
		if ranks[i] == 0:
			alldone = 0

# Sort by ranking:
sfilms = [fnam for fnum, fnam in sorted(zip(ranks,films))]
ranks.sort()

# Print results:
print('')
for i in range(len(sfilms)):
	print(str(ranks[i])+' '+sfilms[i])
print('')
