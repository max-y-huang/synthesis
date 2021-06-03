import numpy, math

class WaveSplitter:

  def split(self, input, samples):

    N = len(input)
    samples = min(samples, N)
    fft = numpy.fft.fft(input)[0:samples]

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