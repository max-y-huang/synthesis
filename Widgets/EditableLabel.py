from PyQt6.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import Qt

class EditableLabel(QWidget):
  
  def __init__(self, onChange, val='Edit me!', textAlign=Qt.AlignmentFlag.AlignLeft):
    super().__init__()

    self.editing = False

    self.onChange = onChange
    self.val = val

    self.label = QLabel(self.val)
    self.label.setAlignment(textAlign)
    self.label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    self.label.setStyleSheet('color: #c0c020; font-weight: 500;')

    self.input = MyLineEdit(self.endEdit)
    self.input.returnPressed.connect(self.endEdit)
    self.input.setAlignment(textAlign)
    self.input.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    self.input.hide()

    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(self.label)
    layout.addWidget(self.input)
    self.setLayout(layout)
  
  def mouseDoubleClickEvent(self, event):
    self.startEdit()
  
  def startEdit(self):
    if not self.editing:
      self.editing = True
      self.label.hide()
      self.input.setText(self.val)
      self.input.show()
      self.input.setFocus()
  
  def endEdit(self):
    if self.editing:
      self.editing = False
      self.val = self.input.text()
      self.input.hide()
      self.label.setText(self.val)
      self.label.show()
      self.onChange(self.val)

class MyLineEdit(QLineEdit):

  def __init__(self, onFocusOut):
    super().__init__()
    self.onFocusOut = onFocusOut

  def focusOutEvent(self, event):
    self.onFocusOut()