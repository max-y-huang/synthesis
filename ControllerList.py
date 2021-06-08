from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QFrame, QSpacerItem

from Widgets.Dial import LabelDial
from Widgets.ScrollGroupBox import HScrollGroupBox
from funcs import formatId
from store import Store

# CONTROLLER_HEIGHT = 150

class ControllerList(HScrollGroupBox):

  count = 0

  def __init__(self):
    
    super().__init__('Controllers')
    self.controllers = []
    self.initGUI()
  
  def initGUI(self):

    addControllerButton = QPushButton('Add Controller')
    addControllerButton.clicked.connect(self.addController)
    addControllerButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    addControllerButton.setStyleSheet('padding: 16 24')

    footerLayout = QHBoxLayout()
    footerLayout.addSpacerItem(QSpacerItem(8, 0))
    footerLayout.addWidget(addControllerButton)
    footerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    self.listLayout = QHBoxLayout()
    # HScrollGroupBox comes with a layout.
    self.setSpacing(8)
    self.addLayout(self.listLayout)
    self.addLayout(footerLayout)
  
  def addController(self):
    c = Controller()
    self.controllers.append(c)
    self.listLayout.addWidget(c)
    self.count += 1
  
  def update(self):
    for c in self.controllers:
      c.updateComponentSelect()


class Controller(QFrame):

  def __init__(self):

    super().__init__()
    self.initGUI()
  
  def initGUI(self):

    self.componentSelect = QComboBox()
    self.updateComponentSelect()

    self.intensity = LabelDial('Intensity')
    self.pan = LabelDial('Pan', -100, 100, 0)

    dialLayout = QHBoxLayout()
    dialLayout.setSpacing(8)
    dialLayout.addWidget(self.intensity)
    dialLayout.addWidget(self.pan)

    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.addWidget(self.componentSelect)
    layout.addLayout(dialLayout)
    self.setLayout(layout)
    # self.setFixedHeight(CONTROLLER_HEIGHT)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
  
  def updateComponentSelect(self):
    
    def getComponentDisplayName(c):
      id, name = c['id'], c['name']
      return f'<{formatId(id)}> {name}'

    self.componentSelect.clear()
    self.componentSelect.addItems(list(map(getComponentDisplayName, Store.components)))