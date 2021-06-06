import numpy

from Widgets.WaveCanvas import WaveCanvas

class WaveInput(WaveCanvas):

  def __init__(self, onUpdate):
    
    super().__init__(64, 1/32)
    self.prevMousePos = (0, 0)
    self.onUpdate = onUpdate
  
  def mousePressEvent(self, event):
    self.handleMouseEvent(event)
  
  def mouseMoveEvent(self, event):
    self.handleMouseEvent(event)
  
  def mouseReleaseEvent(self, event):
    self.prevMousePos = None
  
  def handleMouseEvent(self, event):
    x, y = event.position().x(), event.position().y()
    self.updateValue((self.realToCoordX(x), self.realToCoordY(y)))
  
  def updateValue(self, pos):
    # Get current and previous mouse positions.
    x, y = pos
    px, py = pos if self.prevMousePos == None else self.prevMousePos  # Previous mouse position defaults to current mouse position.
    # Make sure (px, py) comes before (x, y)
    if px > x:
      x, y, px, py = px, py, x, y
    # Update all data points from px to x.
    for i in range(px, x + 1):
      self.value[i] = numpy.interp(i, [px, x], [py, y])
    
    self.prevMousePos = pos
    self.onUpdate(self.value)
    self.repaint()