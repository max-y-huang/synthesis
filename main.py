from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt

import sys
import synthesizer

from ComponentList import ComponentList
from ControllerList import ControllerList
from Output import Output

class Window(QWidget):

  def onComponentUpdate(self):
    self.controllerList.update()
    self.output.waveLeft.updateValue(synthesizer.calculateOutput())
  
  def onControllerUpdate(self):
    self.output.waveLeft.updateValue(synthesizer.calculateOutput())

  def __init__(self):

    super().__init__()
    self.setFixedSize(0, 0)  # Auto-fits
    self.setWindowTitle('Synthesis')
    self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
    QFontDatabase.addApplicationFont('./assets/Play.ttf')
    self.initGUI()
    # Initialize program with a wave input and a controller
    self.componentList.addWaveInput()
    self.controllerList.addController()
  
  def initGUI(self):

    self.output = Output()
    self.controllerList = ControllerList(self.onControllerUpdate)
    self.componentList = ComponentList(self.onComponentUpdate)

    rightLayout = QVBoxLayout()
    rightLayout.setSpacing(16)
    rightLayout.addWidget(self.controllerList)
    rightLayout.addWidget(self.output)
    rightLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    layout = QHBoxLayout()
    layout.setSpacing(16)
    layout.addWidget(self.componentList)
    layout.addLayout(rightLayout)
    self.setLayout(layout)

app = QApplication(sys.argv)
app.setStyleSheet(open('./assets/styles.qtcss', 'r').read())
window = Window()
window.show()
sys.exit(app.exec())