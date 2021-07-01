import pygame, pygame.midi
from threads import threads

class Piano:
  
  def __init__(self, onChange):
    pygame.init()
    pygame.midi.init()
    self.keyboard = pygame.midi.Input(pygame.midi.get_default_input_id())
    self.onChange = onChange
    threads.add(self.poll, ())
  
  def onExit(self):
    self.keyboard.close()
    pygame.midi.quit()
    pygame.quit()

  def poll(self):

    while not threads.ended():

      if not self.keyboard.poll():
        continue

      eventList = self.keyboard.read(10)
      for ev in eventList:

        state, pitch, intensity, _ = ev[0]
        if state == 144:
          self.onChange('add', pitch, intensity)
        elif state == 128:
          self.onChange('remove', pitch)

    self.onExit()