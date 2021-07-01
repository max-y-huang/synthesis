import pyaudio, time, threading, atexit, re, numpy as np

class AudioPlayer:

  fs = 16000
  # fs = 22050
  # fs = 44100
  updateRate = 1/10

  def __init__(self):
    atexit.register(self.exit)
    self.p = pyaudio.PyAudio()
    self.wavePlaybackPos = 0
    self.notes = []
    self.data = []
    
    thread = threading.Thread(target=self.startStream, args=())
    thread.start()
  
  def exit(self):
    self.clear()
    self.p.terminate()
  
  def getPitch(self, note):

    noteVals = { 'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11 }
    split = re.search('[0-9]', note).start()
    noteNum = noteVals[note[0:split]]
    octave = int(note[split:])

    return octave * 12 + noteNum
  
  def getFreq(self, pitch):
    offset = pitch - 57  # A4 = 57
    return 440.0 * (2 ** (1/12.0)) ** offset
  
  def add(self, pitch, volume=0.5):
    # pitch = self.getPitch(note)
    self.remove(pitch)
    self.notes.append({ 'pitch': pitch, 'volume': volume })
  
  def remove(self, pitch):
    # pitch = self.getPitch(note)
    self.notes = list(filter(lambda item: item['pitch'] != pitch, self.notes))
  
  def clear(self):
    self.notes.clear()
  
  def setData(self, data):
    self.data = data
  
  def startStream(self):

    def getDataByFrame(n):

      def getWaveDataByFrame(n, freq, volume):

        lenData = len(self.data)
        rangeData = list(range(lenData))

        index = n * lenData * freq / self.fs
        return np.interp(index % lenData, rangeData, self.data) * volume / 5   # Dividing by a constant to lower the peak from stacking multiple notes.
      
      ret = 0
      for note in self.notes:
        ret += getWaveDataByFrame(n, self.getFreq(note['pitch']), note['volume'])
      return ret

    def streamCallback(in_data, frame_count, time_info, status):

      samples = np.array([ getDataByFrame(self.wavePlaybackPos + i) for i in range(frame_count) ])
      self.wavePlaybackPos += frame_count
      return (
        samples.astype(np.float32).tobytes(),
        pyaudio.paContinue
      )

    stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.fs, output=True, stream_callback=streamCallback)
    stream.start_stream()
    while True:
      time.sleep(self.updateRate)