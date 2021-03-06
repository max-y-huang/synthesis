from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

import numpy as np

from funcs import clamp

HEIGHT = 144

class WaveCanvas(QFrame):

  padding = 24

  def __init__(self, res, snap=0, compress=1, color=QColor(192, 192, 32), drawGridLines=True):

    super().__init__()
    self.setFixedHeight(HEIGHT)
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    self.res = res
    self.snap = snap
    self.compress = compress
    self.color = color
    self.drawGridLines = drawGridLines
    
    self.value = [0] * self.res
  
  def getWidth(self):
    return self.geometry().width()
  
  def getHeight(self):
    return self.geometry().height()
  
  def getInnerWidth(self):
    return self.getWidth() - 2 * self.padding
  
  def getInnerHeight(self):
    return self.getHeight() - 2 * self.padding
  
  def realToCoordX(self, x):
    x = clamp(x - self.padding, 0, self.getInnerWidth())                 # Remove offset and clamp inside input boundaries.
    ret = np.interp(x, [0, self.getInnerWidth()], [0, self.res - 1])  # Map from 0 to res - 1
    ret = round(ret)                                                     # Snap to the nearest integer.
    return ret
  
  def realToCoordY(self, y):
    y = clamp(y - self.padding, 0, self.getInnerHeight())       # Remove offset and clamp inside input boundaries.
    ret = np.interp(y, [0, self.getInnerHeight()], [1, -1])  # Map from 1 to -1
    if self.snap != 0:
      ret = round(ret / self.snap) * self.snap                  # Snap with respect to the snap interval.
    return ret
  
  def coordToRealX(self, x):
    return np.interp(x, [0, self.res - 1], [0, self.getInnerWidth()]) + self.padding
  
  def coordToRealY(self, y):
    return np.interp(-y, [-1, 1], [0, self.getInnerHeight()]) + self.padding  # Using -y and [-1, 1] because range [1, -1].

  def paintEvent(self, event):

    value = self.value
    # Set data lines pen.
    pen = QPen()
    pen.setColor(QColor(24, 24, 24))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    qp = QPainter()
    qp.begin(self)
    qp.setRenderHint(QPainter.RenderHint.Antialiasing)
    qp.setPen(pen)
    # Draw grid lines.
    if self.drawGridLines:
      self.drawHGridLine(qp, 0)
      self.drawVGridLine(qp, 0)
      self.drawHGridLine(qp, 1 / 2)
      self.drawHGridLine(qp, -1 / 2)
      self.drawVGridLine(qp, 1 / 2)
      self.drawVGridLine(qp, -1 / 2)
    # Draw data lines.
    pen.setColor(self.color)
    qp.setPen(pen)
    for i in range(len(value) * self.compress - 1):
      a = i % len(value)
      b = (i + 1) % len(value)
      qp.drawLine(self.coordToRealX(i / self.compress), self.coordToRealY(value[a]), self.coordToRealX((i + 1) / self.compress), self.coordToRealY(value[b]))
    
    qp.end()
  
  def drawHGridLine(self, qp, pos):
    y = self.getHeight() / 2 + self.getInnerHeight() / 2 * pos
    qp.drawLine(self.padding, y, self.getWidth() - self.padding, y)
  
  def drawVGridLine(self, qp, pos):
    x = self.getWidth() / 2 + self.getInnerWidth() / 2 * pos
    qp.drawLine(x, self.padding, x, self.getHeight() - self.padding)
  
  def updateValue(self, input):
    self.value = input
    self.repaint()