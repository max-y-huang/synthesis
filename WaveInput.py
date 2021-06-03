from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line, PushMatrix, PopMatrix, Translate

import numpy
from copy import copy

from color import rgb
from funcs import clamp

class WaveInput(Widget):

  snap = 1 / 16
  padding = 16
  num_points = 64

  def __init__(self, x, y, w, h, on_update):
    super(WaveInput, self).__init__()
    # Initialize position, size, points.
    self.prev_touch = None
    self.on_update = on_update
    self.set_dimensions(x, y, w, h)
    self.input = [0] * self.num_points
    # Add draw instructions.
    self.draw_background()
    self.draw_line()
  
  def set_dimensions(self, x, y, w, h):
    self.pos_x = x
    self.pos_y = y
    self.w = w
    self.h = h
    self.inner_w = w - 2 * self.padding
    self.inner_h = h - 2 * self.padding
    self.pos = (x, y)
    self.size = (w, h)

  def touch_pos(self, touch):
    x = touch.pos[0] - (self.pos_x + self.padding)
    y = touch.pos[1] - (self.pos_y + self.padding)
    return (x, y)

  def points_spacing(self):
    return self.inner_w / (self.num_points - 1)
  
  def get_line_points(self):
    def get_coord(x):
      return (x * self.points_spacing(), self.input[x] * self.inner_h / 2)
    
    return list(map(get_coord, range(self.num_points)))
    
  def touching(self, touch):
    tx, ty = self.touch_pos(touch)
    p = self.padding
    return tx >= -p and tx <= self.inner_w + p and ty >= -p and ty <= self.inner_h + p
  
  def touch_to_wave_pos(self, touch):
    tx, ty = self.touch_pos(touch)
    pos = clamp(round(tx / self.points_spacing()), 0, self.num_points - 1)
    val = round((clamp(ty, 0, self.inner_h) - self.inner_h / 2) / (self.inner_h / 2) / self.snap) * self.snap
    return (pos, val)

  def draw_background(self):
    # TODO: Clean up.
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x, self.pos_y)
      rgb(24, 24, 24)
      Rectangle(pos=(0, 0), size=(self.w, self.h))
      Translate(0, self.h / 2)
      rgb(48, 48, 48)
      Line(points=[(0, 0), (self.w, 0)], width=1.5, cap='none')
      Line(points=[(0,  self.inner_h // 2), (self.w,  self.inner_h // 2)], width=1.5, cap='none')
      Line(points=[(0, -self.inner_h // 2), (self.w, -self.inner_h // 2)], width=1.5, cap='none')
      rgb(32, 32, 32)
      Line(points=[(0,  self.inner_h // 4), (self.w,  self.inner_h // 4)], width=1.5, cap='none')
      Line(points=[(0, -self.inner_h // 4), (self.w, -self.inner_h // 4)], width=1.5, cap='none')
      PopMatrix()

  def remove_line(self):
    with self.canvas:
      self.canvas.remove(self.line)
  
  def draw_line(self):
    with self.canvas:
      PushMatrix()
      Translate(self.pos_x + self.padding, self.pos_y + self.padding + self.inner_h / 2)
      rgb(96, 96, 255)
      self.line = Line(points=self.get_line_points(), width=2)
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
      self.remove_line()
      self.draw_line()
    
    self.on_update(self.input)