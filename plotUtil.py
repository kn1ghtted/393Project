import matplotlib
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
import numpy as np

# You probably won't need this if you're embedding things in a tkinter plot...

class Plot:
  def __init__(self):
    plt.ion()
    self.fig, self.ax1 = plt.subplots()
    # self.ax1 = plt.gca()
    self.line1, = self.ax1.plot([], [], 'b-')
    self.ax1.set_xlabel('Updated Iterations')
    self.ax1.set_ylabel('Score')
    
  def update(self, x, y):
    self.line1.set_xdata(np.append(self.line1.get_xdata(), np.array([x])))
    self.line1.set_ydata(np.append(self.line1.get_ydata(), np.array([y])))
    self.ax1.relim()
    self.ax1.autoscale_view()
    plt.draw()