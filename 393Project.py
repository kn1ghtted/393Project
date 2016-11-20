#Variable: X_i_j_d

# 30 choose 2 = 435
# d = 
# assumption: use same game dates for 


from csvreader import *
import time
import timeUtil
import collections

DATE = 0
AWAY = 1
HOME = 3

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
    calDict = collections.OrderedDict()
    for gameEntry in reader.data:
      date = gameEntry[DATE].split(" ")[DATE]
      epoch = timeUtil.dateToEpoch(date)
      standardDate = timeUtil.epochToDate(epoch)
      gameEntry[DATE] = standardDate
      # if this date already stored
      awayTeam = gameEntry[AWAY]
      homeTeam = gameEntry[HOME]
      game = (awayTeam, homeTeam)
      if standardDate in calDict:
        calDict[standardDate].add(game)
      else:
        calDict[standardDate] = set([game])
      return calDict

  # TODO: given a schedule, evaluates its score
  # calDict: (or print calDict to see what it is)
  #'mm/dd/yy' -> set([(away1, home1), (away2, home2), ...])

  def evaluateSchedule(calDict):
    return 0

  def searchSchedule(calDict):
    



S = scheduler()
S.readSchedule("nba_games_2015-2016.txt")


