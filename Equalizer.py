from PyQt6.QtWidgets import QFrame, QHBoxLayout

from Widgets.LabelSlider import LabelSlider

HEIGHT = 180

class Equalizer(QFrame):

  def __init__(self, onUpdate):

    super().__init__()
    self.value = []

    sliderLayout = QHBoxLayout()

    self.sliders = []
    for i in range(7):
      slider = LabelSlider()
      self.sliders.append(slider)
      sliderLayout.addWidget(slider)
    
    self.setLayout(sliderLayout)
    self.setFixedHeight(HEIGHT)
    self.setContentsMargins(0, 8, 0, 8)
