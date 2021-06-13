from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QFrame, QSpacerItem, QLabel

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

    footerLayout = QHBoxLayout()
    # footerLayout.addSpacerItem(QSpacerItem(12, 0))
    footerLayout.addWidget(addControllerButton)
    footerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    self.listLayout = QHBoxLayout()
    # HScrollGroupBox comes with a layout.
    self.setSpacing(4)
    self.addLayout(self.listLayout)
    self.addLayout(footerLayout)
    self.setFixedHeight(220)
  
  def addController(self):
    c = Controller(self.onChange, formatId(self.count))
    self.controllers.append(c)
    self.listLayout.addWidget(c)
    self.listLayout.addWidget(self.getArrowImage())
    self.count += 1
  
  def update(self):
    for c in self.controllers:
      c.updateComponentSelect()
  
  def getArrowImage(self):
    pixmap = QPixmap('./assets/arrowRight.png')
    label = QLabel(self)
    label.setPixmap(pixmap)
    return label


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
    self.componentSelect.setPlaceholderText('Select Component')
    self.componentSelect.currentIndexChanged.connect(self.onIndexChange)

    self.intensity = LabelDial('Intensity', self.onIntensityChange)
    self.pan = LabelDial('Pan',self.onPanChange, -100, 100, 0)

    dialLayout = QHBoxLayout()
    dialLayout.setSpacing(8)
    dialLayout.addWidget(self.intensity)
    dialLayout.addWidget(self.pan)

    layout = QVBoxLayout()
    layout.setSpacing(8)
    layout.addWidget(self.componentSelect)
    layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
    layout.addLayout(dialLayout)
    self.setLayout(layout)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
  
  def initInStore(self):
    Store.controllers[self.id] = { 'id': self.id, 'componentId': None, 'intensity': 0, 'pan': 0 }
  
  def updateComponentSelect(self):
    
    def getComponentDisplayName(c):
      id, name = c['id'], c['name']
      return f'<{formatId(id)}> {name}'

    self.stateLocked = True

    components = Store.getComponents()
    items = list(map(getComponentDisplayName, components))
    index = self.componentSelect.currentIndex() % len(items)  # Set to last item if index = -1.

    self.componentSelect.clear()
    self.componentSelect.addItems(items)
    self.componentSelect.setCurrentIndex(index)

    self.stateLocked = False
    self.onIndexChange(index)
  
  def onIndexChange(self, index):
    if self.stateLocked:
      return
    components = Store.getComponents()
    componentId = components[index]['id']
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