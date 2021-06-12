from PyQt6.QtWidgets import QGroupBox, QSizePolicy, QVBoxLayout
from PyQt6.QtGui import QColor

from Widgets.WaveCanvas import WaveCanvas
from store import Store

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.setTitle('Output')
    self.initGUI()
  
  def initGUI(self):

    self.waveLeft = WaveCanvas(Store.WAVE_RES, 0, 2, QColor(32, 156, 255), False)
    self.waveRight = WaveCanvas(Store.WAVE_RES, 0, 2, QColor(32, 156, 255), False)

    layout = QVBoxLayout()
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(12)
    layout.addWidget(self.waveLeft)
    layout.addWidget(self.waveRight)
    self.setLayout(layout)
    self.setMinimumWidth(640)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)