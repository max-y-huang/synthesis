from PyQt6.QtWidgets import QComboBox, QHBoxLayout,  QPushButton, QSizePolicy, QVBoxLayout, QFrame, QSpacerItem

from Widgets.Dial import LabelDial
from Widgets.ScrollGroupBox import HScrollGroupBox
from funcs import formatId
from store import Store

class ControllerList(HScrollGroupBox):

  count = 0

  def __init__(self, onChange):
    
    super().__init__('Controllers')
    self.onChange = onChange
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
    c = Controller(self.onChange, self.count)
    self.controllers.append(c)
    self.listLayout.addWidget(c)
    self.count += 1
  
  def update(self):
    for c in self.controllers:
      c.updateComponentSelect()


class Controller(QFrame):

  def __init__(self, onChange, id):

    super().__init__()
    self.stateLocked = False
    self.id = id
    self.onChange = onChange
    self.initInStore()
    self.initGUI()
    self.updateComponentSelect()  # Automatically runs onComponentChange.
    self.onIntensityChange(self.intensity.getValue())
    self.onPanChange(self.pan.getValue())
  
  def initGUI(self):

    self.componentSelect = QComboBox()
    self.componentSelect.currentIndexChanged.connect(self.onComponentChange)

    self.intensity = LabelDial('Intensity', self.onIntensityChange)
    self.pan = LabelDial('Pan',self.onPanChange, -100, 100, 0)

    dialLayout = QHBoxLayout()
    dialLayout.setSpacing(8)
    dialLayout.addWidget(self.intensity)
    dialLayout.addWidget(self.pan)

    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.addWidget(self.componentSelect)
    layout.addLayout(dialLayout)
    self.setLayout(layout)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
  
  def initInStore(self):
    Store.controllers.append({ 'id': self.id, 'componentId': -1, 'intensity': 0, 'pan': 0 })
  
  def updateComponentSelect(self):
    
    def getComponentDisplayName(c):
      id, name = c['id'], c['name']
      return f'<{formatId(id)}> {name}'

    self.stateLocked = True

    items = list(map(getComponentDisplayName, Store.components))
    value = self.componentSelect.currentIndex()
    if value == -1:
      value = len(items) - 1

    self.componentSelect.clear()
    self.componentSelect.addItems(items)
    self.componentSelect.setCurrentIndex(value)

    self.stateLocked = False
    self.onComponentChange(self.componentSelect.currentIndex())
  
  def onComponentChange(self, componentId):
    if self.stateLocked:
      return
    Store.controllers[self.id]['componentId'] = componentId
    self.onChange()
  
  def onIntensityChange(self, intensity):
    if self.stateLocked:
      return
    Store.controllers[self.id]['intensity'] = intensity
    self.onChange()
  
  def onPanChange(self, pan):
    if self.stateLocked:
      return
    Store.controllers[self.id]['pan'] = pan
    self.onChange()