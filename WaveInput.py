from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line, PushMatrix, PopMatrix, Translate

import numpy, math
from functools import reduce
from copy import copy, deepcopy
from random import random

from color import rgb
from funcs import clamp

class WaveInput(Widget):

  output_zoom = 1 / 2

  def __init__(self, x, y, w, h, padding=16, num_points=64):
    super(WaveInput, self).__init__()
    # Initialize position, size, points.
    self.prev_touch = None
    self.set_dimensions(x, y, w, h, padding, num_points)
    self.input = [0] * num_points
    self.waves = []
    self.output = [0] * self.output_w
    # Add draw instructions.
    self.draw_background()
    self.draw_input_line()
    self.draw_output_line()
  
  def set_dimensions(self, x, y, w, h, padding, num_points):
    self.pos_x = x
    self.pos_y = y
    self.w = w
    self.h = h
    self.padding = padding
    self.num_points = num_points
    self.input_w = w - 2 * padding
    self.input_h = (h - 4 * padding) * 11 / 16
    self.output_w = w - 2 * padding
    self.output_h = (h - 4 * padding) * 5 / 16
    self.pos = (x, y)
    self.size = (w, h)

  def touch_pos(self, touch):
    x = touch.pos[0] - (self.pos_x + self.padding)
    y = touch.pos[1] - (self.pos_y + self.padding)
    return (x, y)

  def generate_waves(self, samples):

    N = self.num_points
    samples = min(samples, self.num_points)
    fft = numpy.fft.fft(self.input)[0:samples]

    self.waves.clear()
    for k, c in enumerate(fft):
      speed = 2 * math.pi * k / N
      self.waves.append({
        'amp': 1 / N * c.real,
        'speed': speed,
        'offset': 0
      })
      self.waves.append({
        'amp': -1 / N * c.imag,
        'speed': speed,
        'offset': -math.pi / 2
      })
  
  def generate_output(self):
    def get_y(acc, n, x):
      return acc + n['amp'] * math.cos(n['speed'] * x + n['offset'])

    max_y = -10000000
    min_y =  10000000

    self.output.clear()
    for raw_x in range(self.output_w):
      x = raw_x / self.points_spacing()
      y = reduce(lambda acc, n: get_y(acc, n, x), self.waves, 0)
      self.output.append(y)
      max_y = max(y, max_y)
      min_y = min(y, min_y)
    
    for i in range(len(self.output)):
      self.output[i] = numpy.interp(self.output[i], [min_y, max_y], [-1, 1])

  def points_spacing(self):
    return self.input_w / (self.num_points - 1)
  
  def get_input_line_points(self):
    def get_coord(x):
      return (x * self.points_spacing(), self.input[x] * self.input_h / 2)
    
    return list(map(get_coord, range(self.num_points)))

  def get_output_line_points(self):
    N = len(self.output)
    zoom = self.output_zoom
    def get_coord(x):
      new_x = int(x / zoom - ((1 - zoom) / 2) / zoom * N)
      return (x, self.output[new_x % N] * self.output_h / 2)
    
    return list(map(get_coord, range(N)))
    
  def touching(self, touch):
    tx, ty = self.touch_pos(touch)
    p = self.padding
    return tx >= -p and tx <= self.input_w + p and ty >= -p and ty <= self.input_h + p
  
  def touch_to_wave_pos(self, touch):
    tx, ty = self.touch_pos(touch)
    pos = clamp(round(tx / self.points_spacing()), 0, self.num_points - 1)
    val = (clamp(ty, 0, self.input_h) - self.input_h / 2) / (self.input_h / 2)
    return (pos, val)

  def draw_background(self):
    # TODO: Clean up.
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x, self.pos_y)
      rgb(24, 24, 24)
      Rectangle(pos=(0, 0), size=(self.input_w + 2 * self.padding, self.input_h + 2 * self.padding))
      rgb(16, 16, 16)
      Rectangle(pos=(0, self.input_h + 2 * self.padding), size=(self.output_w + 2 * self.padding, self.output_h + 2 * self.padding))
      rgb(32, 32, 16)
      Rectangle(pos=(self.output_w * ((1 - self.output_zoom) / 2) + self.padding, self.input_h + 2 * self.padding), size=(self.output_w * self.output_zoom, self.output_h + 2 * self.padding))
      PopMatrix()

  def remove_input_line(self):
    with self.canvas:
      self.canvas.remove(self.input_line)
  
  def draw_input_line(self):
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x + self.padding, self.pos_y + self.padding + self.input_h / 2)
      rgb(96, 96, 255)
      self.input_line = Line(points=self.get_input_line_points(), width=2)
      PopMatrix()
  
  def remove_output_line(self):
    with self.canvas:
      self.canvas.remove(self.output_line)
  
  def draw_output_line(self):
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x + self.padding, self.pos_y + self.input_h + 3 * self.padding + self.output_h / 2)
      rgb(221, 221, 32)
      self.output_line = Line(points=self.get_output_line_points(), width=1.5)
      PopMatrix()

  def on_touch_down(self, touch):
    super(WaveInput, self).on_touch_down(touch)
    self.handle_touch(copy(touch))

  def on_touch_move(self, touch):
    self.handle_touch(copy(touch))
  
  def on_touch_up(self, touch):
    self.prev_touch = None
  
  def handle_touch(self, touch):
    if self.touching(touch):
      self.update_wave(touch)
    self.prev_touch = touch

  # Update the wave based on the user's touch position.
  def update_wave(self, touch):
    # Get touch positions (current and previous).
    pos, val = self.touch_to_wave_pos(touch)
    prev_pos, prev_val = self.touch_to_wave_pos(touch if self.prev_touch == None else self.prev_touch)
    
    with self.canvas:
      # Set new position values from the start point to the end point.
      start_pos, end_pos, start_val, end_val = (pos, prev_pos, val, prev_val) if prev_pos > pos else (prev_pos, pos, prev_val, val)
      for i in range(start_pos, end_pos + 1):
        self.input[i] = numpy.interp(i, [start_pos, end_pos], [start_val, end_val])
      # Reset input line.
      self.remove_input_line()
      self.draw_input_line()
      # Generate waves and reset output line.
      self.generate_waves(self.num_points // 2)
      self.generate_output()
      self.remove_output_line()
      self.draw_output_line()