import math
def rotate(point, angle):
  s = math.sin(angle)
  c = math.cos(angle)
  xnew = point[0] * c - point[1] * s
  ynew = point[0] * s + point[1] * c
  return [xnew, ynew]