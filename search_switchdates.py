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



class searcherSwitchDates(searcher):
  def switchBack(self):
    schedule = self.schedule
    temp = schedule[self.date1]
    schedule[self.date1] = schedule[self.date2]
    schedule[self.date2] = temp

  def generateNewSchedule(self):
    schedule = self.schedule
    self.date1 = random.choice(schedule.keys())
    self.date2 = self.date1
    while (self.date1 == self.date2):
    # ???? should we limit the range of difference between the
    # dates to switch with?          
      self.date2 = random.choice(schedule.keys())
    # print self.date1, self.date2
    # print schedule[self.date1], schedule[self.date2]
    temp = schedule[self.date1]
    schedule[self.date1] = schedule[self.date2]
    schedule[self.date2] = temp
    # print schedule[self.date1], schedule[self.date2]





S = searcherSwitchDates()
S.readSchedule("nba_games_2015-2016.txt")
S.searchSchedule()