import math
import numpy as np
# GENERAL CONFIG
SHOW_IMG = False  # show opencv window with camera img and detected cones
SHOW_VIEWER = True  # show window with top down view detected cones and controller
# options: CAR_SIMULATION, VISION_SIMULATION. CAN_READ
RUN_FLAGS = ["CAN_READ", "CAR_SIMULATION", "VISION_SIMULATION"]
#RUN_FLAGS = []

# Camera settings
CAPTURE_MODE = "ZED_SDK"  # ZED_SDK or OPENCV
FLIP_IMG = False  # set to true if camera is mounted upside down
# for full hd image zed camera
PIXEL_SIZE = 0.002  # pixel size in mm
FOCAL = 1400*PIXEL_SIZE  # focal distance in mm
X_OFFSET = 0.00  # offset of camera from center of the car in mm
U_OFFSET = 1920/2  # image center offset in px
V_OFFSET = 1080/2  # image center offset in px
# for pseye
PIXEL_SIZE = 0.006
FOCAL = 3.2
X_OFFSET = 0.0
U_OFFSET = 640/2
V_OFFSET = 480/2

# if CAPTURE_MODE = "OPENCV"
OPENCV_CAMERA_INDEX = 0  # camera index for opencv
OPENCV_CAMERA_WIDTH = 1280 * 2
OPENCV_CAMERA_HEIGHT = 720
OPENCV_FRAME_WIDTH_CUT = 1280

# detection settings
DETECTION_MODE = "YOLO"  # YOLO or NONE

# Mesurment Settings
MESURMENT_MODE = "STEREO"  # STEREO or MONO
CONE_HEIGHT = 230  # cone real heigth in mm for monocular distance estiamtion
MAX_DISTANCE = 8  # max detection distance in m
MIN_DISTANCE = 0  # min detection distance in m
MIN_RATIO = 0  # min box w,h ratio
MAX_RATIO = 10  # max box w,h ratio

# Change this number to change yolo
# 0 - YOLO only FSOCO (last training)
# 1 - full yolo
# 2 - yolo tiny
YOLO_VERSION = 0

# YOLO files
DETECTION_THRESHOLD = 0.3
YOLO_PATH_CONFIG = ["yolo/fsoco/cone-yolov3-tiny.cfg",     "yolo/old/yolov3.cfg",
                    "yolo/old/yolov3-tiny-cone.cfg", "yolo/yolo-v4/cone-tiny.cfg"]
YOLO_PATH_WEIGHTS = ["yolo/fsoco/cone-yolov3-tiny.weights", "yolo/old/yolov3.weights",
                     "yolo/old/yolov3-tiny.weights", "yolo/yolo-v4/yolo_4classes_fsoso.weights"]
YOLO_PATH_DATA = ["yolo/fsoco/cone-obj.data",
                  "yolo/old/cone-obj.data",   "yolo/old/cone-obj.data", "yolo/yolo-v4/cone.data"]


# CONTROLLER
DEFAULT_ANGLE = 0.0  # degrees

HALF_CAR_WIDTH = 1.3  # meters
FRONT_DISTANCE = 5.0  # meters
HALF_TRACK_WIDTH = 1.9

# CAN

# OUTPUT
DEFAULT_SPEED_PEDAL = 10.0  # 10%
DEFAULT_BRAKE_PEDAL = 0.0  # %

CAN_DRIVERLESS_ID = 0x172
CAN_MOTOR_RPM_ID = 0x12d
CAN_STEERING_ID = 0x1a2

# viewer settings
VIEWER_SCALE = 100/3

# Predictive settings
SOFTWARE_LATENCY = 0.250

# Steering related
STEER_SPEED = 50  # 50º / s
STEER_DEAD_ZONE = 10  # 7 º
STEER_MAX = 90
STEER_MIN = -90
STEER_SENSOR_MIN = 31
STEER_SENSOR_MAX = 390
STEERING_OFFSET = -31
SIMULATION_TIME_STEEP = 0.02
STEER_TO_WHEEL = 1/3
STEER_CORRECTION = 2
MIN_CAR_SPEED_TO_STEER = 0.1

# CAR EMULATION / MODEL
MOTOR_RPM = 50
TIRE_DIAMETER = 0.228
RPM_TO_MS = ((TIRE_DIAMETER*math.pi)/60)
CAR_LENGHT = 1.5
STEER_WHEEL_MAX = 30
STEER_WHEEL_MIN = -30
SIMULATION_POS_ERROR = 0.0001
SIMULATION_THETA_ERROR = 0.0001

# Middle algorithm
MAX_TRACK_WIDTH = 5
MIN_TRACK_WIDTH = 2

# Vision Simulation
VIEW_MAX_DISTANCE = 10
VIEW_HFOV = np.deg2rad(90)
DROPOUT_PERCENTAGE = 0.1

MIN_MIDDLE_DISTANCE = 7
