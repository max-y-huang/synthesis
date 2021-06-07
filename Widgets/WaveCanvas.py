from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

import numpy

from funcs import clamp

HEIGHT = 156

class WaveCanvas(QFrame):

  padding = 24

  def __init__(self, res, snap=0):

    super().__init__()
    self.setFixedHeight(HEIGHT)
    self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    self.res = res
    self.snap = snap
    
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
    ret = numpy.interp(x, [0, self.getInnerWidth()], [0, self.res - 1])  # Map from 0 to res - 1
    ret = round(ret)                                                     # Snap to the nearest integer.
    return ret
  
  def realToCoordY(self, y):
    y = clamp(y - self.padding, 0, self.getInnerHeight())       # Remove offset and clamp inside input boundaries.
    ret = numpy.interp(y, [0, self.getInnerHeight()], [-1, 1])  # Map from -1 to 1
    if self.snap != 0:
      ret = round(ret / self.snap) * self.snap                  # Snap with respect to the snap interval.
    return ret
  
  def coordToRealX(self, x):
    return numpy.interp(x, [0, self.res - 1], [0, self.getInnerWidth()]) + self.padding
  
  def coordToRealY(self, y):
    return numpy.interp(y, [-1, 1], [0, self.getInnerHeight()]) + self.padding

  def paintEvent(self, event):

    value = self.value
    # Set data lines pen.
    pen = QPen()
    pen.setColor(QColor(192, 192, 32))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    qp = QPainter()
    qp.begin(self)
    qp.setRenderHint(QPainter.RenderHint.Antialiasing)
    # Draw data lines.
    qp.setPen(pen)
    for i in range(len(value) - 1):
      qp.drawLine(self.coordToRealX(i), self.coordToRealY(value[i]), self.coordToRealX(i + 1), self.coordToRealY(value[i + 1]))
    
    qp.end()
  
  def updateValue(self, input):
    self.value = input
    self.repaint()