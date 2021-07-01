from PyQt6.QtGui import QFontDatabase, QIcon, QScreen
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt

import sys
from threads import threads

from ComponentList import ComponentList
from ControllerList import ControllerList
from Output import Output

class Window(QWidget):

  def onComponentUpdate(self):
    self.controllerList.update()
    self.output.update()
  
  def onControllerUpdate(self):
    self.output.update()

  def __init__(self):

    super().__init__()
    self.setWindowTitle('Synthesis')
    self.setWindowIcon(QIcon('./assets/icon.png'))
    self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
    QFontDatabase.addApplicationFont('./assets/Play.ttf')
    self.initGUI()
    # Initialize program with a wave input and a controller
    self.componentList.addWaveInput()
    self.controllerList.addController()
  
  def initGUI(self):

    self.output = Output()
    self.controllerList = ControllerList(self.onControllerUpdate)
    self.controllerList.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
    self.componentList = ComponentList(self.onComponentUpdate)
    self.componentList.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    inputLayout = QHBoxLayout()
    inputLayout.setSpacing(16)
    inputLayout.addWidget(self.componentList)
    inputLayout.addWidget(self.controllerList)

    layout = QVBoxLayout()
    layout.setSpacing(16)
    layout.addLayout(inputLayout)
    layout.addWidget(self.output)
    self.setLayout(layout)

app = QApplication(sys.argv)
app.setStyleSheet(open('./assets/styles.qtcss', 'r').read())
window = Window()
window.showMaximized()
app.exec()
threads.end()
sys.exit()