from searcher import *
from myOrderedDict import MyOrderedDict
from evaluator import *
from csvreader import *
import time
import timeUtil
import random
import collections
import copy
import math
from plotUtil import *
from constants import *



class searcherSwitchGames(searcher):
  def switchBack(self):
      self.switchGames(self.schedule, self.date2, self.date1, self.game1, self.game2)

  def generateNewSchedule(self):
    schedule = self.schedule
    self.date1 = random.choice(schedule.keys())
    self.game1 = random.choice(list(schedule[self.date1]))
    self.date2 = self.date1
    # choose the target game to switch
    # not on same day, all four games don't have 
    # same day matches after switch
    date2Valid = False
    while ((not date2Valid)):
    # ???? should we limit the range of difference between the
    # dates to switch with?          
      self.date2 = random.choice(schedule.keys())
      self.game2 = random.choice(list(schedule[self.date2]))
      if (self.date1 == self.date2):
        continue
      else:
        date1Games = copy.deepcopy(schedule[self.date1])
        date2Games = copy.deepcopy(schedule[self.date2])
        date1Games.remove(self.game1)
        date2Games.remove(self.game2)
        (teamA, teamB) = self.game1
        (teamC, teamD) = self.game2
        if ((self.teamNoConflict(teamA, date2Games)) and \
        (self.teamNoConflict(teamB, date2Games)) and \
        (self.teamNoConflict(teamC, date1Games)) and \
        (self.teamNoConflict(teamD, date1Games))):
          date2Valid = True
    # switch games, move to s'
    self.switchGames(schedule, self.date1, self.date2, self.game1, self.game2)


S = searcherSwitchGames()
S.readSchedule("nba_games_2015-2016.txt")
S.searchSchedule()