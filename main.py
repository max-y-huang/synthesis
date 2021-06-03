from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

import math

from WaveInput import WaveInput

class Main(App):

  def build(self):

    self.wave_input = WaveInput(32, 32, 420, 300)
    # self.wave_input2 = WaveInput(Window.width // 2 + 16, 32, Window.width // 2 - 48, 400)

    layout = FloatLayout()
    layout.add_widget(self.wave_input)
    # layout.add_widget(self.wave_input2)
    return layout

Main().run()