import sys
import math
import os
from time import time
from threading import Thread
from constants import SHOW_IMG, RUN_FLAGS, SHOW_VIEWER, STEER_TO_WHEEL, STEER_CORRECTION, MIN_CAR_SPEED_TO_STEER
if "VISION_SIMULATION" in RUN_FLAGS:
    import vision_emulator as video
else:
    import video

if SHOW_IMG:
    import cv2

if SHOW_VIEWER:
    import viewer

if "CAR_SIMULATION" in RUN_FLAGS:
    os.system("sudo modprobe vcan")
    os.system("sudo ip link add dev vcan0 type vcan")
    os.system("sudo ip link set vcan0 up")
    import car_emulator
    car_emulator_thread = Thread(target=car_emulator.run_forever)
    car_emulator_thread.start()

import can_interface
if "CAN_READ" in RUN_FLAGS:
    can_recv_thread = Thread(target=can_interface.receive_thread)
    can_recv_thread.start()

#import controller
import controller2 as controller

if __name__ == "__main__":
    blue_all = []
    yellow_all = []
    fov_points = []
    middle_points = []
    predicted_path = []
    fov_points = [[2,2],[2,-2]]
    blue_all = []
    yellow_all = []
    car_pos = [0,0,0,0,0] # x,y, theta, steer
    steer_target_last = 0
    car_speed = 0
    motor_rpm = 0 
    while True:
        try:
            time_start = time()
           
            if "VISION_SIMULATION" in RUN_FLAGS:
                if "CAR_SIMULATION" in RUN_FLAGS:
                    car_pos = car_emulator.car_real_pos
                fov_points, blue_all, yellow_all, blue, yellow, prints_input, img = video.run(car_pos)
            else:
                blue, yellow, prints_input, img = video.run()

            try:
                steer_target, middle_points, prints_controller = controller.run(blue, yellow)
            except Exception as e:
                steer_target = 0
                middle_points = []
                prints_controller  = ""

            prints_controller += f"STEER TARGET:{steer_target:.0f}\n"
            steer_target = -steer_target*STEER_CORRECTION
            if car_speed > MIN_CAR_SPEED_TO_STEER:
                can_interface.run(steer_target)

            prints_can = "CAN DATA:\n"
            prints_can += f"    Motor speed: {motor_rpm} RPM\n"
            prints_can += f"    Car speed: {car_speed:.2f} m/s\n"
            steer_actual = can_interface.steering_sensor
            car_speed = can_interface.car_speed
            motor_rpm = can_interface.motor_rpm
            steer_target_last = steer_target
            

            # TODO put prints in a thread
            os.system("clear")
            print(prints_input, prints_controller, prints_can, f"Total time: {(time()-time_start)*1000:>5.0f}")

            if SHOW_IMG:
                cv2.imshow("frame", cv2.resize(img,(640,480)))
                if cv2.waitKey(1) == ord('q'):
                    break
            if SHOW_VIEWER:
                viewer.run([car_pos,[0,0,0,math.radians(steer_target)]],
                predicted_path,
                blue,yellow,
                middle_points,
                blue_all,
                yellow_all,
                fov_points)

        except KeyboardInterrupt:
            print("Keyboard interruption")
            exit()
