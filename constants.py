import math

PLOT = True
DATE = 0
AWAY = 1
HOME = 3
CTRL_THRESHOLD = 0.0001
SEARCH_DEPTH = 20000

# sequence t_i mentioned in simulated annealing algorithm
# controlValues = [1 - i * 1.0/SEARCH_DEPTH for i in xrange(SEARCH_DEPTH)]
controlValues = [max(CTRL_THRESHOLD, math.pow(1.1, -1.0*i)/2) for i in xrange(SEARCH_DEPTH)]
