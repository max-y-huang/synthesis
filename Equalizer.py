from PyQt6.QtWidgets import QFrame, QHBoxLayout

from Widgets.Slider import Slider
from store import Store

HEIGHT = 180

class Equalizer(QFrame):

  res = Store.EQUALIZER_RES

  def __init__(self, onChange):

    super().__init__()
    self.onChange = onChange
    self.value = [ 50 ] * self.res
    self.initGUI()
    self.sliderChanged(0)
  
  def initGUI(self):

    sliderLayout = QHBoxLayout()

    self.sliders = []
    for _ in range(self.res):
      slider = Slider(self.sliderChanged, 0, 200, 100)
      self.sliders.append(slider)
      sliderLayout.addWidget(slider)
    
    self.setLayout(sliderLayout)
    self.setFixedHeight(HEIGHT)
    self.setContentsMargins(0, 8, 0, 8)
  
  def sliderChanged(self, _):
    for i in range(self.res):
      if i < len(self.sliders):
        self.value[i] = self.sliders[i].value
    self.onChange(self.value)