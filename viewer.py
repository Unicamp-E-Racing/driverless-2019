from fsdviewer import viewer2d
from fsdviewer.viewer2d import Point, Line, LineMiddle, Car
from constants import VIEWER_SCALE 
import math

def local_to_global(car, point):
  s = math.sin(car[2])
  c = math.cos(car[2])
  xnew = point[0] * c - point[1] * s
  ynew = point[0] * s + point[1] * c
  xn = xnew + car[0]
  yn = ynew + car[1]
  return [xn, yn]

viewer2d.init("driverless", "white")
def run(car,predicted_path, viewed_cones_blue, viewed_cones_yelow, middle_points,
        simulated_cones_blue=[],
        simulated_cones_yellow=[],
        fov_points=[]):
    points = []
    cars = []
    lines = []
    cars.append(Car(int(car[0][0]*VIEWER_SCALE),int(car[0][1]*VIEWER_SCALE),car[0][2], -car[0][3], color="black"))

    for i, path in enumerate(reversed(predicted_path)):
        if i % 20 == 0:
            x,y,rot,steer=path
            x,y = local_to_global(car[0], [x,y])
            #print("x,y", x,y)
            cars.append(Car(int(x*VIEWER_SCALE),int(y*VIEWER_SCALE),rot+car[0][2], (steer),color="lime"))

    points.append(Point("black",int(car[0][0]*VIEWER_SCALE), int(car[0][1]*VIEWER_SCALE)))
    if len(fov_points):
        points.append(Point("black",int(fov_points[0][0]*VIEWER_SCALE), int(fov_points[0][1]*VIEWER_SCALE)))
        points.append(Point("black",int(fov_points[1][0]*VIEWER_SCALE), int(fov_points[1][1]*VIEWER_SCALE)))
        lines.append(Line(0, 1, "maroon", 5))
        lines.append(Line(0, 2, "maroon", 5))



    
    for blue in simulated_cones_blue:
        points.append(Point("green", int(blue[0]*VIEWER_SCALE), int(blue[1]*VIEWER_SCALE),7))

    for yellow in simulated_cones_yellow:
        points.append(Point("orange", int(yellow[0]*VIEWER_SCALE), int(yellow[1]*VIEWER_SCALE), 7))

    for blue in viewed_cones_blue:
        blue = local_to_global(car[0], blue)
        points.append(Point("blue", int(blue[0]*VIEWER_SCALE), int(blue[1]*VIEWER_SCALE)))

    for yellow in viewed_cones_yelow:
        yellow = local_to_global(car[0], yellow)
        points.append(Point("yellow", int(yellow[0]*VIEWER_SCALE), int(yellow[1]*VIEWER_SCALE)))

    closest = True
    for mid in middle_points:
        mid = local_to_global(car[0], mid)
        color = "red"
        if closest:
            color = "magenta"
            closest = False

        points.append(Point(color, int(mid[0]*VIEWER_SCALE), int(mid[1]*VIEWER_SCALE), 7))

    viewer2d.draw(points,lines,[],cars)



if __name__ == "__main__":
    while True:
        run()
