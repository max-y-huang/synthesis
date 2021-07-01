from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QColor

from Widgets.WaveCanvas import WaveCanvas
from store import Store
from AudioPlayer import AudioPlayer
from Piano import Piano
from synth import Synth

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.player = AudioPlayer()
    self.piano = Piano(self.onKeyboardChange)
    self.setTitle('Output')
    self.initGUI()
  
  def onKeyboardChange(self, type, pitch, intensity=0):

    if type == 'add':
      self.player.add(pitch, intensity / 128)
      self.player.play()
    
    elif type == 'remove':
      self.player.remove(pitch)
  
  def initGUI(self):

    self.canvas = WaveCanvas(Store.WAVE_RES, 0, 3, QColor(32, 156, 255), False)

    layout = QHBoxLayout()
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(12)
    layout.addWidget(self.canvas)
    self.setLayout(layout)
    self.setMinimumWidth(720)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
  
  def update(self):
    value = Synth.calculateOutput()
    self.canvas.updateValue(value)
    self.player.setData(value)