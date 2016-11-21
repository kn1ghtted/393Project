#Variable: X_i_j_d

# 30 choose 2 = 435
# d = 
# assumption: use same game dates for 

from evaluator import *
from csvreader import *
import time
import timeUtil
import random
import collections

DATE = 0
AWAY = 1
HOME = 3


SEARCH_DEPTH = 100

# sequence t_i mentioned in simulated annealing algorithm
controlValues = [(1.0/x)**2 for x in xrange(1, SEARCH_DEPTH)]

class scheduler:
  def __init__(self):
    return

  # given a schedule file,
  # return a dictionary type of the schedule:
  # 'mm/dd/yy' -> set([(away1, home1), (away2, home2), ...])
  def readSchedule(self, filename):
    reader = CsvReader(filename)
    cal = reader.data  
    attributes = reader.attributes
    # change datetime column to only datetime
    schedule = collections.OrderedDict()
    for gameEntry in reader.data:
      date = gameEntry[DATE].split(" ")[DATE]
      epoch = timeUtil.dateToEpoch(date)
      standardDate = timeUtil.epochToDate(epoch)
      gameEntry[DATE] = standardDate
      awayTeam = gameEntry[AWAY]
      homeTeam = gameEntry[HOME]
      game = (awayTeam, homeTeam)
      # if this date already stored
      if standardDate in schedule:
        schedule[standardDate].add(game)
      else:
        schedule[standardDate] = set([game])
    return schedule

  # uses simulated Annealing from page 16 of pdf
  def searchSchedule(self, schedule):
    best = evaluate(schedule)
    depth = 0
    # choose a solution s' from S randomly
    # by selecting a game randomly and swithing it with 
    # another game, making sure that all four teams involved
    # don't have games on the same day
    while (depth <= SEARCH_DEPTH):
      # choose the source game to switch
      date1 = random.choice(schedule.keys())
      game1 = random.choice(list(schedule[date1]))
      # choose the target game to switch
      # ???? should we limit the range of difference between the
      # dates to switch with?
      date2 = date1
      while (date2 == date1):
        print date1, date2
        date2 = random.choice(schedule.keys())
      game2 = random.choice(list(schedule[date2]))
      


S = scheduler()
intialSchedule = S.readSchedule("nba_games_2015-2016.txt")
print evaluate(intialSchedule)


