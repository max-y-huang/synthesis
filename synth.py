import numpy as np, math

from store import Store
from funcs import scaleWaveDataToRange

class _Synth:

  def calculateOutput(self):

    processFuncs = {
      'wave input': self.processWaveInput,
      'equalizer': self.processEqualizer
    }

    data = self.getEmptyData()
    for controller in Store.getControllers():
      componentId = controller['componentId']
      if componentId == None:
        continue
      component = Store.components[componentId]
      # TODO: Take into account missing component.
      data = processFuncs[component['type']](data, component['value'], controller['intensity'], controller['pan'])
    
    waves = self.getWaves(data)
    data = self.dataFromWaves(waves)
    data = scaleWaveDataToRange(data, [-1, 1])
    return data

  def getEmptyData(self, res=Store.WAVE_RES):
    return [0] * res

  def processWaveInput(self, data, input, intensity, pan):

    for i in range(len(data)):
      if i < len(input):
        data[i] += input[i] * intensity / 100

    return data

  def processEqualizer(self, data, input, intensity, pan):

    sliderWaveRatio = Store.EQUALIZER_RES / Store.WAVE_RES

    waves = self.getWaves(data)
    for i in range(len(waves)):
      sliderNum = math.floor(i / 2 * sliderWaveRatio)
      waves[i]['amp'] *= input[sliderNum] / 100

    return self.dataFromWaves(waves)

  def dataFromWaves(self, waves, res=Store.WAVE_RES):

    ret = [0] * res
    for i in range(res):
      for w in waves:
        ret[i] += w['amp'] * np.cos(w['speed'] * i + w['offset'])
    
    return ret

  def getWaves(self, data, samples=Store.WAVE_RES):

    N = len(data)
    samples = min(samples, N)
    fft = np.fft.fft(data)[0:samples]

    waves = []
    for k, c in enumerate(fft):
      speed = 2 * np.pi * k / N
      waves.append({
        'amp': 1 / N * c.real,
        'speed': speed,
        'offset': 0
      })
      waves.append({
        'amp': -1 / N * c.imag,
        'speed': speed,
        'offset': -np.pi / 2
      })
    
    return waves
  
Synth = _Synth()