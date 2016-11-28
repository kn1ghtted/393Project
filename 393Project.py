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
import copy
import math
from plotUtil import *

PLOT = True
DATE = 0
AWAY = 1
HOME = 3

SEARCH_DEPTH = 1000

# sequence t_i mentioned in simulated annealing algorithm
controlValues = [1 - i * 1.0/SEARCH_DEPTH for i in xrange(SEARCH_DEPTH)]

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

  # uses simulated Annealing from page 16 of pdf
  def searchSchedule(self, schedule):
    scaleFactor = None
    S.best = evaluate(schedule)
    depth = 0
    if (PLOT):
      scorePlot = Plot()
    # choose a solution s' from S randomly
    # by selecting a game randomly and swithing it with 
    # another game, making sure that all four teams involved
    # don't have games on the same day
    while (depth < SEARCH_DEPTH):
      s_score = evaluate(schedule)
      print ("s_score = %.04f" % s_score)
      if (PLOT):
        scorePlot.update(depth, s_score)
      date1 = random.choice(schedule.keys())
      game1 = random.choice(list(schedule[date1]))
      date2 = date1
      # choose the target game to switch
      # not on same day, all four games don't have 
      # same day matches after switch
      date2Valid = False
      while ((not date2Valid)):
      # ???? should we limit the range of difference between the
      # dates to switch with?          
        date2 = random.choice(schedule.keys())
        game2 = random.choice(list(schedule[date2]))
        if (date1 == date2):
          continue
        else:
          date1Games = copy.deepcopy(schedule[date1])
          date2Games = copy.deepcopy(schedule[date2])
          date1Games.remove(game1)
          date2Games.remove(game2)
          (teamA, teamB) = game1
          (teamC, teamD) = game2
          # print teamA, teamB, teamC, teamB
          # print date1Games
          # print date2Games
          if ((self.teamNoConflict(teamA, date2Games)) and \
          (self.teamNoConflict(teamB, date2Games)) and \
          (self.teamNoConflict(teamC, date1Games)) and \
          (self.teamNoConflict(teamD, date1Games))):
            date2Valid = True
      # switch games, move to s'
      self.switchGames(schedule, date1, date2, game1, game2)
      # use randomness to decide with move to s'
      randNum = random.uniform(0, 1)
      s1_score = evaluate(schedule)
      if (scaleFactor == None):
        scaleFactor = abs(s1_score - s_score)
      delta = s1_score - s_score
      condition = min(1, math.exp((delta*1.0/scaleFactor)*1.0/controlValues[depth]))
      if (randNum >= condition):
        # switch back
        self.switchGames(schedule, date2, date1, game1, game2)
      else:
        if (s1_score >= S.best):
          S.best = s1_score
        # this means we only update schedule when it's going in a better direction
        else:
          self.switchGames(schedule, date2, date1, game1, game2)
        depth += 1

S = scheduler()
intialSchedule = S.readSchedule("nba_games_2015-2016.txt")
S.searchSchedule(intialSchedule)