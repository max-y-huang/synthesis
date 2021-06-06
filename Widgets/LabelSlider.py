from PyQt6.QtWidgets import QSizePolicy, QSlider, QSpinBox, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

from Widgets.EditableLabel import EditableLabel
from Widgets.SpinBox import SpinBox

class LabelSlider(QWidget):

  def __init__(self):

    super().__init__()

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
  
  def onLabelChanged(self, value):
    self.slider.setValue(value)
  
  def onSliderChanged(self, value):
    self.label.setValue(value)