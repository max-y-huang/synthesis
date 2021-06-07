from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

import math, numpy

from Widgets.EditableLabel import EditableLabel

class Dial(QWidget):

  dialSize = 14
  startAngle = 5 / 4 * math.pi
  spanAngle = -3 / 2 * math.pi

  def __init__(self, min=0, max=100, defaultValue=25):

    super().__init__()
    self.max = 100
    self.min = 0
    self.setMinimumSize(80, 80)
    self.initGUI()
    self.setRange(min, max)
    self.setValue(defaultValue)
  
  def initGUI(self):

    self.label = EditableLabel(self.onLabelChanged, 'number', 0, Qt.AlignmentFlag.AlignCenter)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 0, 20, 0)
    layout.addWidget(self.label)
    self.setLayout(layout)
  
  def setValue(self, value):
    self.value = value
    self.label.setValue(value)
    self.repaint()

  def setRange(self, min, max):
    self.min = min
    self.max = max
    self.label.input.setRange(min, max)
    self.repaint()
  
  def onLabelChanged(self, value):
    self.setValue(value)
  
  def getWidth(self):
    return self.geometry().width()
  
  def getHeight(self):
    return self.geometry().height()
  
  def getCenterX(self):
    return self.getWidth() / 2
  
  def getCenterY(self):
    return self.getHeight() / 2
  
  def getRadius(self):
    return min(self.getWidth(), self.getHeight()) / 2 - self.dialSize / 2
  
  def valueToPercent(self):
    return numpy.interp(self.value, [self.min, self.max], [0, 1])
  
  def valueToPosition(self):
    angle = self.startAngle + self.valueToPercent() * self.spanAngle
    radius = self.getRadius()
    x = self.getCenterX() + radius * math.cos(angle)
    y = self.getCenterY() - radius * math.sin(angle)  # - sign to account for inverted y-axix.
    return (x, y)
  
  def positionToValue(self, x, y):

    angleDirection = -1 if self.spanAngle < 0 else 1
    dx, dy = x - self.getCenterX(), y - self.getCenterY()
    # Get angle in radians in the same coordinate system as QtAngle.
    angle = numpy.interp(math.atan2(dy, -dx), [-math.pi, math.pi], [0, 2 * math.pi])
    # Move 0 degrees to startAngle, set rotation direction to that of the dial.
    angle = (angle - self.startAngle) * angleDirection
    if angle < 0:
      angle += 2 * math.pi

    maxPercent = 2 * math.pi / abs(self.spanAngle)
    percentOverflow = maxPercent - 1
    percent = numpy.interp(angle, [0, 2 * math.pi], [0, maxPercent])
    if percent > 1 + percentOverflow / 2:
      percent -= maxPercent
    return round(numpy.interp(percent, [0, 1], [self.min, self.max]))

  def drawArc(self, qp, posX, posY, radius, startAngle, spanAngle):
    def toQtAngle(rad):
      return rad * 180 / math.pi * 16  # QtAngle = 1/16th degree.
    qp.drawArc(posX - radius, posY - radius, radius * 2, radius * 2, toQtAngle(startAngle), toQtAngle(spanAngle))
  
  def drawCircle(self, qp, posX, posY, radius):
    qp.drawEllipse(posX - radius, posY - radius, radius * 2, radius * 2)

  def paintEvent(self, event):

    # Set data lines pen.
    pen = QPen()
    pen.setColor(QColor(16, 16, 16))
    pen.setWidth(4)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)

    qp = QPainter()
    qp.begin(self)
    qp.setRenderHint(QPainter.RenderHint.Antialiasing)
    # Draw total arc.
    qp.setPen(pen)
    self.drawArc(qp, self.getCenterX(), self.getCenterY(), self.getRadius(), self.startAngle, self.spanAngle)
    # Draw value arc.
    pen.setColor(QColor(192, 192, 32))
    qp.setPen(pen)
    self.drawArc(qp, self.getCenterX(), self.getCenterY(), self.getRadius(), self.startAngle, self.valueToPercent() * self.spanAngle)
    # Draw handle.
    qp.setBrush(QColor(32, 32, 32))
    pen.setWidth(2)
    qp.setPen(pen)
    x, y = self.valueToPosition()
    self.drawCircle(qp, x, y, self.dialSize / 2 - 1)
    
    qp.end()
  
  def touching(self, x, y):
    dx, dy = x - self.getCenterX(), y - self.getCenterY()
    dist = math.sqrt(dx * dx + dy * dy)
    return abs(dist - self.getRadius()) <= self.dialSize / 2
  
  def mousePressEvent(self, event):
    if self.touching(event.position().x(), event.position().y()):
      self.handleMouseEvent(event)
  
  def mouseMoveEvent(self, event):
    self.handleMouseEvent(event)
  
  def handleMouseEvent(self, event):
    self.setValue(self.positionToValue(event.position().x(), event.position().y()))
