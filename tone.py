import pyaudio
import numpy as np

class _Tone:

  p = None

  def startPyAudio(self):
    self.p = pyaudio.PyAudio()

  def play(self, data, freq=440.0, duration=1.0, volume=0.5):

    self.startPyAudio()

    fs = 44100

    samples = []
    for n in np.arange(fs * duration):
      lenData = len(data)
      index = n * freq * lenData / fs
      samples.append(np.interp(index % lenData, list(range(lenData)), data))
    samples = (np.array(samples)).astype(np.float32)

    stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    stream.write((volume * samples).tobytes())
    stream.stop_stream()
    stream.close()

  # TODO: Call when closing program.
  def endPyAudio(self):
    self.p.terminate()

Tone = _Tone()