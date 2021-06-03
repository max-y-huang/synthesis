from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line, PushMatrix, PopMatrix, Translate

import numpy, math
from functools import reduce
from copy import copy, deepcopy

from color import rgb

class WaveOutput(Widget):

  def __init__(self, x, y, w, h, padding=16, num_points=64):
    super(WaveOutput, self).__init__()
    # Initialize position, size, points.
    self.prev_touch = None
    self.set_dimensions(x, y, w, h, padding, num_points)
    self.output = [0] * self.inner_w
    # Add draw instructions.
    self.draw_background()
    self.draw_line()
  
  def set_dimensions(self, x, y, w, h, padding, num_points):
    self.pos_x = x
    self.pos_y = y
    self.w = w
    self.h = h
    self.padding = padding
    self.num_points = num_points
    self.inner_w = w - 2 * padding
    self.inner_h = h - 2 * padding
    self.pos = (x, y)
    self.size = (w, h)

  def touch_pos(self, touch):
    x = touch.pos[0] - (self.pos_x + self.padding)
    y = touch.pos[1] - (self.pos_y + self.padding)
    return (x, y)
  
  def generate_output(self, input):
    def get_y(acc, n, x):
      return acc + n['amp'] * math.cos(n['speed'] * x + n['offset'])

    max_y = -10000000
    min_y =  10000000

    output = []
    for raw_x in range(self.inner_w):
      x = raw_x / (self.inner_w / (len(input) - 1))
      y = reduce(lambda acc, n: get_y(acc, n, x), input, 0)
      output.append(y)
      max_y = max(y, max_y)
      min_y = min(y, min_y)
    
    self.output = numpy.interp(output, [min_y, max_y], [0, 0] if min_y == max_y else [-1, 1])

  def get_line_points(self):
    N = len(self.output)
    def get_coord(x):
      new_x = x
      return (x, self.output[new_x % N] * self.inner_h / 2)
    
    return list(map(get_coord, range(N)))

  def draw_background(self):
    # TODO: Clean up.
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x, self.pos_y)
      rgb(16, 16, 16)
      Rectangle(pos=(0, 0), size=(self.w, self.h))
      PopMatrix()
  
  def remove_line(self):
    with self.canvas:
      self.canvas.remove(self.line)
  
  def draw_line(self):
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x + self.padding, self.pos_y + self.padding + self.inner_h / 2)
      rgb(221, 221, 32)
      self.line = Line(points=self.get_line_points(), width=1.5)
      PopMatrix()
  
  def update(self, input):
    self.generate_output(input)
    self.remove_line()
    self.draw_line()