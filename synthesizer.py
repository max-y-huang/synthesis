import numpy, math

from store import Store

def getData():

  totalInput = [0] * Store.WAVE_INPUT_RES
  for c in Store.components:
    if c['type'] != 'wave input':
      continue
    if 'value' in c:
      for i, val in enumerate(c['value']):
        totalInput[i] += val
  
  return totalInput

def getWaves(data, samples):

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