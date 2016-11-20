import time

PATTERN = '%m/%d/%y'


def dateToEpoch(date):
  return int(time.mktime(time.strptime(date, PATTERN)))

def epochToDate(epoch):
  return time.strftime(PATTERN, time.gmtime(epoch))


