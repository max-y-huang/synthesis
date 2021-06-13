class Store:

  WAVE_RES = 65
  EQUALIZER_RES = 7
  
  components = {}
  controllers = {}

  def getComponents(self):
    tuples = list(self.components.items())
    return list(map(lambda item: item[1], tuples))
  
  def getControllers(self):
    tuples = list(self.controllers.items())
    return list(map(lambda item: item[1], tuples))