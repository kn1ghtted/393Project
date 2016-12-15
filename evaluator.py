  # TODO: given a schedule, evaluates its score
  # calDict: (or print calDict to see what it is)
  #'mm/dd/yy' -> set([(away1, home1), (away2, home2), ...])

#still need to deal with distance
import datetime
import sys
from timeUtil import *
from distanceReader import *
from popularityReader import *
import time
import timeUtil
import collections
import math

GAME_SCORE_THRESHOLD = 4000

total = 0
teams = set()
teamScores = dict()
teamDistance = dict()
# to be determined
btbOnTotal = -10
btbOnTeam = -10
weightBtb = 0.3
weightFairness = 0.4
weightDistance = 0.3
distanceReader = DistanceReader("distances.csv")
distance = distanceReader.distanceDict
popularityReader = PopularityReader("Popularity new.csv")
popularityDict = popularityReader.popularityDict


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

def backToback(calDict,team):
  totalPanelty = 0
  totalDistance = 0
  counter = 0
  for date in calDict:
    nextDate = nextDay(date)
    games = calDict[date]
    if inGame(team,games):
      if (nextDate in calDict) and inGame(team,calDict[nextDate]):
        counter += 1
        totalPanelty += btbOnTeam
  return (totalPanelty,counter)


def getStdDev(teamScores):
  total = 0
  for team in teamScores:
    total += teamScores[team]
  mean = total * 1.0 /len(teams)
  variance = 0
  for team in teamScores:
    variance += (teamScores[team] - mean)**2
  variance = variance * 1.0 / len(teams)
  return math.sqrt(variance)

def popularity(calDict):
  popularityPoint = 0
  for date in calDict:
    month, day, year = (int(x) for x in date.split('/'))
    year = 2000 + year  
    ans = datetime.date(year, month, day)
    weekday = ans.strftime("%A")
    games = calDict[date]
    if weekday == "Friday":
        for game in games:
            totalScore = popularityDict[game[0]] + popularityDict[game[1]]
            if (totalScore ** 2) > GAME_SCORE_THRESHOLD:
                print game[0], game[1], (totalScore) ** 2 - GAME_SCORE_THRESHOLD
                popularityPoint += (totalScore) ** 2 - GAME_SCORE_THRESHOLD
    if date == "12/25/2015":
        for game in games:
            totalScore = popularityDict[game[0]] + popularityDict[game[1]]
            if totalScore > GAME_SCORE_THRESHOLD:
                popularityPoint += totalScore ** 2
  return popularityPoint


 
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
  for team in teamScores:
    teamScoreDelta, btbNumDelta = backToback(calDict,team)
    teamScores[team] += teamScoreDelta
    btbNum += btbNumDelta
  btbStdev = getStdDev(teamScores)
  teamD = dict()
  for each in teamDistance:
    teamD[each] = teamDistance[each][0]
  distanceStdev = getStdDev(teamD)
  popularityScore = popularity(calDict)
  totalScore = -0.1 * btbStdev + -0.6 * btbNum + distanceStdev * (- 0.1)  /1000 + - 0.5 * (distanceSum/1000) + popularityScore
  retObject = {}
  retObject["score"] = totalScore
  retObject["btbNum"] = btbNum
  retObject["btbStdev"] = btbStdev
  retObject["distanceSum"] = distanceSum
  retObject["distanceStdev"] = distanceStdev
  retObject["popularityScore"] = popularityScore
  # print "popularityScore = ", popularityScore
  sys.exit(0)
  return retObject

