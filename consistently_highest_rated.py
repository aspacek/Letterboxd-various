###################################
## consistently_highest_rated.py ##
###################################

# csv module - read and write csv files
import csv

# numpy module - compute average and standard deviation
import numpy as np

##
## Written by Alex Spacek
## August 2020
##

# Input file
input_file = 'chr_input.txt'

# Read in data
with open(input_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\t')
	name = []
	rating = [[] for num in range(10)]
	score = []
	for row in csv_reader:
		if len(row) == 11:
			# Read in film name:
			name = name+[row[0]]
			# Read in numbers for each rating:
			rating[0] = int(row[1])
			rating[1] = int(row[2])
			rating[2] = int(row[3])
			rating[3] = int(row[4])
			rating[4] = int(row[5])
			rating[5] = int(row[6])
			rating[6] = int(row[7])
			rating[7] = int(row[8])
			rating[8] = int(row[9])
			rating[9] = int(row[10])
			# Combine all ratings into single array:
			ratings = []
			ratings = ratings+[0.5 for num in range(rating[0])]
			ratings = ratings+[1.0 for num in range(rating[1])]
			ratings = ratings+[1.5 for num in range(rating[2])]
			ratings = ratings+[2.0 for num in range(rating[3])]
			ratings = ratings+[2.5 for num in range(rating[4])]
			ratings = ratings+[3.0 for num in range(rating[5])]
			ratings = ratings+[3.5 for num in range(rating[6])]
			ratings = ratings+[4.0 for num in range(rating[7])]
			ratings = ratings+[4.5 for num in range(rating[8])]
			ratings = ratings+[5.0 for num in range(rating[9])]
			# Compute average - standard deviation for the film:
			avg = np.average(ratings)
			stddev = np.std(ratings)
			# Record the score:
			score = score+[avg-stddev]
		else:
			# Make sure no films are being skipped:
			print(row[0])

# Sort everything by score:
sname = [fnam for fnum, fnam in sorted(zip(score,name))]
sname.reverse()
score.sort()
score.reverse()

# Print out results:
print('')
for i in range(len(sname)):
	print('{} - {} - {:4f}'.format(i+1,sname[i],score[i]))
print('')
