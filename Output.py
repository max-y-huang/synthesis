from PyQt6.QtWidgets import QGroupBox, QSizePolicy, QVBoxLayout

from Widgets.WaveCanvas import WaveCanvas

class Output(QGroupBox):

  def __init__(self):
    
    super().__init__()
    self.setTitle('Output')
    self.initGUI()
  
  def initGUI(self):

    self.waveLeft = WaveCanvas(64)
    self.waveRight = WaveCanvas(64)

    layout = QVBoxLayout()
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(8)
    layout.addWidget(self.waveLeft)
    layout.addWidget(self.waveRight)
    self.setLayout(layout)
    self.setMinimumWidth(640)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)