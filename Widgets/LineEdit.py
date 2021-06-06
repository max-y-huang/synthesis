from PyQt6.QtWidgets import QLineEdit

class LineEdit(QLineEdit):

  def __init__(self, onFocusOut=lambda: 0):
    super().__init__()
    self.onFocusOut = onFocusOut

  def focusOutEvent(self, event):
    self.onFocusOut()