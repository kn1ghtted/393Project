class CsvReader:
  def __init__(self, filename):
    examples = []
    inputFile = open(filename, "r+")
    lines = [line.rstrip('\n\r') for line in inputFile]
    self.popularityDict = dict()
    for eachLine in lines:
      line = eachLine.split(",")
      print line



