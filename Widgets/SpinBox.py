from PyQt6.QtWidgets import QSpinBox

class SpinBox(QSpinBox):

  def __init__(self, onFocusOut=lambda: 0):
    super().__init__()
    self.onFocusOut = onFocusOut

  def focusOutEvent(self, event):
    self.onFocusOut()