from PyQt6.QtWidgets import QSizePolicy, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from Widgets.EditableLabel import EditableLabel

class LabelSlider(QWidget):

  def __init__(self, min=0, max=100, defaultValue=50):

    super().__init__()
    self.initGUI()
    self.setRange(min, max)
    self.setValue(defaultValue)
  
  def initGUI(self):

    self.slider = QSlider()
    self.slider.valueChanged.connect(self.onSliderChanged)
    self.slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.label = EditableLabel(self.onLabelChanged, 'number', 0, Qt.AlignmentFlag.AlignCenter)
    self.label.setFixedWidth(50)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.slider)
    layout.addWidget(self.label)
    self.setLayout(layout)
  
  def setValue(self, value):
    self.slider.setValue(value)  # Changing slider value changes label value.

  def setRange(self, min, max):
    self.slider.setRange(min, max)
    self.label.input.setRange(min, max)
  
  def onLabelChanged(self, value):
    self.slider.setValue(value)
  
  def onSliderChanged(self, value):
    self.label.setValue(value)