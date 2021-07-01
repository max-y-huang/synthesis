import threading

class Threads:

  def __init__(self):
    self.threads = []
    self.endThreads = False

  def add(self, func, args):
    self.threads.append(threading.Thread(target=func, args=args))
    self.threads[-1].start()

  def ended(self):
    return self.endThreads

  def end(self):
    self.endThreads = True

threads = Threads()