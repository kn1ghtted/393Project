class CsvReader:
  def __init__(self, filename):
    examples = []
    inputFile = open(filename, "r+")
    lines = [line.rstrip('\n\r') for line in inputFile]
    self.attributes = [field.strip() for field in (lines[0].split(","))]
    self.labelIndex = len(self.attributes) - 1
    self.data = []
    for i in xrange(1, len(lines)):
      self.data.append([value.strip() for value in lines[i].split(",")])