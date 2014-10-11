import csv
import error_geometry
import numpy as np
import math


readCsv = []

with open('Square_Box/_slash_scan1.csv', 'rb') as csvfile:
	for line in csvfile.readlines():
		array = line.split(',')
		readCsv.append(array)
		print array

print len(readCsv)
angleSpacer = float(readCsv[2])
angles = np.arange(0, 2*math.pi,angleSpacer)
anglesList = angles.tolist()
angleRanges = {}

for angle in angles:
	angleRanges[angle] = []

for line in readCsv:
	distances = line[3:]
	print distances

