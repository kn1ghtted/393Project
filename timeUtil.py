import time

PATTERN = '%m/%d/%y'
DAY = 86400

def dateToEpoch(dateString):
  return int(time.mktime(time.strptime(dateString, PATTERN)))

def epochToDate(epoch):
  return time.strftime(PATTERN, time.gmtime(epoch))

# take in a date string, return the string representation of 
# its next day
def nextDay(dateString):
  return epochToDate(dateToEpoch(dateString) + DAY)

# take in a date string, return the string representation of 
# its prev day
def prevDay(dateString):
  return epochToDate(dateToEpoch(dateString) - DAY)


