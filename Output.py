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

    self.waveLeft = WaveCanvas(Store.WAVE_INPUT_RES, 0, QColor(32, 156, 255), False)
    self.waveRight = WaveCanvas(Store.WAVE_INPUT_RES, 0, QColor(32, 156, 255), False)

    layout = QVBoxLayout()
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(8)
    layout.addWidget(self.waveLeft)
    layout.addWidget(self.waveRight)
    self.setLayout(layout)
    self.setMinimumWidth(640)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)