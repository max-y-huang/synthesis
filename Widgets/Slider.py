from PyQt6.QtWidgets import QSizePolicy, QSlider, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from Widgets.EditableLabel import EditableLabel
from funcs import clamp

class Slider(QWidget):

  def __init__(self, onChange, min=0, max=100, defaultValue=50):

    super().__init__()
    self.initGUI()
    self.onChange = onChange
    self.setRange(min, max)
    self.setValue(defaultValue)
  
  def initGUI(self):

    self.slider = QSlider()
    self.slider.valueChanged.connect(self.setValue)
    self.slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.label = EditableLabel(self.setValue, 'number', 0, Qt.AlignmentFlag.AlignCenter)
    self.label.setFixedWidth(50)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.slider)
    layout.addWidget(self.label)
    self.setLayout(layout)
  
  def setValue(self, value):
    self.value = clamp(value, self.min, self.max)
    self.slider.setValue(self.value)
    self.label.setValue(self.value)
    self.onChange(self.value)

  def setRange(self, min, max):
    self.min = min
    self.max = max
    self.slider.setRange(min, max)
    self.label.input.setRange(min, max)