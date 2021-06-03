from kivy.graphics import Color

def rgba(r, g, b, a):
  return Color(r / 255, g / 255, b / 255, a)

def rgb(r, g, b):
  return rgba(r, g, b, 1)