from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QColor

from Widgets.WaveCanvas import WaveCanvas
from store import Store
from AudioPlayer import AudioPlayer
from synth import Synth

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.player = AudioPlayer()
    self.active = False
    self.setTitle('Output')
    self.initGUI()
  
  def onButtonPressed(self):

    self.active = not self.active
    if self.active:
      # self.player.add('A2')
      # self.player.add('E3')
      # self.player.add('C4')
      self.player.add('A4')
      # self.player.add('E5')
      # self.player.add('C6')
      # self.player.add('A6')
      # self.player.add('E7')
      # self.player.add('C8')
      self.player.play()
      self.playButton.setText('Stop Tone')
    else:
      self.player.clear()
      self.playButton.setText('Play Tone')
  
  def initGUI(self):

    self.canvas = WaveCanvas(Store.WAVE_RES, 0, 3, QColor(32, 156, 255), False)

    self.playButton = QPushButton('Play Tone')
    self.playButton.clicked.connect(self.onButtonPressed)
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
  
  def update(self):
    value = Synth.calculateOutput()
    self.canvas.updateValue(value)
    self.player.setData(value)