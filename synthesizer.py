import numpy as np, math

from store import Store

def playData(self, data):
  pass

def calculateOutput():

  processFuncs = {
    'wave input': processWaveInput,
    'equalizer': processEqualizer
  }

  data = getEmptyData()
  for controller in Store.getControllers(Store):
    componentId = controller['componentId']
    if componentId == None:
      continue
    component = Store.components[componentId]
    # TODO: Take into account missing component.
    data = processFuncs[component['type']](data, component['value'], controller['intensity'], controller['pan'])
  
  waves = getWaves(data)
  data = dataFromWaves(waves)
  data = scaleDataToRange(data, [-1, 1])
  return data

def getEmptyData(res=Store.WAVE_RES):
  return [0] * res

def processWaveInput(data, input, intensity, pan):

  for i in range(len(data)):
    if i < len(input):
      data[i] += input[i] * intensity / 100

  return data

def processEqualizer(data, input, intensity, pan):

  sliderWaveRatio = Store.EQUALIZER_RES / Store.WAVE_RES

  waves = getWaves(data)
  for i in range(len(waves)):
    sliderNum = math.floor(i / 2 * sliderWaveRatio)
    waves[i]['amp'] *= input[sliderNum] / 100

  return dataFromWaves(waves)

def scaleDataToRange(data, range):
  dataMin, dataMax = min(data), max(data)
  return np.interp(data, [dataMin, dataMax], [0, 0] if dataMin == dataMax else range)

def dataFromWaves(waves, res=Store.WAVE_RES):

  ret = [0] * res
  for i in range(res):
    for w in waves:
      ret[i] += w['amp'] * np.cos(w['speed'] * i + w['offset'])
  
  return ret

def getWaves(data, samples=Store.WAVE_RES):

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