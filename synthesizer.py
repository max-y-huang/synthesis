import numpy, math

from store import Store

def calculateOutput():

  processFuncs = {
    'wave input': processWaveInput,
    'equalizer': processEqualizer
  }

  data = [0] * Store.WAVE_OUTPUT_RES
  for controller in Store.controllers:
    componentId = controller['componentId']
    if componentId == -1:
      continue
    component = Store.components[componentId]
    data = processFuncs[component['type']](data, component['value'], controller['intensity'], controller['pan'])
  
  waves = getWaves(convertRes(data, Store.WAVE_INPUT_RES))
  data = dataFromWaves(waves, Store.WAVE_INPUT_RES, Store.WAVE_OUTPUT_RES)
  return scaleDataToRange(data, [-1, 1])

def processWaveInput(data, input, intensity, pan):

  input = convertRes(input, Store.WAVE_OUTPUT_RES)
  for i in range(len(data)):
    if i < len(input):
      data[i] += input[i] * intensity / 100

  return data

def processEqualizer(data, input, intensity, pan):

  inputRes = Store.WAVE_INPUT_RES
  outputRes = Store.WAVE_OUTPUT_RES
  eqRes = Store.EQUALIZER_RES

  waves = getWaves(convertRes(data, inputRes))
  for i in range(len(waves)):
    sliderNum = math.floor(i * eqRes / inputRes)
    waves[i]['amp'] *= input[sliderNum] / 100 * intensity / 100
  data = dataFromWaves(waves, inputRes, outputRes)

  return data

def convertRes(data, outputRes):

  inputRes = len(data)
  interpIn = list(range(inputRes))
  interpOut = data
  ret = [0] * outputRes

  for i, j in enumerate(numpy.linspace(0, inputRes - 1, outputRes)):
    ret[i] = numpy.interp(j, interpIn, interpOut)
  
  return ret

def scaleDataToRange(data, range):
  dataMin, dataMax = min(data), max(data)
  return numpy.interp(data, [dataMin, dataMax], [0, 0] if dataMin == dataMax else range)

def dataFromWaves(waves, inputRes, outputRes):

  ret = [0] * outputRes
  for i in range(outputRes):
    for w in waves:
      ret[i] += w['amp'] * math.cos(w['speed'] * (i * inputRes / outputRes) + w['offset'])
  
  return ret

def getWaves(data, samples=Store.WAVE_INPUT_RES // 2):

  N = len(data)
  samples = min(samples, N)
  fft = numpy.fft.fft(data)[0:samples]

  waves = []
  for k, c in enumerate(fft):
    speed = 2 * math.pi * k / N
    waves.append({
      'amp': 1 / N * c.real,
      'speed': speed,
      'offset': 0
    })
    waves.append({
      'amp': -1 / N * c.imag,
      'speed': speed,
      'offset': -math.pi / 2
    })
  
  return waves