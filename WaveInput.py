from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

import numpy as np

from Widgets.WaveCanvas import WaveCanvas
from store import Store

class WaveInput(WaveCanvas):

  def __init__(self, onChange):
    
    super().__init__(Store.WAVE_RES, 1/32)
    self.prevMousePos = None
    self.onChange = onChange
  
  def mousePressEvent(self, event):
    self.handleMouseEvent(event, QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier)
  
  def mouseMoveEvent(self, event):
    self.handleMouseEvent(event, True)
  
  def handleMouseEvent(self, event, usePrevPos):
    x, y = event.position().x(), event.position().y()
    self.updateValue((self.realToCoordX(x), self.realToCoordY(y)), usePrevPos)
  
  def updateValue(self, pos, usePrevPos):
    # Get current and previous mouse positions.
    x, y = pos
    px, py = pos if not usePrevPos or self.prevMousePos == None else self.prevMousePos  # Previous mouse position defaults to current mouse position.
    # Make sure (px, py) comes before (x, y)
    if px > x:
      x, y, px, py = px, py, x, y
    # Update all data points from px to x.
    for i in range(px, x + 1):
      self.value[i] = np.interp(i, [px, x], [py, y])
    
    self.prevMousePos = pos
    self.onChange(self.value)
    self.repaint()