from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

import math, numpy

from Widgets.EditableLabel import EditableLabel
from funcs import clamp

class LabelDial(QWidget):

  def __init__(self, text, onChange, min=0, max=100, defaultValue=50):

    super().__init__()

    self.dial = Dial(onChange, min, max, defaultValue)

    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(self.dial)
    layout.addWidget(label)
    self.setLayout(layout)
  
  def getValue(self):
    return self.dial.value

  def setValue(self, value):
    self.dial.setValue(value)
  
  def setRange(self, min, max):
    self.dial.setRange(min, max)


class Dial(QWidget):

  dialSize = 14
  startAngle = 5 / 4 * math.pi
  spanAngle = -3 / 2 * math.pi

  def __init__(self, onChange, min=0, max=100, defaultValue=50):

    super().__init__()
    self.onChange = onChange
    self.max = 100
    self.min = 0
    self.setFixedSize(82, 72)
    self.initGUI()
    self.setRange(min, max)
    self.setValue(defaultValue)
  
  def initGUI(self):

    self.label = EditableLabel(self.setValue, 'number', 0, Qt.AlignmentFlag.AlignCenter)
    
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 5, 20, 0)
    layout.addWidget(self.label)
    self.setLayout(layout)

  def setValue(self, value):
    self.value = clamp(value, self.min, self.max)
    self.label.setValue(self.value)
    self.repaint()
    self.onChange(self.value)

  def setRange(self, min, max):
    self.min = min
    self.max = max
    self.label.input.setRange(min, max)
    self.repaint()
  
  def getWidth(self):
    return self.geometry().width()
  
  def getHeight(self):
    return self.geometry().height()
  
  def getCenterX(self):
    return 41
  
  def getCenterY(self):
    return 41
  
  def getRadius(self):
    return 32
  
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
    # qp.drawRect(0, 0, self.getWidth(), self.getHeight())
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

  def wheelEvent(self, event):
    self.setValue(round(self.value + event.angleDelta().y() / 40))
