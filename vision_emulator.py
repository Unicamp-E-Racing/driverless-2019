import numpy as np
import cv2
import math
import tracks as track
from constants import  *
from utils import rotate
import random
import time

img = np.zeros([480,640,3])
cv2.putText(img,"VISION EMULATOR ENABLED!", (20, 240),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255))



def global_to_local(car, point):
  xn = point[0] - car[0]
  yn = point[1] - car[1]
  s = math.sin(-car[2])
  c = math.cos(-car[2])
  xnew = xn * c - yn * s
  ynew = xn * s + yn * c
  return [xnew, ynew]



def is_in_fov(point):
  if point[0] != 0:
    angle = np.arctan2(point[1], point[0])
    is_inside = False
    if abs(angle) < VIEW_HFOV/2:
      is_inside = True
    return is_inside
  else:
    return True


def dist(point1, point2):
  return np.hypot(point1[0]-point2[0], point1[1]-point2[1])



track_blue, track_yellow = track.blue, track.yellow
def run(car_pos=[0,0,0,0]):
  global track_blue, track_yellow
  viewed_blue = []
  viewed_yellow = []

  for cone in track_blue:
    local = global_to_local(car_pos, cone)
    if dist([0,0], local) < VIEW_MAX_DISTANCE:
      if is_in_fov(local):
        viewed_blue.append(local)
  for cone in track_yellow:
    local = global_to_local(car_pos, cone)
    if dist([0,0], local) < VIEW_MAX_DISTANCE:
      if is_in_fov(local):
        viewed_yellow.append(local)

  
  n_blue = len(viewed_blue)
  n_yellow = len(viewed_yellow)
  for i in range(int(DROPOUT_PERCENTAGE*n_blue)):
    viewed_blue.pop(random.randrange(len(viewed_blue)))
  for i in range(int(DROPOUT_PERCENTAGE*n_yellow)):
    viewed_yellow.pop(random.randrange(len(viewed_yellow)))

  fov_p0 = [0, VIEW_MAX_DISTANCE]
  fov_p0 = rotate(fov_p0, car_pos[2]-math.pi/2)
  fov_p1 = fov_p0
  fov_p0 = rotate(fov_p0, VIEW_HFOV/2)
  fov_p1 = rotate(fov_p1, -VIEW_HFOV/2)
  fov_p0[0] += car_pos[0]
  fov_p0[1] += car_pos[1]
  fov_p1[0] += car_pos[0]
  fov_p1[1] += car_pos[1]
  time.sleep(SOFTWARE_LATENCY)



  return [fov_p0, fov_p1],np.array(track_blue), np.array(track_yellow),np.array(viewed_blue), np.array(viewed_yellow), "", img 