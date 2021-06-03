from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from WaveOutput import WaveOutput
from WaveInputComponent import WaveInputComponent
from WaveSplitter import WaveSplitter

class Main(App):

  wave_splitter = WaveSplitter()

  def __init__(self):
    super(Main, self).__init__()

  def update_output(self):

    total_input = [0] * 64
    for i in range(64):
      for input in self.wave_inputs:
        total_input[i] += input.input[i] * input.sign
    
    self.wave_output.update(self.wave_splitter.split(total_input, 64 // 2))

  def build(self):

    layout = BoxLayout(orientation='vertical')

    # b1 = Button()
    # b2 = Button()

    # layout2 = BoxLayout()

    # layout2.add_widget(b1)
    # layout2.add_widget(b2)

    # layout.add_widget(layout2)

    # print(b1.pos, b1.size, b1.x, b1.y)
    # print(b2.pos, b2.size, b2.x, b2.y)

    self.wave_inputs = [
      WaveInputComponent(layout, 32, 32, 420, 150, self.update_output),
      WaveInputComponent(layout, 32, 200, 420, 150, self.update_output),
    ]

    self.wave_output = WaveOutput(32, 400, 420, 100)
    layout.add_widget(self.wave_output)
    return layout

Main().run()