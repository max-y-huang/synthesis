from PyQt6.QtWidgets import QGroupBox, QSizePolicy, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor

from Widgets.WaveCanvas import WaveCanvas

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.setTitle('Output')
    self.initGUI()
  
  def initGUI(self):

    self.waveLeft = WaveCanvas(65, 0, QColor(32, 156, 255))
    self.waveRight = WaveCanvas(65, 0, QColor(32, 156, 255))

    layout = QVBoxLayout()
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(8)
    layout.addWidget(self.waveLeft)
    layout.addWidget(self.waveRight)
    self.setLayout(layout)
    self.setMinimumWidth(640)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)