import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as pyplot

# You probably won't need this if you're embedding things in a tkinter plot...

class Plot:
  def __init__(self):
    plt.ion()
    self.ax = pyplot.gca()
    self.line1, = plt.plot([], [])

  def update(self, x, y):
    self.line1.set_xdata(np.append(self.line1.get_xdata(), np.array([x])))
    self.line1.set_ydata(np.append(self.line1.get_ydata(), np.array([y])))
    self.ax.relim()
    self.ax.autoscale_view()
    plt.draw()
