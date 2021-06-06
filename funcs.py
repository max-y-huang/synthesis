def clamp(val, low, high):
  return max(min(val, high), low)

def formatId(id):
  return '' + str(id).zfill(3)