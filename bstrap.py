# Author: Omar Olivarez
# Last modified: 05/11/2021
import math
import numpy as np

def b_mean(series, reps):
	means = []
	for i in range(reps):
		s = series.sample(series.size, replace = True) # gets sample same size as the series
		# and samples with replacement
		m = s.mean()
		means.append(m)
	avg = round(sum(means) / len(means), 5)
	sd = round(np.std(means), 5)
	ci_lo = round(avg + 1.95 * sd / math.sqrt(reps), 5)
	ci_hi = round(avg - 1.95 * sd / math.sqrt(reps), 5)
	return avg, sd, ci_lo, ci_hi

def b_sd():
	return
