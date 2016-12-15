class PopularityReader:
  def __init__(self, filename):
    examples = []
    inputFile = open(filename, "r+")
    lines = [line.rstrip('\n\r') for line in inputFile]
    self.popularityDict = dict()
    for eachLine in lines:
        data = eachLine.split(",")
        city = data[0]
        value = data[1]
        self.popularityDict[city] = float(value)

