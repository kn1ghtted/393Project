class DistanceReader:
  def __init__(self, filename):
    examples = []
    inputFile = open(filename, "r+")
    lines = [line.rstrip('\n\r') for line in inputFile]
    cities = lines.pop(0)
    self.cities = [city.strip() for city in cities.split(",")]
    self.cities.pop(0)
    self.distanceDict = dict()
    for each in lines:
      distances = each.split(",")
      current = distances.pop(0)
      for i in xrange(len(self.cities)):
        againstCity = self.cities[i]
        key = (current,againstCity)
        self.distanceDict[key] = int(distances[i])

