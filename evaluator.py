  # TODO: given a schedule, evaluates its score
  # calDict: (or print calDict to see what it is)
  #'mm/dd/yy' -> set([(away1, home1), (away2, home2), ...])

#still need to deal with distance

import sys
from timeUtil import *
from distanceReader import *
import time
import timeUtil
import collections

total = 0
teams = set()
teamScores = dict()
teamDistance = dict()
# to be determined
btbOnTotal = -25
btbOnTeam = -25
weightBtb = 0.5
weightFairness = 0.5
distanceReader = CsvReader("distances.csv")
distance = distanceReader.distanceDict


 

def allTeams(calDict):
  for date in calDict:
    s = calDict[date]
    for game in s:
      for team in game:
        teams.add(team)

def initialTeamSocores(calDict):
  for eachTeam in teams:
    teamScores[eachTeam] = 0
    teamDistance[eachTeam] = (0,None)

# return True if team not relevant in games
def inGame(team, games):
  for game in games:
    if team in game:
      return True
  return None

def backToback(calDict,team,btbNum):
  totalPanelty = 0
  totalDistance = 0
  for date in calDict:
    nextDate = nextDay(date)
    games = calDict[date]
    ##????
    if inGame(team,games):
      if (nextDate in calDict) and inGame(team,calDict[nextDate]):
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

def totalDistance(calDict,teams):
  total = 0
  for date in calDict:
    games = calDict[date]
    for game in games:
      homeTeam = game[1]
      awayTeam = game[0]
      hDistance = teamDistance[homeTeam][0]
      aDistance = teamDistance[awayTeam][0]
      if (teamDistance[awayTeam][1] == None):
        teamDistance[awayTeam] = (distance[awayTeam,homeTeam] + aDistance, homeTeam)
      else:
        previous = teamDistance[awayTeam][1]
        teamDistance[awayTeam] = (distance[awayTeam,previous] + aDistance, homeTeam)
      if (teamDistance[homeTeam][1] == None):
        teamDistance[homeTeam] = (hDistance, None)
      else:
        previous = teamDistance[awayTeam][1]
        teamDistance[homeTeam] = (distance[homeTeam,previous] + hDistance, homeTeam)
  for each in teamDistance:
    total += teamDistance[each][0]
  return total


def evaluate(calDict):
  allTeams(calDict)
  initialTeamSocores(calDict)
  btbNum = 0
  distanceSum = totalDistance(calDict, teams)
  print distanceSum
  for team in teamScores:
    teamScores[team] += backToback(calDict,team,btbNum)
  
  fairness = getVariance(teamScores) * -1
  totalScore = weightFairness * fairness + weightBtb * btbNum 
  return totalScore




