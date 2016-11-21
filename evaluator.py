  # TODO: given a schedule, evaluates its score
  # calDict: (or print calDict to see what it is)
  #'mm/dd/yy' -> set([(away1, home1), (away2, home2), ...])

#still need to deal with distance

import sys
from timeUtil import *
import time
import timeUtil
import collections

total = 0
teams = set()
teamScores = dict()
# to be determined
btbOnTotal = -25
btbOnTeam = -25
weightBtb = 0.5
weightFairness = 0.5

def allTeams(calDict):
  for date in calDict:
    s = calDict[date]
    for game in s:
      for team in game:
        teams.add(team)

def initialTeamSocores(calDict):
  for eachTeam in teams:
    teamScores[eachTeam] = 0

# return True if team not relevant in games
def inGame(team, games):
  for game in games:
    if team in game:
      return True
  return False

def backToback(calDict,team,btbNum):
  totalPanelty = 0
  for date in calDict:
    nextDate = nextDay(date)
    games = calDict[date]
    ##????
    if inGame(team,games):
      if (nextDate in calDict) and inGame(team,calDict[nextDate]):
        print "found back to back"
        btbNum += 1
        totalPanelty += btbOnTeam
  return totalPanelty

def getVariance(teamScores):
  total = 0
  for team in teamScores:
    total += teamScores[team]
  mean = total/len(teams)
  variance = 0
  for team in teamScores:
    variance += (teamScores[team] - mean)**2
  variance /= len(teams)
  return variance




def evaluate(calDict):
  allTeams(calDict)
  initialTeamSocores(calDict)
  #????
  btbNum = 0
  for team in teamScores:
    teamScores[team] += backToback(calDict,team,btbNum)
  fairness = getVariance(teamScores) * -1
  totalScore = weightFairness * fairness + weightBtb * btbNum
  return totalScore