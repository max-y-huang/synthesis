import pyaudio
import time
import threading
import atexit
import numpy as np

class AudioPlayer:

  fs = 44100
  updateRate = 1/100

  def __init__(self):
    atexit.register(self.exit)
    self.p = pyaudio.PyAudio()
    self.queue = []
    self.playing = False
    self.data = [0]
  
  def exit(self):
    self.p.terminate()
  
  def queueIsEmpty(self):
    return len(self.queue) == 0
  
  def queueNote(self, note, volume=0.5):
    self.dequeueNote(note)
    self.queue.append({ 'note': note, 'volume': volume })
    if not self.playing:
      self.playing = True
      self.play()
  
  def dequeueNote(self, note):
    self.queue = list(filter(lambda item: item['note'] != note, self.queue))
    if self.queueIsEmpty():
      self.playing = False
  
  def setData(self, data):
    self.data = data
  
  def play(self, freq=440.0, volume=0.5):

    # Helper variables for dataFunc.
    lenData = len(self.data)
    rangeData = list(range(lenData))

    def dataFunc(n):
      index = n * lenData * freq / self.fs
      return np.interp(index % lenData, rangeData, self.data) * volume

    def getData(in_data, frame_count, time_info, status):
      samples = np.array([ dataFunc(self.wavePlaybackPos + i) for i in range(frame_count) ])
      self.wavePlaybackPos += frame_count
      return (
        samples.astype(np.float32).tobytes(),
        pyaudio.paComplete if self.queueIsEmpty() else pyaudio.paContinue
      )
    
    def handleStream():
      self.wavePlaybackPos = 0
      stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.fs, output=True, stream_callback=getData)
      stream.start_stream()
      while stream.is_active():
        time.sleep(self.updateRate)
      stream.stop_stream()
      stream.close()
    
    thread = threading.Thread(target=handleStream, args=())
    thread.start()