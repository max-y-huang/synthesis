from kivy.uix.widget import Widget
from kivy.uix.button import Button
# from kivy.uix.floatlayout import FloatLayout

from WaveInput import WaveInput

class WaveInputComponent(Widget):

  def __init__(self, layout, x, y, w, h, on_update):
    super(WaveInputComponent, self).__init__()

    self.input = [0] * 64
    self.sign = +1

    self.on_update = on_update
    layout.add_widget(WaveInput(x + 100, y, w - 100, h, self.on_wave_input_update))
  
  def on_wave_input_update(self, input):
    self.input = input
    self.on_update()