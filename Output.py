from PyQt6.QtWidgets import QGroupBox, QPushButton, QSizePolicy, QVBoxLayout
from PyQt6.QtGui import QColor

from Widgets.WaveCanvas import WaveCanvas
from store import Store
from tone import playTone

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.setTitle('Output')
    self.initGUI()
  
  def initGUI(self):

    self.waveLeft = WaveCanvas(Store.WAVE_RES, 0, 2, QColor(32, 156, 255), False)
    self.waveRight = WaveCanvas(Store.WAVE_RES, 0, 2, QColor(32, 156, 255), False)

    self.playButton = QPushButton('Play Tone')
    self.playButton.clicked.connect(lambda: playTone(self.waveLeft.value))
    self.playButton.setStyleSheet(':hover { border-color: rgb(32, 156, 255); }')

    layout = QVBoxLayout()
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(12)
    layout.addWidget(self.waveLeft)
    layout.addWidget(self.waveRight)
    layout.addWidget(self.playButton)
    self.setLayout(layout)
    self.setMinimumWidth(720)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)