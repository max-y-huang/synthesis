from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QColor

from Widgets.WaveCanvas import WaveCanvas
from store import Store
from tone import Tone

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.setTitle('Output')
    self.initGUI()
  
  def initGUI(self):

    self.canvas = WaveCanvas(Store.WAVE_RES, 0, 2, QColor(32, 156, 255), False)

    self.playButton = QPushButton('Play Tone')
    self.playButton.clicked.connect(lambda: Tone.play(self.canvas.value))
    self.playButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    self.playButton.setStyleSheet(':hover { border-color: rgb(32, 156, 255); }')

    layout = QHBoxLayout()
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(12)
    layout.addWidget(self.canvas)
    layout.addWidget(self.playButton)
    self.setLayout(layout)
    self.setMinimumWidth(720)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)