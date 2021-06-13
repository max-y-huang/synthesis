from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QSpacerItem, QFrame, QLabel

from Widgets.ScrollGroupBox import VScrollGroupBox
from Widgets.EditableLabel import EditableLabel
from WaveInput import WaveInput
from Equalizer import Equalizer
from funcs import formatId
from store import Store

class ComponentList(VScrollGroupBox):

  count = 0

  def __init__(self, onChange):

    super().__init__('Components')
    self.onChange = onChange
    self.components = []
    self.initGUI()
  
  def initGUI(self):

    addWaveInputButton = QPushButton('Add Wave')
    addWaveInputButton.clicked.connect(self.addWaveInput)
    addEqualizerButton = QPushButton('Add EQ')
    addEqualizerButton.clicked.connect(self.addEqualizer)

    footerOptionsLayout = QHBoxLayout()
    footerOptionsLayout.addWidget(addWaveInputButton)
    footerOptionsLayout.addWidget(addEqualizerButton)

    footerLayout = QVBoxLayout()
    footerLayout.addSpacerItem(QSpacerItem(0, 8))
    footerLayout.addLayout(footerOptionsLayout)
    footerLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    self.listLayout = QVBoxLayout()
    # VScrollGroupBox comes with a layout.
    self.setSpacing(12)
    self.addLayout(self.listLayout)
    self.addLayout(footerLayout)
    self.setFixedWidth(480)

  def addWaveInput(self):
    c = Component('wave input', self.onChange, formatId(self.count), 'New Wave')
    self.components.append(c)
    self.listLayout.addWidget(c)
    self.count += 1
  
  def addEqualizer(self):
    c = Component('equalizer', self.onChange, formatId(self.count), 'New EQ')
    self.components.append(c)
    self.listLayout.addWidget(c)
    self.count += 1


class Component(QFrame):

  def __init__(self, type, onChange, id, name='Component'):

    super().__init__()
    self.type = type
    self.id = id
    self.name = name
    self.onChange = onChange
    self.initInStore()
    self.initGUI()
    self.onNameChange(name)
    self.onValueChange(self.inputWidget.value)
  
  def initGUI(self):
    inputWidgetComponent = { 'wave input': WaveInput, 'equalizer': Equalizer }

    idWidget = QLabel(self.id)
    idWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    nameWidget = EditableLabel(self.onNameChange, 'text', self.name)
    nameWidget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

    self.inputWidget = inputWidgetComponent[self.type](self.onValueChange)

    labelLayout = QHBoxLayout()
    labelLayout.addWidget(idWidget)
    labelLayout.addWidget(nameWidget)

    layout = QVBoxLayout()
    layout.addLayout(labelLayout)
    layout.addWidget(self.inputWidget)
    self.setLayout(layout)
    self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
  
  def initInStore(self):
    Store.components[self.id] = { 'id': self.id, 'type': self.type, 'name': '', 'value': [] }

  def onValueChange(self, input):
    Store.components[self.id]['value'] = input
    self.onChange()
  
  def onNameChange(self, name):
    Store.components[self.id]['name'] = name
    self.onChange()