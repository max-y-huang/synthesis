import pygame, pygame.midi, threading

class Piano:
  
  def __init__(self, onChange):
    pygame.init()
    pygame.midi.init()

    self.keyboard = pygame.midi.Input(pygame.midi.get_default_input_id())
    self.onChange = onChange

    thread = threading.Thread(target=self.poll, args=())
    thread.start()
  
  def end(self):
    print("exit button clicked.")
    self.keyboard.close()
    pygame.midi.quit()
    pygame.quit()
    exit()

  def poll(self):

    while True:
      if not self.keyboard.poll():
        continue

      eventList = self.keyboard.read(10)
      for ev in eventList:

        state, pitch, intensity, _ = ev[0]
        if state == 144:
          self.onChange('add', pitch, intensity)
        elif state == 128:
          self.onChange('remove', pitch)