#Variable: X_i_j_d

# 30 choose 2 = 435
# d = 
# assumption: use same game dates for 

from myOrderedDict import MyOrderedDict
from evaluator import *
from csvreader import *
import time
import timeUtil
import random
import collections
import copy
from plotUtil import *
from constants import *

class searcher:
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
    schedule = MyOrderedDict()
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
    self.schedule = schedule

  # return True if team not relevant in games
  def teamNoConflict(self, team, games):
    for game in games:
      if team in game:
        return False
    return True

  def switchGames(self, schedule, date1, date2, game1, game2):
    assert(game1 in schedule[date1])
    assert(game2 in schedule[date2])
    schedule[date1].remove(game1)
    schedule[date2].remove(game2)
    schedule[date1].add(game2)
    schedule[date2].add(game1)
  def generateNewSchedule(self):
    pass

  def switchBack(self):
    pass
  # uses simulated Annealing from page 16 of pdf
  def searchSchedule(self):
    schedule = self.schedule
    scaleFactor = None
    self.best = evaluate(schedule)["score"]
    depth = 0
    update = 0

    if (PLOT):
      scorePlot = Plot()
    # choose a solution s' from S randomly
    # by selecting a game randomly and swithing it with 
    # another game, making sure that all four teams involved
    # don't have games on the same day
    while (depth < SEARCH_DEPTH):
      retObject = evaluate(schedule)
      s_score = retObject["score"]
      btbNum, btbStdev, distanceSum, distanceStdev = retObject["btbNum"], \
        retObject["btbStdev"], retObject["distanceSum"], retObject["distanceStdev"]
      totalBtbs = 1
      print ("[%d, %d], s_score = %.04f, btbNum = %d, btbStdev = %.04f, distanceSum = %.04f, distanceStdev = %.04f" % (depth, update, s_score, btbNum, btbStdev, distanceSum, distanceStdev))
      print 
      if (PLOT):
        scorePlot.update(update, s_score)
      self.generateNewSchedule()
      # use randomness to decide with move to s'
      randNum = random.uniform(0.0, 1.0)
      s1_object = evaluate(schedule)
      s1_score = s1_object["score"]
      if (scaleFactor == None):
        scaleFactor = abs(s1_score - s_score)
      delta = s1_score - s_score
      # condition = min(1, math.exp((delta*1.0/scaleFactor)*1.0/controlValues[update]))
      exponent = min(0, (delta*1.0/scaleFactor)*1.0/controlValues[update])
      condition = math.exp(exponent)
      # print "delta = %.04f, randNum = %.04f, condition = %.04f" % (delta, randNum, condition)
      if (randNum >= condition):
        # switch back
        self.switchBack()
      else:
        if (s1_score >= self.best):
          self.best = s1_score
        # this means we only update schedule when it's going in a better direction
        # else:
        #   self.switchGames(schedule, date2, date1, game1, game2)
        update += 1
      depth += 1
