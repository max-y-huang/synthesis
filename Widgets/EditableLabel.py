from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from Widgets.LineEdit import LineEdit
from Widgets.SpinBox import SpinBox

class EditableLabel(QWidget):
  
  def __init__(self, onChange, type, val='Edit me!', textAlign=Qt.AlignmentFlag.AlignLeft):

    super().__init__()
    self.editing = False

    self.type = type
    self.onChange = onChange
    self.value = val
    self.initGUI(textAlign)
  
  def initGUI(self, textAlign):

    inputComponent = { 'text': LineEdit, 'number': SpinBox }

    self.label = QLabel(str(self.value))
    self.label.setAlignment(textAlign)
    self.label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    self.label.setStyleSheet('color: #c0c020; font-weight: 500;')

    self.input = inputComponent[self.type](self.endEdit)
    self.input.setAlignment(textAlign)
    self.input.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
    self.input.hide()

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.label)
    layout.addWidget(self.input)
    self.setLayout(layout)
  
  def setValue(self, value):
    self.value = value
    self.updateLabelValue()
    self.updateInputValue()
  
  def updateValue(self):
    if self.type == 'text':
      self.value = self.input.text()
    if self.type == 'number':
      self.value = self.input.value()
    self.updateLabelValue()
    self.updateInputValue()

  def updateLabelValue(self):
    self.label.setText(str(self.value))
  
  def updateInputValue(self):
    if self.type == 'text':
      self.input.setText(self.value)
    if self.type == 'number':
      self.input.setValue(self.value)

  def mouseDoubleClickEvent(self, event):
    self.startEdit()
  
  def startEdit(self):
    if self.editing:
      return
    self.editing = True
    self.label.hide()
    self.input.show()
    self.input.setFocus()
  
  def endEdit(self):
    if not self.editing:
      return
    self.editing = False
    self.updateValue()
    self.input.hide()
    self.label.show()
    self.onChange(self.value)