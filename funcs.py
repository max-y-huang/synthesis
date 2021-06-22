import numpy as np

def clamp(val, low, high):
  return max(min(val, high), low)

def formatId(id):
  return '' + str(id).zfill(3)

def scaleWaveDataToRange(data, range):
    dataMin, dataMax = min(data), max(data)
    return np.interp(data, [dataMin, dataMax], [0, 0] if dataMin == dataMax else range)