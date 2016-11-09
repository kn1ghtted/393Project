#Variable: X_i_j_d

# 30 choose 2 = 435
# d = 
# assumption: use same game dates for 



from csvreader import *

class project:
  def __init__(self):
    return

  def readSchedule(self, filename):
    reader = CsvReader(filename)
    data = reader.data  
    attributes = reader.attributes
    print attributes


P = project()
P.readSchedule("nba_games_2015-2016.txt")
