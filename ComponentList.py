from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QSpacerItem, QFrame, QLabel

from Widgets.ScrollGroupBox import VScrollGroupBox
from Widgets.EditableLabel import EditableLabel
from WaveInput import WaveInput
from Equalizer import Equalizer
from funcs import formatId
from store import Store

class ComponentList(VScrollGroupBox):

  count = 0

  def __init__(self, onUpdate):

    super().__init__('Components')
    self.onUpdate = onUpdate
    self.components = []
    self.initGUI()
  
  def initGUI(self):

    addWaveInputButton = QPushButton('Add Wave')
    addWaveInputButton.clicked.connect(self.addWaveInput)
    addWaveInputButton.setStyleSheet('padding: 16 24')
    addEqualizerButton = QPushButton('Add EQ')
    addEqualizerButton.clicked.connect(self.addEqualizer)
    addEqualizerButton.setStyleSheet('padding: 16 24')

    footerOptionsLayout = QHBoxLayout()
    footerOptionsLayout.addWidget(addWaveInputButton)
    footerOptionsLayout.addWidget(addEqualizerButton)

    footerLayout = QVBoxLayout()
    footerLayout.addSpacerItem(QSpacerItem(0, 8))
    footerLayout.addLayout(footerOptionsLayout)
    footerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    self.listLayout = QVBoxLayout()
    # VScrollGroupBox comes with a layout.
    self.setSpacing(8)
    self.addLayout(self.listLayout)
    self.addLayout(footerLayout)
    self.setFixedWidth(480)

  def addWaveInput(self):
    c = Component(WaveInput, self.onUpdate, self.count, 'New Wave')
    self.components.append(c)
    self.listLayout.addWidget(c)
    self.count += 1
  
  def addEqualizer(self):
    c = Component(Equalizer, self.onUpdate, self.count, 'New EQ')
    self.components.append(c)
    self.listLayout.addWidget(c)
    self.count += 1


class Component(QFrame):

  def onValueUpdate(self, input):
    Store.components[self.id]['value'] = input
    self.onUpdate()
  
  def onNameUpdate(self, name):
    Store.components[self.id]['name'] = name
    self.onUpdate()

  def __init__(self, component, onUpdate, id, name='Component'):

    super().__init__()
    self.id = id
    self.name = name
    self.onUpdate = onUpdate
    self.initGUI(component)
    self.initInStore(name, self.inputWidget.value)
  
  def initGUI(self, component):
    idWidget = QLabel(formatId(self.id))
    idWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    nameWidget = EditableLabel(self.onNameUpdate, self.name)
    nameWidget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    self.inputWidget = component(self.onValueUpdate)

    labelLayout = QHBoxLayout()
    labelLayout.addWidget(idWidget)
    labelLayout.addWidget(nameWidget)

    layout = QVBoxLayout()
    layout.addLayout(labelLayout)
    layout.addWidget(self.inputWidget)
    self.setLayout(layout)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
  
  def initInStore(self, name, value):
    Store.components.append({ 'id': self.id })
    self.onNameUpdate(name)
    self.onValueUpdate(value)