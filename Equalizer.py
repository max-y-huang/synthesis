from PyQt6.QtWidgets import QFrame, QHBoxLayout

from Widgets.Slider import Slider

HEIGHT = 180

class Equalizer(QFrame):

  numSliders = 7

  def __init__(self, onChange):

    super().__init__()
    self.onChange = onChange
    self.value = [ 50 ] * self.numSliders
    self.initGUI()
  
  def initGUI(self):

    sliderLayout = QHBoxLayout()

    self.sliders = []
    for _ in range(self.numSliders):
      slider = Slider(self.sliderChanged)
      self.sliders.append(slider)
      sliderLayout.addWidget(slider)
    
    self.setLayout(sliderLayout)
    self.setFixedHeight(HEIGHT)
    self.setContentsMargins(0, 8, 0, 8)
  
  def sliderChanged(self, _):
    for i in range(self.numSliders):
      if i < len(self.sliders):
        self.value[i] = self.sliders[i].value
    self.onChange(self.value)