from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QSizePolicy, QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

class ScrollGroupBox(QGroupBox):

  def __init__(self, title, scrollComponent):

    super().__init__()
    self.setTitle(title)
    self._initGUI(scrollComponent)
  
  def _initGUI(self, scrollComponent):

    self._scrollLayout = scrollComponent()

    scrollWidget = QWidget()
    scrollWidget.setLayout(self._scrollLayout)
    scrollWidget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    self._scrollArea = QScrollArea()
    self._scrollArea.setWidgetResizable(True)
    self._scrollArea.setWidget(scrollWidget)
    self._scrollArea.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

    self._layout = scrollComponent()
    self._layout.addWidget(self._scrollArea)
    self.setLayout(self._layout)
  
  def addWidget(self, widget):
    self._scrollLayout.addWidget(widget)
  
  def addLayout(self, layout):
    self._scrollLayout.addLayout(layout)
  
  def setSpacing(self, spacing):
    self._scrollLayout.setSpacing(spacing)


class VScrollGroupBox(ScrollGroupBox):

  def __init__(self, title):

    super().__init__(title, QVBoxLayout)
    self._scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self._scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self._scrollLayout.setContentsMargins(0, 0, 12, 0)
    self._layout.setContentsMargins(16, 16, 4, 16)


class HScrollGroupBox(ScrollGroupBox):

  def __init__(self, title):

    super().__init__(title, QHBoxLayout)
    self._scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    self._scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    self._scrollLayout.setContentsMargins(0, 0, 0, 12)
    self._layout.setContentsMargins(16, 16, 16, 4)