from time import time
import numpy as np
from constants import STEER_MAX, STEER_MIN, DEFAULT_ANGLE, HALF_CAR_WIDTH, FRONT_DISTANCE
from math import atan2, degrees, hypot


######## General functions ########
def angle_to_point(point):
    angle = -degrees(atan2(point[1],point[0]))
    return angle 

def sort_cones(cones):
    dists = np.sqrt(np.sum(np.square(cones), axis=1))
    sorted_indexes = dists.argsort()
    return cones[sorted_indexes[::]] # sort cones based on dist 

def normalize_angle(angle):
    # normalize over 90 degree angles
    angle = min(STEER_MAX, angle)
    angle = max(STEER_MIN, angle)
    return angle


######## One Cone ########
def gonna_hit(cone):
    x,y = cone
    if y < FRONT_DISTANCE:
        return (x > - HALF_CAR_WIDTH or x < HALF_CAR_WIDTH)
    else:
        return False

def one_cone(blue, yellow):
    # TODO:  calculate mid to return to viewer
    blue_size = blue.shape[0]
    yellow_size = yellow.shape[0]

    if blue_size > yellow_size: # one blue cone
        if gonna_hit(blue[0]):
            return STEER_MIN, [] # steer away
        else:
            return DEFAULT_ANGLE, []
    
    else: # one yellow cone
        if gonna_hit(yellow[0]):
            return STEER_MAX , []# steer away
        else:
            return DEFAULT_ANGLE, []


######## One side ########
def one_side(blue, yellow):
    if blue.shape[0] > yellow.shape[0]: # only blue
        cones = sort_cones(blue)[:2] # get closest to car
    else: # only yellow
        cones = sort_cones(yellow)[:2] # get closest to car

    (x1,y1), (x2,y2) = cones
    dist_x = hypot(x2, x1)
    dist_y = hypot(y2, y1)
    angle = angle_to_point([dist_x, dist_y])
    if angle > 0:
        angle = STEER_MAX
    else:
        angle = STEER_MIN
    return angle, [[dist_x,dist_y]] # steer in the angle of the two cones

######## One on one side ########
def one_on_one_side(blue, yellow):
    if blue.shape[0] > yellow.shape[0]:
        blue = sort_cones(blue)[:1] # get closest to car
    else:
        yellow = sort_cones(yellow)[:1] # get closest to car
    mid = (blue + yellow) / 2
    return angle_to_point(mid[0]), mid # steer to mid


######## One on each side ########
def one_on_each_side(blue, yellow):
    mid = (blue + yellow) / 2
    return angle_to_point(mid[0]), mid # steer to mid


######## All cones ########
def lots_of_cones(blue, yellow):
    main_blue = sort_cones(blue)[:2]
    main_yellow = sort_cones(yellow)[:2]
    all_cones = np.concatenate((main_blue,main_yellow))
    mid = np.average(all_cones, axis=0)
    return angle_to_point(mid), [mid] # steer to mid


''' 
Parameters:
    blue - np.array( [ [x1,y1], [x2,y2], ... ] )
    yellow - np.array( [ [x1,y1], [x2,y2], ... ] )
'''
def run(blue, yellow):
    time_start = time()
    blue_size = blue.shape[0]
    yellow_size = yellow.shape[0]
    total_size = blue_size + yellow_size
    print_info = f"Controller:\n    Input:\n        Blue size: {blue_size:>5}\n        Yellow size: {yellow_size:>3}\n    "

    if total_size == 0: # no cones
        print_info += "Control Mode: no cones"
        angle = DEFAULT_ANGLE
        mid = []

    elif total_size == 1: # one cone
        angle, mid = one_cone(blue, yellow)
        print_info += "Control Mode: one cone{'' if angle == DEFAULT_ANGLE else ' - gonna hit'}"

    elif blue_size == 0 or yellow_size == 0: # cones on only one side
        print_info += "Control Mode: one side only"
        angle, mid = one_side(blue, yellow)
    
    elif blue_size == 1 and yellow_size == 1:
        print_info += "Control Mode: one on each side"
        angle, mid = one_on_each_side(blue, yellow)

    elif blue_size == 1 or yellow_size == 1:
        print_info += "Control Mode: lots on one side and one on the other"
        angle, mid = one_on_one_side(blue, yellow)

    else: # one or more cones on both sides
        print_info += "Control Mode: lots of cones"
        angle, mid = lots_of_cones(blue, yellow)

    # print("Angle before normalization", angle)
    print_info += f"\n    Angle before normalization: {angle:>5.2f}\n"
    angle = normalize_angle(angle)
    print_info += f"    Angle after normalization: {angle:>6.2f}\n    Time: {(time() - time_start)*1000:>5.0f} ms \n"
    return angle, mid, print_info








if __name__ == "__main__":
    def test(blue, yellow, expected, test_name):
        result = run(blue,yellow)
        print(f"{test_name} : \nresult: {result} Expected {expected}")
        print("Succeed test" if result == expected else "\n\nFailed test\n\n")
        print()

    ### No cone test
    expected = 0.0
    yel = np.array( [] )
    blue = np.array( [] )
    test(blue, yel, expected=0.0, test_name="no cone")


    ### One code tests
    # blue
    yel = np.array( [] )
    blue = np.array( [ [1,1] ] )
    test(blue, yel, expected=STEER_MAX, test_name="one cone : blue")

    # yellow
    yel = np.array( [ [1,1] ] )
    blue = np.array( [] )
    test(blue, yel, expected=STEER_MIN, test_name="one cone : yellow")


    ### One side tests
    # blue
    yel = np.array( [] )
    blue = np.array( [ [2,1], [1,1] ] )
    test(blue, yel, expected=STEER_MAX, test_name="one side : blue")

    # yellow
    yel = np.array( [ [2,1], [1,1] ] )
    blue = np.array( [] )
    test(blue, yel, expected=STEER_MIN, test_name="one side : yellow")


    ### Only one cone on one side tests
    # blue
    yel = np.array( [[-1, 1]] )
    blue = np.array( [ [2,1], [1,1] ] )
    test(blue, yel, expected=0.0, test_name="only one cone on one side : blue")

    # yellow
    yel = np.array( [ [2,1], [1,1] ] )
    blue = np.array( [[-1, 1]] )
    test(blue, yel, expected=-0.0, test_name="only one cone on one side : yellow")


    ### Only one cone on one side tests
    # blue
    yel = np.array( [[-1, 1]] )
    blue = np.array( [ [2,1], [1,1] ] )
    test(blue, yel, expected=0.0, test_name="only one cone on one side : blue")

    # yellow
    yel = np.array( [ [2,1], [1,1] ] )
    blue = np.array( [[-1, 1]] )
    test(blue, yel, expected=-0.0, test_name="only one cone on one side : yellow")


    ### One cone on each side tests
    # blue
    yel = np.array( [[-1, 1]] )
    blue = np.array( [ [1,1] ] )
    test(blue, yel, expected=0.0, test_name="one cone on each side : blue")

    # yellow
    yel = np.array( [ [1,1] ] )
    blue = np.array( [ [-1, 1] ] )
    test(blue, yel, expected=-0.0, test_name="one cone on each side : yellow")


    ### Lots of cones tests
    # blue
    yel = np.array( [ [2,1], [1,1] ] )
    blue = np.array( [ [-2,1], [-1,1] ] )
    test(blue, yel, expected=0.0, test_name="lots of cones : blue")

    # yellow
    yel = np.array( [ [2,1], [1,1] ] )
    blue = np.array( [ [-2,1], [-1,1] ] )
    test(blue, yel, expected=-0.0, test_name="lots of cones : yellow")
